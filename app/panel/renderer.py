from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord

from app.markup.nodes import (
    GalleryNode,
    ImageNode,
    SectionNode,
    SeparatorNode,
    TextNode,
    ThumbnailNode,
)

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


@dataclass
class _RenderCtx:
    stateful: bool = False
    member: discord.Member | None = None
    template_id: str | None = None
    on_color: str = "blurple"
    off_color: str = "grey"


def _parse_emoji(emoji_str: str) -> discord.PartialEmoji | str:
    m = _CUSTOM_EMOJI_RE.fullmatch(emoji_str)
    if m:
        return discord.PartialEmoji(
            name=m.group("name"), id=int(m.group("id")), animated=m.group("animated") == "a"
        )
    return emoji_str


def _resolve_stateful_style(
    btn: ButtonNode, member: discord.Member, on_color: str, off_color: str
) -> discord.ButtonStyle:
    if btn.role_id is not None:
        has_role = any(r.id == btn.role_id for r in member.roles)
    elif btn.label is not None:
        has_role = any(r.name == btn.label for r in member.roles)
    else:
        has_role = False
    return _COLOR_MAP[on_color] if has_role else _COLOR_MAP[off_color]


def _button_style(btn: ButtonNode, ctx: _RenderCtx) -> discord.ButtonStyle:
    if ctx.stateful and ctx.member is not None and not btn.disabled and btn.template_ref is None:
        return _resolve_stateful_style(btn, ctx.member, ctx.on_color, ctx.off_color)
    return _COLOR_MAP.get(btn.color, discord.ButtonStyle.blurple)


def _resolve_custom_id(btn: ButtonNode, noop_counter: list[int], ctx: _RenderCtx) -> str:
    if btn.disabled:
        custom_id = f"noop:{noop_counter[0]}"
        noop_counter[0] += 1
        return custom_id
    if btn.template_ref is not None:
        return f"tpl:{btn.template_ref}"
    if ctx.stateful and ctx.template_id is not None:
        if btn.role_id is not None:
            return f"rp_s:{btn.mode}:{btn.role_id}:{ctx.template_id}"
        return f"rp_s:{btn.mode}:name:{btn.label}:{ctx.template_id}"
    if btn.role_id is not None:
        return f"rp:{btn.mode}:{btn.role_id}"
    return f"rp:{btn.mode}:name:{btn.label}"


def _build_section(
    node: SectionNode, noop_counter: list[int], ctx: _RenderCtx
) -> discord.ui.Section:
    text_displays = [discord.ui.TextDisplay(child.content) for child in node.children]
    if isinstance(node.accessory, ThumbnailNode):
        accessory: discord.ui.Thumbnail | discord.ui.Button = discord.ui.Thumbnail(
            media=node.accessory.url,
            description=node.accessory.description,
            spoiler=node.accessory.spoiler,
        )
    else:
        btn = node.accessory
        emoji = _parse_emoji(btn.emoji) if btn.emoji else None
        if btn.url is not None:
            accessory = discord.ui.Button(
                style=discord.ButtonStyle.link,
                url=btn.url,
                label=btn.label,
                emoji=emoji,
                disabled=btn.disabled,
            )
        else:
            accessory = discord.ui.Button(
                style=_button_style(btn, ctx),
                label=btn.label,
                emoji=emoji,
                custom_id=_resolve_custom_id(btn, noop_counter, ctx),
                disabled=btn.disabled,
            )
    return discord.ui.Section(*text_displays, accessory=accessory)


def _build_action_row(
    node: ActionRowGroup, noop_counter: list[int], ctx: _RenderCtx
) -> discord.ui.ActionRow:
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
                style=_button_style(btn, ctx),
                label=btn.label,
                emoji=emoji,
                custom_id=_resolve_custom_id(btn, noop_counter, ctx),
                disabled=btn.disabled,
            )
        row.add_item(button)
    return row


def render(
    template: ParsedTemplate,
    stateful: bool = False,
    member: discord.Member | None = None,
    template_id: str | None = None,
) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()
    noop_counter = [0]
    ctx = _RenderCtx(
        stateful=stateful,
        member=member,
        template_id=(template_id or template.template_id) if stateful else None,
        on_color=template.on_color,
        off_color=template.off_color,
    )

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
        elif isinstance(node, SectionNode):
            view.add_item(_build_section(node, noop_counter, ctx))
        else:
            view.add_item(_build_action_row(node, noop_counter, ctx))

    return view
