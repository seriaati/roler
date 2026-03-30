from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from loguru import logger

if TYPE_CHECKING:
    import re

    from app.types import Interaction


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
            if self.mode == "add":
                await member.add_roles(role, reason="Role panel")
                await interaction.response.send_message(
                    f"✅ Added **{role.name}**.", ephemeral=True
                )
            elif self.mode == "remove" or role in member.roles:
                await member.remove_roles(role, reason="Role panel")
                await interaction.response.send_message(
                    f"✅ Removed **{role.name}**.", ephemeral=True
                )
            else:
                await member.add_roles(role, reason="Role panel")
                await interaction.response.send_message(
                    f"✅ Added **{role.name}**.", ephemeral=True
                )
        except discord.Forbidden:
            logger.warning(f"Missing permissions to assign role {self.role_id}")
            await interaction.response.send_message(
                "I don't have permission to assign that role.", ephemeral=True
            )
        except discord.HTTPException as e:
            logger.exception(f"HTTP error assigning role {self.role_id}: {e}")
            await interaction.response.send_message(
                "Something went wrong. Please try again.", ephemeral=True
            )
