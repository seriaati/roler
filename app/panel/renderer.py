from __future__ import annotations

import re
from typing import TYPE_CHECKING

import discord

from app.markup.nodes import GalleryNode, ImageNode, SeparatorNode, TextNode

if TYPE_CHECKING:
    from app.markup.nodes import ActionRowGroup, ButtonNode, ParsedTemplate

_COLOR_MAP: dict[str, discord.ButtonStyle] = {
    "blurple": discord.ButtonStyle.blurple,
    "green": discord.ButtonStyle.green,
    "red": discord.ButtonStyle.red,
    "grey": discord.ButtonStyle.grey,
}

_SPACING_MAP: dict[str, discord.SeparatorSpacing] = {
    "small": discord.SeparatorSpacing.small,
    "large": discord.SeparatorSpacing.large,
}

_CUSTOM_EMOJI_RE = re.compile(r"<(?P<animated>a)?:(?P<name>[^:]+):(?P<id>\d+)>")


def _parse_emoji(emoji_str: str) -> discord.PartialEmoji | str:
    m = _CUSTOM_EMOJI_RE.fullmatch(emoji_str)
    if m:
        return discord.PartialEmoji(
            name=m.group("name"), id=int(m.group("id")), animated=m.group("animated") == "a"
        )
    return emoji_str


def _resolve_custom_id(btn: ButtonNode, noop_counter: list[int]) -> str:
    if btn.disabled:
        custom_id = f"noop:{noop_counter[0]}"
        noop_counter[0] += 1
        return custom_id
    if btn.template_ref is not None:
        return f"tpl:{btn.template_ref}"
    if btn.role_id is not None:
        return f"rp:{btn.mode}:{btn.role_id}"
    return f"rp:{btn.mode}:name:{btn.label}"


def _build_action_row(node: ActionRowGroup, noop_counter: list[int]) -> discord.ui.ActionRow:
    row = discord.ui.ActionRow()
    for btn in node.buttons:
        emoji = _parse_emoji(btn.emoji) if btn.emoji else None
        if btn.url is not None:
            button = discord.ui.Button(
                style=discord.ButtonStyle.link,
                url=btn.url,
                label=btn.label,
                emoji=emoji,
                disabled=btn.disabled,
            )
        else:
            button = discord.ui.Button(
                style=_COLOR_MAP.get(btn.color, discord.ButtonStyle.blurple),
                label=btn.label,
                emoji=emoji,
                custom_id=_resolve_custom_id(btn, noop_counter),
                disabled=btn.disabled,
            )
        row.add_item(button)
    return row


def render(template: ParsedTemplate) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()
    noop_counter = [0]

    for node in template.nodes:
        if isinstance(node, TextNode):
            view.add_item(discord.ui.TextDisplay(node.content))
        elif isinstance(node, SeparatorNode):
            spacing = _SPACING_MAP.get(node.size, discord.SeparatorSpacing.small)
            view.add_item(discord.ui.Separator(spacing=spacing, visible=node.visible))
        elif isinstance(node, ImageNode):
            view.add_item(
                discord.ui.MediaGallery(
                    discord.components.MediaGalleryItem(node.url, spoiler=node.spoiler)
                )
            )
        elif isinstance(node, GalleryNode):
            items = [
                discord.components.MediaGalleryItem(item.url, spoiler=item.spoiler)
                for item in node.items
            ]
            view.add_item(discord.ui.MediaGallery(*items))
        else:
            view.add_item(_build_action_row(node, noop_counter))

    return view
