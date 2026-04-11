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
class ParsedTemplate:
    nodes: list[TextNode | ActionRowGroup | SeparatorNode] = field(default_factory=list)
    webhook: WebhookConfig = field(default_factory=WebhookConfig)
    template_id: str | None = None
