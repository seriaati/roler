from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TextNode:
    content: str


@dataclass
class ButtonNode:
    role_id: int | None
    label: str | None
    emoji: str | None
    color: str
    mode: str
    template_ref: str | None = None
    disabled: bool = False
    url: str | None = None


@dataclass
class ActionRowGroup:
    buttons: list[ButtonNode] = field(default_factory=list)


@dataclass
class SeparatorNode:
    size: str = "small"
    visible: bool = True


@dataclass
class WebhookConfig:
    name: str | None = None
    avatar_url: str | None = None
    present: bool = False


@dataclass
class ImageNode:
    url: str
    spoiler: bool = False


@dataclass
class GalleryItemNode:
    url: str
    spoiler: bool = False


@dataclass
class GalleryNode:
    items: list[GalleryItemNode] = field(default_factory=list)


@dataclass
class ThumbnailNode:
    url: str
    description: str | None = None
    spoiler: bool = False


@dataclass
class SectionNode:
    children: list[TextNode]
    accessory: ThumbnailNode | ButtonNode


@dataclass
class ParsedTemplate:
    nodes: list[
        TextNode | ActionRowGroup | SeparatorNode | ImageNode | GalleryNode | SectionNode
    ] = field(default_factory=list)
    webhook: WebhookConfig = field(default_factory=WebhookConfig)
    template_id: str | None = None
    stateful: bool = False
    on_color: str = "blurple"
    off_color: str = "grey"
    replace: bool = False
