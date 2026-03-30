from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TextNode:
    content: str


@dataclass
class ButtonNode:
    role_id: int
    label: str | None
    emoji: str | None
    color: str
    mode: str


@dataclass
class ActionRowGroup:
    buttons: list[ButtonNode] = field(default_factory=list)


@dataclass
class SeparatorNode:
    size: str = "small"
    visible: bool = True


ParsedTemplate = list[TextNode | ActionRowGroup | SeparatorNode]
