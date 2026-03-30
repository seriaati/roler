from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from app.db.models import RolePanel
from app.markup import parse_template
from app.markup.validator import validate
from app.panel.renderer import render

if TYPE_CHECKING:
    from app.types import Interaction


class ChannelPickerView(discord.ui.View):
    def __init__(self, source_message: discord.Message) -> None:
        super().__init__(timeout=120)
        self.source_message = source_message
        self.selected_channel: discord.TextChannel | None = None

    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        channel_types=[discord.ChannelType.text],
        placeholder="Select a channel to post the panel in…",
    )
    async def channel_select(
        self, interaction: Interaction, select: discord.ui.ChannelSelect
    ) -> None:
        channel = select.values[0].resolve()
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("Please select a text channel.", ephemeral=True)
            return

        self.selected_channel = channel
        self.stop()

        await _create_panel(interaction, self.source_message, channel)


async def _create_panel(
    interaction: Interaction, source_message: discord.Message, target_channel: discord.TextChannel
) -> None:
    content = source_message.content
    template = parse_template(content)
    errors = validate(template)

    if errors:
        error_list = "\n".join(f"• {e}" for e in errors)
        await interaction.response.send_message(
            f"❌ **Template has errors:**\n{error_list}", ephemeral=True
        )
        return

    if source_message.guild is None:
        await interaction.response.send_message(
            "This command can only be used in a server.", ephemeral=True
        )
        return

    view = render(template)

    try:
        sent = await target_channel.send(view=view)
    except discord.Forbidden:
        await interaction.response.send_message(
            f"I don't have permission to send messages in {target_channel.mention}.", ephemeral=True
        )
        return
    except discord.HTTPException as e:
        logger.exception(f"Failed to send panel to {target_channel.id}: {e}")
        await interaction.response.send_message(
            "Failed to send the panel. Please try again.", ephemeral=True
        )
        return

    await RolePanel.create(
        guild_id=source_message.guild.id,
        source_channel_id=source_message.channel.id,
        source_message_id=source_message.id,
        target_channel_id=target_channel.id,
        target_message_id=sent.id,
        created_by=interaction.user.id,
    )

    await interaction.response.send_message(
        f"✅ Role panel created in {target_channel.mention}.", ephemeral=True
    )


class RolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._create_ctx_menu = app_commands.ContextMenu(
            name="Create Role Panel", callback=self._create_role_panel
        )
        self._delete_ctx_menu = app_commands.ContextMenu(
            name="Delete Role Panel", callback=self._delete_role_panel
        )
        self.bot.tree.add_command(self._create_ctx_menu)
        self.bot.tree.add_command(self._delete_ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self._create_ctx_menu.name, type=self._create_ctx_menu.type)
        self.bot.tree.remove_command(self._delete_ctx_menu.name, type=self._delete_ctx_menu.type)

    @app_commands.checks.has_permissions(manage_roles=True)
    async def _create_role_panel(self, interaction: Interaction, message: discord.Message) -> None:
        if not message.content:
            await interaction.response.send_message(
                "That message has no text content to parse.", ephemeral=True
            )
            return

        template = parse_template(message.content)
        errors = validate(template)

        if errors:
            error_list = "\n".join(f"• {e}" for e in errors)
            await interaction.response.send_message(
                f"❌ **Template has errors:**\n{error_list}", ephemeral=True
            )
            return

        existing = await RolePanel.filter(source_message_id=message.id).first()
        if existing:
            await interaction.response.send_message(
                "A role panel already exists for that message. Delete it first.", ephemeral=True
            )
            return

        view = ChannelPickerView(source_message=message)
        await interaction.response.send_message(
            "Select the channel where the role panel should be posted:", view=view, ephemeral=True
        )

    @app_commands.checks.has_permissions(manage_roles=True)
    async def _delete_role_panel(self, interaction: Interaction, message: discord.Message) -> None:
        panel = await RolePanel.filter(source_message_id=message.id).first()
        if panel is None:
            panel = await RolePanel.filter(target_message_id=message.id).first()
        if panel is None:
            await interaction.response.send_message(
                "No role panel is linked to that message.", ephemeral=True
            )
            return

        target_channel = interaction.guild and interaction.guild.get_channel(
            panel.target_channel_id
        )
        if isinstance(target_channel, discord.TextChannel):
            try:
                target_message = await target_channel.fetch_message(panel.target_message_id)
                await target_message.delete()
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
                logger.warning(f"Could not delete target panel message: {e}")

        await panel.delete()
        await interaction.response.send_message("✅ Role panel deleted.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:
        panel = await RolePanel.filter(source_message_id=payload.message_id).first()
        if panel is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        try:
            source_message = await channel.fetch_message(payload.message_id)
        except (discord.NotFound, discord.HTTPException) as e:
            logger.warning(f"Could not fetch edited source message {payload.message_id}: {e}")
            return

        content = source_message.content
        if not content:
            return

        template = parse_template(content)
        errors = validate(template)

        if errors:
            logger.warning(
                f"Edited source message {payload.message_id} has validation errors; skipping update: {errors}"
            )
            try:
                creator = await self.bot.fetch_user(panel.created_by)
                error_list = "\n".join(f"• {e}" for e in errors)
                await creator.send(
                    f"⚠️ Your role panel template (message `{payload.message_id}`) has errors and could not be updated:\n{error_list}"
                )
            except Exception as e:
                logger.warning(f"Could not notify panel creator: {e}")
            return

        view = render(template)

        target_channel = self.bot.get_channel(panel.target_channel_id)
        if not isinstance(target_channel, discord.TextChannel):
            logger.warning(
                f"Target channel {panel.target_channel_id} not found; cleaning up DB record"
            )
            await panel.delete()
            return

        try:
            target_message = await target_channel.fetch_message(panel.target_message_id)
            await target_message.edit(view=view)
        except discord.NotFound:
            logger.warning(
                f"Target panel message {panel.target_message_id} not found; cleaning up DB record"
            )
            await panel.delete()
        except (discord.Forbidden, discord.HTTPException) as e:
            logger.exception(f"Failed to update panel message {panel.target_message_id}: {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RolesCog(bot))
