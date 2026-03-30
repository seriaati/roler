from __future__ import annotations

from typing import TYPE_CHECKING

from app.markup.nodes import ActionRowGroup, SeparatorNode

if TYPE_CHECKING:
    from app.markup.nodes import ParsedTemplate

_VALID_COLORS = {"blurple", "green", "red", "grey"}
_VALID_MODES = {"toggle", "add", "remove"}
_VALID_SIZES = {"small", "large"}
_MIN_SNOWFLAKE = 10**17
_MAX_SNOWFLAKE = 10**19


def _validate_webhook(template: ParsedTemplate, errors: list[str]) -> None:
    if template.webhook.name is not None:
        name = template.webhook.name
        if not (1 <= len(name) <= 80):
            errors.append(f"Webhook name must be between 1 and 80 characters (got {len(name)})")

    if template.webhook.avatar_url is not None:
        url = template.webhook.avatar_url
        if not url.startswith(("http://", "https://")):
            errors.append(f"Webhook avatar must be a valid HTTP(S) URL (got {url!r})")


def _validate_button_row(
    row_idx: int, row: ActionRowGroup, seen_role_ids: set[int], errors: list[str]
) -> None:
    if len(row.buttons) > 5:
        errors.append(f"Row {row_idx} has {len(row.buttons)} buttons, max is 5")

    for btn in row.buttons:
        if btn.role_id and btn.role_id in seen_role_ids:
            errors.append(f"Row {row_idx}: role ID {btn.role_id} is already used by another button")
        else:
            seen_role_ids.add(btn.role_id)

        if not btn.role_id or not (_MIN_SNOWFLAKE <= btn.role_id <= _MAX_SNOWFLAKE):
            errors.append(
                f"Row {row_idx}: button has an invalid or missing role ID ({btn.role_id!r})"
            )

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


def validate(template: ParsedTemplate) -> list[str]:
    errors: list[str] = []

    _validate_webhook(template, errors)

    action_rows = [node for node in template.nodes if isinstance(node, ActionRowGroup)]

    if len(action_rows) > 5:
        errors.append(f"Too many button rows ({len(action_rows)}), max is 5")

    seen_role_ids: set[int] = set()
    for row_idx, row in enumerate(action_rows, start=1):
        _validate_button_row(row_idx, row, seen_role_ids, errors)

    for sep_idx, sep in enumerate(
        (node for node in template.nodes if isinstance(node, SeparatorNode)), start=1
    ):
        if sep.size not in _VALID_SIZES:
            errors.append(f"Separator {sep_idx} has invalid size {sep.size!r}")

    return errors
