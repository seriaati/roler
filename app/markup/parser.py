from __future__ import annotations

import re

from app.markup.nodes import (
    ActionRowGroup,
    ButtonNode,
    GalleryItemNode,
    GalleryNode,
    ImageNode,
    ParsedTemplate,
    SeparatorNode,
    TextNode,
    WebhookConfig,
)

_CODE_BLOCK_RE = re.compile(r"```[^\n]*\n?(.*?)```", re.DOTALL)
_FENCE_LINE_RE = re.compile(r"^```[^\n]*$", re.MULTILINE)

_BUTTON_TAG_RE = re.compile(
    r"\[button(?P<attrs>(?:\s+[a-z_]+=\S+)*)\s*\](?P<label>[^\[]*)\[/button\]", re.IGNORECASE
)
_SEPARATOR_TAG_RE = re.compile(r"\[separator(?P<attrs>(?:\s+[a-z_]+=\S+)*)\s*\]", re.IGNORECASE)
_WEBHOOK_TAG_RE = re.compile(r"\[webhook(?P<attrs>(?:\s+[a-z_]+=\S+)*)\s*\]", re.IGNORECASE)
TEMPLATE_TAG_RE = re.compile(r"\[template\s+id=(?P<id>\S+)\s*\]", re.IGNORECASE)
_IMAGE_TAG_RE = re.compile(r"\[image(?P<attrs>(?:\s+[a-z_]+=\S+)*)\s*\]", re.IGNORECASE)
_GALLERY_OPEN_RE = re.compile(r"\[gallery\s*\]", re.IGNORECASE)
_GALLERY_CLOSE_RE = re.compile(r"\[/gallery\]", re.IGNORECASE)
_GALLERY_ITEM_RE = re.compile(r"\[item(?P<attrs>(?:\s+[a-z_]+=\S+)*)\s*\]", re.IGNORECASE)
_ATTR_RE = re.compile(r"([a-z_]+)=(\S+)", re.IGNORECASE)

_VALID_COLORS = {"blurple", "green", "red", "grey"}
_VALID_MODES = {"toggle", "add", "remove"}
_VALID_SIZES = {"small", "large"}


def _parse_button(attrs_str: str, label_text: str) -> ButtonNode:
    attrs: dict[str, str] = dict(_ATTR_RE.findall(attrs_str))

    role_id_str = attrs.get("role", "")
    role_id: int | None = int(role_id_str) if role_id_str.isdigit() else None

    label = label_text.strip() or None
    emoji = attrs.get("emoji") or None
    color = attrs.get("color", "blurple").lower()
    mode = attrs.get("mode", "toggle").lower()
    template_ref = attrs.get("template") or None
    disabled = attrs.get("disabled", "false").lower() == "true"
    url = attrs.get("url") or None

    if color not in _VALID_COLORS:
        color = "blurple"
    if mode not in _VALID_MODES:
        mode = "toggle"

    return ButtonNode(
        role_id=role_id,
        label=label,
        emoji=emoji,
        color=color,
        mode=mode,
        template_ref=template_ref,
        disabled=disabled,
        url=url,
    )


def _parse_image(attrs_str: str) -> ImageNode:
    attrs: dict[str, str] = dict(_ATTR_RE.findall(attrs_str))
    url = attrs.get("url", "")
    spoiler = attrs.get("spoiler", "false").lower() == "true"
    return ImageNode(url=url, spoiler=spoiler)


def _parse_gallery_item(attrs_str: str) -> GalleryItemNode:
    attrs: dict[str, str] = dict(_ATTR_RE.findall(attrs_str))
    url = attrs.get("url", "")
    spoiler = attrs.get("spoiler", "false").lower() == "true"
    return GalleryItemNode(url=url, spoiler=spoiler)


def _parse_gallery(block: str) -> GalleryNode:
    items = [
        _parse_gallery_item(m.group("attrs"))
        for m in _GALLERY_ITEM_RE.finditer(block)
    ]
    return GalleryNode(items=items)


def _parse_separator(attrs_str: str) -> SeparatorNode:
    attrs: dict[str, str] = dict(_ATTR_RE.findall(attrs_str))

    size = attrs.get("size", "large").lower()
    if size not in _VALID_SIZES:
        size = "small"

    visible_str = attrs.get("visible", "true").lower()
    visible = visible_str != "false"

    return SeparatorNode(size=size, visible=visible)


def _parse_webhook(attrs_str: str) -> WebhookConfig:
    attrs: dict[str, str] = dict(_ATTR_RE.findall(attrs_str))
    return WebhookConfig(
        name=attrs.get("name") or None, avatar_url=attrs.get("avatar") or None, present=True
    )


def _parse_button_block(block: str) -> ActionRowGroup | None:
    lines = [line for line in block.splitlines() if line.strip()]
    buttons: list[ButtonNode] = [
        _parse_button(m.group("attrs"), m.group("label"))
        for line in lines
        for m in _BUTTON_TAG_RE.finditer(line)
    ]
    if not buttons:
        return None
    return ActionRowGroup(buttons=buttons)


def _process_mixed_block(
    stripped: str,
    result: list[TextNode | ActionRowGroup | SeparatorNode | ImageNode | GalleryNode],
) -> None:
    lines = stripped.splitlines()
    current_row_lines: list[str] = []

    for line in lines:
        line_lower = line.lower()
        if "[button" in line_lower:
            current_row_lines.append(line)
        else:
            if current_row_lines:
                row = _parse_button_block("\n".join(current_row_lines))
                if row:
                    result.append(row)
                current_row_lines = []
            if line.strip() == "---":
                result.append(SeparatorNode(size="large", visible=True))
            elif sep_match := _SEPARATOR_TAG_RE.search(line):
                result.append(_parse_separator(sep_match.group("attrs")))
            elif img_match := _IMAGE_TAG_RE.search(line):
                result.append(_parse_image(img_match.group("attrs")))
            elif line.strip():
                result.append(TextNode(content=line.strip()))

    if current_row_lines:
        row = _parse_button_block("\n".join(current_row_lines))
        if row:
            result.append(row)


def _extract_code_blocks(source: str) -> str:
    matches = _CODE_BLOCK_RE.findall(source)
    if matches:
        return "\n".join(m.strip() for m in matches)
    if _FENCE_LINE_RE.search(source):
        return _FENCE_LINE_RE.sub("", source).strip()
    return source


def _extract_galleries(source: str) -> tuple[str, list[tuple[str, GalleryNode]]]:
    galleries: list[tuple[str, GalleryNode]] = []
    idx = 0

    def replacer(m: re.Match[str]) -> str:
        nonlocal idx
        placeholder = f"__GALLERY_{idx}__"
        galleries.append((placeholder, _parse_gallery(m.group(0))))
        idx += 1
        return f"\n{placeholder}\n"

    cleaned = re.sub(
        r"\[gallery\s*\].*?\[/gallery\]",
        replacer,
        source,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return cleaned, galleries


def _extract_webhook_config(source: str) -> tuple[str, WebhookConfig]:
    m = _WEBHOOK_TAG_RE.search(source)
    if not m:
        return source, WebhookConfig()
    webhook = _parse_webhook(m.group("attrs"))
    cleaned = _WEBHOOK_TAG_RE.sub("", source, count=1).strip()
    return cleaned, webhook


def _extract_template_id(source: str) -> tuple[str, str | None]:
    m = TEMPLATE_TAG_RE.search(source)
    if not m:
        return source, None
    template_id = m.group("id")
    cleaned = TEMPLATE_TAG_RE.sub("", source, count=1).strip()
    return cleaned, template_id


def parse_template(source: str) -> ParsedTemplate:
    source = _extract_code_blocks(source)
    source, template_id = _extract_template_id(source)
    source, webhook = _extract_webhook_config(source)
    source, galleries = _extract_galleries(source)

    gallery_map: dict[str, GalleryNode] = dict(galleries)

    blocks = re.split(r"\n{2,}", source)
    nodes: list[TextNode | ActionRowGroup | SeparatorNode | ImageNode | GalleryNode] = []

    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue

        if stripped in gallery_map:
            nodes.append(gallery_map[stripped])
        elif stripped == "---":
            nodes.append(SeparatorNode(size="large", visible=True))
        elif (
            "[button" in stripped.lower()
            or "[separator" in stripped.lower()
            or "[image" in stripped.lower()
        ):
            _process_mixed_block(stripped, nodes)
        else:
            nodes.append(TextNode(content=stripped))

    return ParsedTemplate(nodes=nodes, webhook=webhook, template_id=template_id)
