from __future__ import annotations

import re
from typing import TYPE_CHECKING

import discord

from app.markup.nodes import GalleryNode, ImageNode, SeparatorNode, TextNode

if TYPE_CHECKING:
    from app.markup.nodes import ParsedTemplate

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


def render(template: ParsedTemplate) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()

    for node in template.nodes:
        if isinstance(node, TextNode):
            view.add_item(discord.ui.TextDisplay(node.content))
        elif isinstance(node, SeparatorNode):
            spacing = _SPACING_MAP.get(node.size, discord.SeparatorSpacing.small)
            view.add_item(discord.ui.Separator(spacing=spacing, visible=node.visible))
        elif isinstance(node, ImageNode):
            gallery = discord.ui.MediaGallery(
                discord.components.MediaGalleryItem(node.url, spoiler=node.spoiler)
            )
            view.add_item(gallery)
        elif isinstance(node, GalleryNode):
            items = [
                discord.components.MediaGalleryItem(item.url, spoiler=item.spoiler)
                for item in node.items
            ]
            gallery = discord.ui.MediaGallery(*items)
            view.add_item(gallery)
        else:
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
                    style = _COLOR_MAP.get(btn.color, discord.ButtonStyle.blurple)
                    if btn.template_ref is not None:
                        custom_id = f"tpl:{btn.template_ref}"
                    elif btn.role_id is not None:
                        custom_id = f"rp:{btn.mode}:{btn.role_id}"
                    else:
                        custom_id = f"rp:{btn.mode}:name:{btn.label}"
                    button = discord.ui.Button(
                        style=style,
                        label=btn.label,
                        emoji=emoji,
                        custom_id=custom_id,
                        disabled=btn.disabled,
                    )
                row.add_item(button)
            view.add_item(row)

    return view
