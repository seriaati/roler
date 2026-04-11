from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from loguru import logger

from app.db.models import PanelTemplate
from app.markup import parse_template
from app.markup.validator import validate
from app.panel.renderer import render

if TYPE_CHECKING:
    import re

    from app.types import Interaction


async def _apply_role(interaction: Interaction, mode: str, role: discord.Role) -> None:
    assert interaction.guild is not None
    bot_member = interaction.guild.me
    if role >= bot_member.top_role:
        await interaction.response.send_message(
            f"I cannot assign **{role.name}**, it is above my highest role.", ephemeral=True
        )
        return

    if not bot_member.guild_permissions.manage_roles:
        await interaction.response.send_message(
            "I need the **Manage Roles** permission to assign roles.", ephemeral=True
        )
        return

    member = interaction.user
    if not isinstance(member, discord.Member):
        await interaction.response.send_message(
            "Could not resolve your member data.", ephemeral=True
        )
        return

    try:
        if mode == "add":
            await member.add_roles(role, reason="Role panel")
            await interaction.response.send_message(f"✅ Added **{role.name}**.", ephemeral=True)
        elif mode == "remove" or role in member.roles:
            await member.remove_roles(role, reason="Role panel")
            await interaction.response.send_message(f"✅ Removed **{role.name}**.", ephemeral=True)
        else:
            await member.add_roles(role, reason="Role panel")
            await interaction.response.send_message(f"✅ Added **{role.name}**.", ephemeral=True)
    except discord.Forbidden:
        logger.warning(f"Missing permissions to assign role {role.id}")
        await interaction.response.send_message(
            "I don't have permission to assign that role.", ephemeral=True
        )
    except discord.HTTPException as e:
        logger.exception(f"HTTP error assigning role {role.id}: {e}")
        await interaction.response.send_message(
            "Something went wrong. Please try again.", ephemeral=True
        )


class RolePanelButton(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"rp:(?P<mode>toggle|add|remove):(?P<role_id>\d+)",
):
    def __init__(self, mode: str, role_id: int) -> None:
        self.mode = mode
        self.role_id = role_id
        super().__init__(discord.ui.Button(custom_id=f"rp:{mode}:{role_id}"))

    @classmethod
    async def from_custom_id(
        cls, _i: discord.Interaction, _item: discord.ui.Button, match: re.Match[str]
    ) -> RolePanelButton:
        return cls(mode=match["mode"], role_id=int(match["role_id"]))

    async def callback(self, interaction: Interaction) -> None:
        if not interaction.guild:
            await interaction.response.send_message(
                "This button can only be used in a server.", ephemeral=True
            )
            return

        role = interaction.guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message(
                f"Role `{self.role_id}` no longer exists.", ephemeral=True
            )
            return

        await _apply_role(interaction, self.mode, role)


class RolePanelButtonByName(
    discord.ui.DynamicItem[discord.ui.Button],
    template=r"rp:(?P<mode>toggle|add|remove):name:(?P<label>.+)",
):
    def __init__(self, mode: str, label: str) -> None:
        self.mode = mode
        self.label = label
        super().__init__(discord.ui.Button(custom_id=f"rp:{mode}:name:{label}"))

    @classmethod
    async def from_custom_id(
        cls, _i: discord.Interaction, _item: discord.ui.Button, match: re.Match[str]
    ) -> RolePanelButtonByName:
        return cls(mode=match["mode"], label=match["label"])

    async def callback(self, interaction: Interaction) -> None:
        if not interaction.guild:
            await interaction.response.send_message(
                "This button can only be used in a server.", ephemeral=True
            )
            return

        role = discord.utils.get(interaction.guild.roles, name=self.label)
        if role is None:
            await interaction.response.send_message(
                f"No role named **{self.label}** was found in this server.", ephemeral=True
            )
            return

        await _apply_role(interaction, self.mode, role)


class TemplateButton(
    discord.ui.DynamicItem[discord.ui.Button], template=r"tpl:(?P<template_id>.+)"
):
    def __init__(self, template_id: str) -> None:
        self.template_id = template_id
        super().__init__(discord.ui.Button(custom_id=f"tpl:{template_id}"))

    @classmethod
    async def from_custom_id(
        cls, _i: discord.Interaction, _item: discord.ui.Button, match: re.Match[str]
    ) -> TemplateButton:
        return cls(template_id=match["template_id"])

    async def callback(self, i: Interaction) -> None:
        if not i.guild:
            await i.response.send_message(
                "This button can only be used in a server.", ephemeral=True
            )
            return

        await i.response.defer(ephemeral=True)

        record = await PanelTemplate.filter(
            guild_id=i.guild_id, template_id=self.template_id
        ).first()

        if record is None:
            await i.followup.send(f"Template `{self.template_id}` not found.", ephemeral=True)
            return

        parsed = parse_template(record.content)
        errors = validate(parsed)

        if errors:
            error_list = "\n".join(f"• {e}" for e in errors)
            await i.followup.send(f"❌ **Template has errors:**\n{error_list}", ephemeral=True)
            return

        view = render(parsed)
        await i.followup.send(view=view, ephemeral=True)
