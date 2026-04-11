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
    from app.markup.nodes import ParsedTemplate
    from app.types import Interaction

_WEBHOOK_NAME = "Roler"


async def _get_or_create_webhook(
    channel: discord.TextChannel, bot_user: discord.ClientUser
) -> discord.Webhook:
    webhooks = await channel.webhooks()

    for wh in webhooks:
        if wh.user and wh.user.id == bot_user.id:
            return wh

    return await channel.create_webhook(name=_WEBHOOK_NAME)


async def _send_via_webhook(
    webhook: discord.Webhook,
    view: discord.ui.LayoutView,
    template: ParsedTemplate,
    bot_user: discord.ClientUser,
) -> discord.WebhookMessage:
    username = template.webhook.name or bot_user.name
    avatar_url = template.webhook.avatar_url or bot_user.display_avatar.url
    return await webhook.send(view=view, username=username, avatar_url=avatar_url, wait=True)


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


async def _resolve_bot_user(interaction: Interaction) -> discord.ClientUser | None:
    bot_user = interaction.client.user
    if bot_user is None:
        await interaction.response.send_message("Bot user is unavailable.", ephemeral=True)
    return bot_user


async def _setup_webhook(
    interaction: Interaction, target_channel: discord.TextChannel, bot_user: discord.ClientUser
) -> discord.Webhook | None:
    try:
        return await _get_or_create_webhook(target_channel, bot_user)
    except discord.Forbidden:
        await interaction.response.send_message(
            f"I need the **Manage Webhooks** permission in {target_channel.mention}.",
            ephemeral=True,
        )
    except discord.HTTPException as e:
        logger.exception(f"Failed to get/create webhook in {target_channel.id}: {e}")
        await interaction.response.send_message(
            "Failed to set up the webhook. Please try again.", ephemeral=True
        )
    return None


async def _send_panel_via_webhook(
    interaction: Interaction,
    source_message: discord.Message,
    target_channel: discord.TextChannel,
    template: ParsedTemplate,
    bot_user: discord.ClientUser,
) -> bool:
    webhook = await _setup_webhook(interaction, target_channel, bot_user)
    if webhook is None:
        return False

    view = render(template)
    try:
        sent = await _send_via_webhook(webhook, view, template, bot_user)
    except discord.Forbidden:
        await interaction.response.send_message(
            f"I don't have permission to send messages in {target_channel.mention}.", ephemeral=True
        )
        return False
    except discord.HTTPException as e:
        logger.exception(f"Failed to send panel to {target_channel.id}: {e}")
        await interaction.response.send_message(
            "Failed to send the panel. Please try again.", ephemeral=True
        )
        return False

    username = template.webhook.name or bot_user.name
    avatar_url = template.webhook.avatar_url or bot_user.display_avatar.url

    assert source_message.guild is not None
    await RolePanel.create(
        guild_id=source_message.guild.id,
        source_channel_id=source_message.channel.id,
        source_message_id=source_message.id,
        target_channel_id=target_channel.id,
        target_message_id=sent.id,
        created_by=interaction.user.id,
        webhook_id=webhook.id,
        webhook_token=webhook.token,
        webhook_name=username,
        webhook_avatar_url=avatar_url,
    )
    return True


async def _send_panel_as_bot(
    interaction: Interaction,
    source_message: discord.Message,
    target_channel: discord.TextChannel,
    template: ParsedTemplate,
) -> bool:
    view = render(template)
    try:
        sent = await target_channel.send(view=view)
    except discord.Forbidden:
        await interaction.response.send_message(
            f"I don't have permission to send messages in {target_channel.mention}.", ephemeral=True
        )
        return False
    except discord.HTTPException as e:
        logger.exception(f"Failed to send panel to {target_channel.id}: {e}")
        await interaction.response.send_message(
            "Failed to send the panel. Please try again.", ephemeral=True
        )
        return False

    assert source_message.guild is not None
    await RolePanel.create(
        guild_id=source_message.guild.id,
        source_channel_id=source_message.channel.id,
        source_message_id=source_message.id,
        target_channel_id=target_channel.id,
        target_message_id=sent.id,
        created_by=interaction.user.id,
    )
    return True


async def _create_panel(
    interaction: Interaction, source_message: discord.Message, target_channel: discord.TextChannel
) -> None:
    if source_message.guild is None:
        await interaction.response.send_message(
            "This command can only be used in a server.", ephemeral=True
        )
        return

    content = source_message.content
    template = parse_template(content)
    errors = validate(template)

    if errors:
        error_list = "\n".join(f"• {e}" for e in errors)
        await interaction.response.send_message(
            f"❌ **Template has errors:**\n{error_list}", ephemeral=True
        )
        return

    bot_user = await _resolve_bot_user(interaction)
    if bot_user is None:
        return

    if template.webhook.present:
        ok = await _send_panel_via_webhook(
            interaction, source_message, target_channel, template, bot_user
        )
    else:
        ok = await _send_panel_as_bot(interaction, source_message, target_channel, template)

    if ok:
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

        if panel.webhook_id and panel.webhook_token:
            webhook = discord.Webhook.partial(
                panel.webhook_id, panel.webhook_token, client=self.bot
            )
            try:
                await webhook.delete_message(panel.target_message_id)
            except discord.NotFound:
                pass
            except (discord.Forbidden, discord.HTTPException) as e:
                logger.warning(f"Could not delete webhook panel message: {e}")
        else:
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
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:  # noqa: PLR0911
        panel = await RolePanel.filter(source_message_id=payload.message_id).first()
        if panel is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        source_message = await self._fetch_source_message(channel, payload.message_id)
        if source_message is None or not source_message.content:
            return

        template = parse_template(source_message.content)
        errors = validate(template)

        if errors:
            await self._notify_creator_of_errors(panel, payload.message_id, errors)
            return

        try:
            view = render(template)
        except Exception as e:
            logger.exception(f"Failed to render template for panel {panel.id}: {e}")
            await self._notify_creator_of_failure(panel, payload.message_id, str(e))
            return

        target_channel = self.bot.get_channel(panel.target_channel_id)
        if not isinstance(target_channel, discord.TextChannel):
            logger.warning(
                f"Target channel {panel.target_channel_id} not found; cleaning up DB record"
            )
            await panel.delete()
            return

        bot_user = self.bot.user
        if bot_user is None:
            logger.warning("Bot user unavailable during panel edit")
            return

        was_webhook = bool(panel.webhook_id and panel.webhook_token)
        wants_webhook = template.webhook.present

        if was_webhook and wants_webhook:
            await self._edit_via_webhook(panel, view, template, target_channel, bot_user)
        elif not was_webhook and not wants_webhook:
            await self._edit_bot_message(panel, view, target_channel)
        else:
            await self._resend_panel(panel, view, template, target_channel, bot_user)

    async def _fetch_source_message(
        self, channel: discord.TextChannel, message_id: int
    ) -> discord.Message | None:
        try:
            return await channel.fetch_message(message_id)
        except (discord.NotFound, discord.HTTPException) as e:
            logger.warning(f"Could not fetch edited source message {message_id}: {e}")
            return None

    async def _notify_creator_of_errors(
        self, panel: RolePanel, message_id: int, errors: list[str]
    ) -> None:
        logger.warning(
            f"Edited source message {message_id} has validation errors; skipping update: {errors}"
        )
        try:
            creator = await self.bot.fetch_user(panel.created_by)
            error_list = "\n".join(f"• {e}" for e in errors)
            await creator.send(
                f"⚠️ Your role panel template (message `{message_id}`) has errors and could not be updated:\n{error_list}"
            )
        except Exception as e:
            logger.warning(f"Could not notify panel creator: {e}")

    async def _notify_creator_of_failure(
        self, panel: RolePanel, message_id: int, reason: str
    ) -> None:
        try:
            creator = await self.bot.fetch_user(panel.created_by)
            await creator.send(
                f"⚠️ Your role panel (message `{message_id}`) could not be updated: {reason}"
            )
        except Exception as e:
            logger.warning(f"Could not notify panel creator of failure: {e}")

    async def _edit_bot_message(
        self, panel: RolePanel, view: discord.ui.LayoutView, target_channel: discord.TextChannel
    ) -> None:
        try:
            target_message = await target_channel.fetch_message(panel.target_message_id)
            await target_message.edit(view=view)
        except discord.NotFound:
            logger.warning(
                f"Bot panel message {panel.target_message_id} not found; re-sending panel"
            )
            await self._resend_bot_message(panel, view, target_channel)
        except (discord.Forbidden, discord.HTTPException) as e:
            logger.error(f"Failed to edit bot panel message {panel.target_message_id}: {e}")
            await self._notify_creator_of_failure(panel, panel.source_message_id, str(e))

    async def _resend_bot_message(
        self, panel: RolePanel, view: discord.ui.LayoutView, target_channel: discord.TextChannel
    ) -> None:
        try:
            sent = await target_channel.send(view=view)
        except (discord.Forbidden, discord.HTTPException) as e:
            logger.exception(f"Failed to resend bot panel {panel.id} in {target_channel.id}: {e}")
            await self._notify_creator_of_failure(panel, panel.source_message_id, str(e))
            return

        panel.target_message_id = sent.id
        await panel.save(update_fields=["target_message_id"])
        logger.info(f"Resent bot panel {panel.id} as message {sent.id}")

    async def _edit_via_webhook(
        self,
        panel: RolePanel,
        view: discord.ui.LayoutView,
        template: ParsedTemplate,
        target_channel: discord.TextChannel,
        bot_user: discord.ClientUser,
    ) -> None:
        new_name = template.webhook.name or bot_user.name
        new_avatar = template.webhook.avatar_url or bot_user.display_avatar.url
        identity_changed = new_name != panel.webhook_name or new_avatar != panel.webhook_avatar_url

        if identity_changed:
            await self._resend_panel(panel, view, template, target_channel, bot_user)
            return

        webhook = discord.Webhook.partial(
            panel.webhook_id,  # type: ignore[arg-type]
            panel.webhook_token,  # type: ignore[arg-type]
            client=self.bot,
        )

        try:
            await webhook.edit_message(panel.target_message_id, view=view)
        except discord.NotFound:
            logger.warning(
                f"Webhook {panel.webhook_id} or message {panel.target_message_id} not found; re-sending panel"
            )
            await self._resend_panel(panel, view, template, target_channel, bot_user)
        except (discord.Forbidden, discord.HTTPException) as e:
            logger.exception(f"Failed to edit panel message {panel.target_message_id}: {e}")
            await self._notify_creator_of_failure(panel, panel.source_message_id, str(e))

    async def _resend_panel(
        self,
        panel: RolePanel,
        view: discord.ui.LayoutView,
        template: ParsedTemplate,
        target_channel: discord.TextChannel,
        bot_user: discord.ClientUser,
    ) -> None:
        if panel.webhook_id and panel.webhook_token:
            old_webhook = discord.Webhook.partial(
                panel.webhook_id,  # type: ignore[arg-type]
                panel.webhook_token,  # type: ignore[arg-type]
                client=self.bot,
            )
            try:
                await old_webhook.delete_message(panel.target_message_id)
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
                logger.warning(f"Could not delete old panel message during resend: {e}")
        else:
            try:
                old_message = await target_channel.fetch_message(panel.target_message_id)
                await old_message.delete()
            except (discord.NotFound, discord.Forbidden, discord.HTTPException) as e:
                logger.warning(f"Could not delete old panel message during resend: {e}")

        if template.webhook.present:
            try:
                webhook = await _get_or_create_webhook(target_channel, bot_user)
                sent = await _send_via_webhook(webhook, view, template, bot_user)
            except (discord.Forbidden, discord.HTTPException) as e:
                logger.exception(f"Failed to resend panel {panel.id} in {target_channel.id}: {e}")
                await self._notify_creator_of_failure(panel, panel.source_message_id, str(e))
                return

            new_name = template.webhook.name or bot_user.name
            new_avatar = template.webhook.avatar_url or bot_user.display_avatar.url

            panel.target_message_id = sent.id
            panel.webhook_id = webhook.id
            panel.webhook_token = webhook.token
            panel.webhook_name = new_name
            panel.webhook_avatar_url = new_avatar
            await panel.save(
                update_fields=[
                    "target_message_id",
                    "webhook_id",
                    "webhook_token",
                    "webhook_name",
                    "webhook_avatar_url",
                ]
            )
            logger.info(f"Resent panel {panel.id} via webhook {webhook.id}")
        else:
            try:
                sent = await target_channel.send(view=view)
            except (discord.Forbidden, discord.HTTPException) as e:
                logger.exception(f"Failed to resend panel {panel.id} in {target_channel.id}: {e}")
                await self._notify_creator_of_failure(panel, panel.source_message_id, str(e))
                return

            panel.target_message_id = sent.id
            panel.webhook_id = None
            panel.webhook_token = None
            panel.webhook_name = None
            panel.webhook_avatar_url = None
            await panel.save(
                update_fields=[
                    "target_message_id",
                    "webhook_id",
                    "webhook_token",
                    "webhook_name",
                    "webhook_avatar_url",
                ]
            )
            logger.info(f"Resent panel {panel.id} as bot message {sent.id}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RolesCog(bot))
