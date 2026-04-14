from __future__ import annotations

import re
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from app.db.models import PanelTemplate
from app.markup import parse_template
from app.markup.parser import TEMPLATE_TAG_RE
from app.markup.validator import validate

if TYPE_CHECKING:
    from app.types import Interaction

_TEMPLATE_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


async def _notify_template_creator(
    bot: commands.Bot, created_by: int, message_id: int, errors: list[str]
) -> None:
    logger.warning(
        f"Edited template message {message_id} has validation errors; skipping update: {errors}"
    )
    try:
        creator = await bot.fetch_user(created_by)
        error_list = "\n".join(f"• {e}" for e in errors)
        await creator.send(
            f"⚠️ Your panel template (message `{message_id}`) has errors and could not be updated:\n{error_list}"
        )
    except Exception as e:
        logger.warning(f"Could not notify template creator: {e}")


class TemplatesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._define_template_ctx_menu = app_commands.ContextMenu(
            name="Define as Template", callback=self._define_template
        )
        self.bot.tree.add_command(self._define_template_ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self._define_template_ctx_menu.name, type=self._define_template_ctx_menu.type
        )

    @app_commands.checks.has_permissions(manage_roles=True)
    async def _define_template(self, interaction: Interaction, message: discord.Message) -> None:
        if not message.content:
            await interaction.response.send_message(
                "That message has no text content to parse.", ephemeral=True
            )
            return

        if message.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        parsed = parse_template(message.content)

        if parsed.template_id is None:
            await interaction.response.send_message(
                "Message must contain a `[template id=...]` tag.", ephemeral=True
            )
            return

        if not _TEMPLATE_ID_RE.match(parsed.template_id):
            await interaction.response.send_message(
                f"Template ID `{parsed.template_id}` is invalid."
                " Use alphanumeric characters, hyphens, and underscores (1-64 chars).",
                ephemeral=True,
            )
            return

        errors = validate(parsed)
        if errors:
            error_list = "\n".join(f"• {e}" for e in errors)
            await interaction.response.send_message(
                f"❌ **Template has errors:**\n{error_list}", ephemeral=True
            )
            return

        existing = await PanelTemplate.filter(
            guild_id=message.guild.id, template_id=parsed.template_id
        ).first()

        if existing is not None and existing.source_message_id != message.id:
            await interaction.response.send_message(
                f"Template ID `{parsed.template_id}` is already in use by another message.",
                ephemeral=True,
            )
            return

        stripped_content = _strip_template_tag(message.content)

        if existing is not None:
            existing.source_channel_id = message.channel.id
            existing.content = stripped_content
            existing.stateful = parsed.stateful
            await existing.save(
                update_fields=["source_channel_id", "content", "stateful", "updated_at"]
            )
        else:
            await PanelTemplate.create(
                guild_id=message.guild.id,
                template_id=parsed.template_id,
                source_channel_id=message.channel.id,
                source_message_id=message.id,
                content=stripped_content,
                stateful=parsed.stateful,
                created_by=interaction.user.id,
            )

        await interaction.response.send_message(
            f"✅ Template `{parsed.template_id}` defined.", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent) -> None:  # noqa: PLR0911
        record = await PanelTemplate.filter(source_message_id=payload.message_id).first()
        if record is None:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except (discord.NotFound, discord.HTTPException) as e:
            logger.warning(f"Could not fetch edited template message {payload.message_id}: {e}")
            return

        if not message.content:
            return

        parsed = parse_template(message.content)

        if parsed.template_id is None:
            await record.delete()
            logger.info(
                f"Template {record.template_id!r} deleted because [template] tag was removed"
            )
            return

        if parsed.template_id != record.template_id:
            conflict = await PanelTemplate.filter(
                guild_id=record.guild_id, template_id=parsed.template_id
            ).first()
            if conflict is not None:
                try:
                    creator = await self.bot.fetch_user(record.created_by)
                    await creator.send(
                        f"⚠️ Could not rename template `{record.template_id}` to"
                        f" `{parsed.template_id}` - that ID is already in use."
                        " The old template remains unchanged."
                    )
                except Exception as e:
                    logger.warning(f"Could not notify template creator of ID conflict: {e}")
                return

        errors = validate(parsed)
        if errors:
            await _notify_template_creator(self.bot, record.created_by, payload.message_id, errors)
            return

        record.template_id = parsed.template_id
        record.content = _strip_template_tag(message.content)
        record.stateful = parsed.stateful
        await record.save(update_fields=["template_id", "content", "stateful", "updated_at"])
        logger.info(f"Updated template {record.template_id!r} from message {payload.message_id}")


def _strip_template_tag(source: str) -> str:
    return TEMPLATE_TAG_RE.sub("", source, count=1).strip()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TemplatesCog(bot))
