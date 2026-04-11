from __future__ import annotations

import re
from typing import TYPE_CHECKING

from app.markup.nodes import ActionRowGroup, GalleryNode, ImageNode, SeparatorNode

if TYPE_CHECKING:
    from app.markup.nodes import ButtonNode, ParsedTemplate

_VALID_COLORS = {"blurple", "green", "red", "grey"}
_VALID_MODES = {"toggle", "add", "remove"}
_VALID_SIZES = {"small", "large"}
_MIN_SNOWFLAKE = 10**17
_MAX_SNOWFLAKE = 10**19
_TEMPLATE_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def _validate_webhook(template: ParsedTemplate, errors: list[str]) -> None:
    if template.webhook.name is not None:
        name = template.webhook.name
        if not (1 <= len(name) <= 80):
            errors.append(f"Webhook name must be between 1 and 80 characters (got {len(name)})")

    if template.webhook.avatar_url is not None:
        url = template.webhook.avatar_url
        if not url.startswith(("http://", "https://")):
            errors.append(f"Webhook avatar must be a valid HTTP(S) URL (got {url!r})")


def _validate_template_button(row_idx: int, btn: ButtonNode, errors: list[str]) -> None:
    if btn.role_id is not None:
        errors.append(f"Row {row_idx}: template button cannot also have a role= attribute")
    if btn.label is None:
        errors.append(f"Row {row_idx}: template button must have a label")
    if btn.template_ref and not _TEMPLATE_ID_RE.match(btn.template_ref):
        errors.append(
            f"Row {row_idx}: template ID {btn.template_ref!r} is invalid"
            " (use alphanumeric characters, hyphens, and underscores, 1-64 chars)"
        )


def _validate_button_identity(
    row_idx: int,
    btn: ButtonNode,
    seen_role_ids: set[int],
    seen_role_names: set[str],
    errors: list[str],
) -> None:
    if btn.template_ref is not None:
        _validate_template_button(row_idx, btn, errors)
        return

    if btn.role_id is not None:
        if btn.role_id in seen_role_ids:
            errors.append(f"Row {row_idx}: role ID {btn.role_id} is already used by another button")
        else:
            seen_role_ids.add(btn.role_id)
        if not (_MIN_SNOWFLAKE <= btn.role_id <= _MAX_SNOWFLAKE):
            errors.append(f"Row {row_idx}: button has an invalid role ID ({btn.role_id!r})")
        return

    if btn.label is None:
        errors.append(
            f"Row {row_idx}: button without a role= attribute must have a label to match by name"
        )
        return

    label_key = btn.label.lower()
    if label_key in seen_role_names:
        errors.append(f"Row {row_idx}: role name {btn.label!r} is already used by another button")
    else:
        seen_role_names.add(label_key)


def _validate_button_row(
    row_idx: int,
    row: ActionRowGroup,
    seen_role_ids: set[int],
    seen_role_names: set[str],
    errors: list[str],
) -> None:
    if len(row.buttons) > 5:
        errors.append(f"Row {row_idx} has {len(row.buttons)} buttons, max is 5")

    for btn in row.buttons:
        if btn.url is not None:
            if not btn.url.startswith(("http://", "https://")):
                errors.append(
                    f"Row {row_idx}: URL button has an invalid URL {btn.url!r}"
                    " (must start with http:// or https://)"
                )
            if btn.role_id is not None:
                errors.append(
                    f"Row {row_idx}: URL button cannot also have a role= attribute"
                )
            if btn.template_ref is not None:
                errors.append(
                    f"Row {row_idx}: URL button cannot also have a template= attribute"
                )
            if btn.color not in {"grey", "blurple"}:
                errors.append(
                    f"Row {row_idx}: URL buttons are always grey; color={btn.color!r} has no effect"
                )
            continue

        _validate_button_identity(row_idx, btn, seen_role_ids, seen_role_names, errors)

        if btn.template_ref is not None:
            continue

        if btn.label is None and btn.emoji is None:
            errors.append(f"Row {row_idx}: button for role {btn.role_id} needs a label or emoji")

        if btn.color not in _VALID_COLORS:
            errors.append(
                f"Row {row_idx}: button for role {btn.role_id} has invalid color {btn.color!r}"
            )

        if btn.mode not in _VALID_MODES:
            errors.append(
                f"Row {row_idx}: button for role {btn.role_id} has invalid mode {btn.mode!r}"
            )


def _validate_image(idx: int, node: ImageNode, errors: list[str]) -> None:
    if not node.url.startswith(("http://", "https://")):
        errors.append(
            f"Image {idx}: URL {node.url!r} is invalid (must start with http:// or https://)"
        )


def _validate_gallery(idx: int, node: GalleryNode, errors: list[str]) -> None:
    if len(node.items) < 1:
        errors.append(f"Gallery {idx}: must have at least 1 item")
    if len(node.items) > 10:
        errors.append(f"Gallery {idx}: has {len(node.items)} items, max is 10")
    for item_idx, item in enumerate(node.items, start=1):
        if not item.url.startswith(("http://", "https://")):
            errors.append(
                f"Gallery {idx}, item {item_idx}: URL {item.url!r} is invalid"
                " (must start with http:// or https://)"
            )


def validate(template: ParsedTemplate) -> list[str]:
    errors: list[str] = []

    _validate_webhook(template, errors)

    action_rows = [node for node in template.nodes if isinstance(node, ActionRowGroup)]

    if len(action_rows) > 5:
        errors.append(f"Too many button rows ({len(action_rows)}), max is 5")

    seen_role_ids: set[int] = set()
    seen_role_names: set[str] = set()
    for row_idx, row in enumerate(action_rows, start=1):
        _validate_button_row(row_idx, row, seen_role_ids, seen_role_names, errors)

    for sep_idx, sep in enumerate(
        (node for node in template.nodes if isinstance(node, SeparatorNode)), start=1
    ):
        if sep.size not in _VALID_SIZES:
            errors.append(f"Separator {sep_idx} has invalid size {sep.size!r}")

    for img_idx, img in enumerate(
        (node for node in template.nodes if isinstance(node, ImageNode)), start=1
    ):
        _validate_image(img_idx, img, errors)

    for gal_idx, gal in enumerate(
        (node for node in template.nodes if isinstance(node, GalleryNode)), start=1
    ):
        _validate_gallery(gal_idx, gal, errors)

    return errors
