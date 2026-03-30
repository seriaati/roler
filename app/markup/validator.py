from __future__ import annotations

from typing import TYPE_CHECKING

from app.markup.nodes import ActionRowGroup

if TYPE_CHECKING:
    from app.markup.nodes import ParsedTemplate

_VALID_COLORS = {"blurple", "green", "red", "grey"}
_VALID_MODES = {"toggle", "add", "remove"}
_MIN_SNOWFLAKE = 10**17
_MAX_SNOWFLAKE = 10**19


def validate(template: ParsedTemplate) -> list[str]:
    errors: list[str] = []

    action_rows = [node for node in template if isinstance(node, ActionRowGroup)]

    if len(action_rows) > 5:
        errors.append(f"Too many button rows ({len(action_rows)}), max is 5")

    for row_idx, row in enumerate(action_rows, start=1):
        if len(row.buttons) > 5:
            errors.append(f"Row {row_idx} has {len(row.buttons)} buttons, max is 5")

        for btn in row.buttons:
            if not btn.role_id or not (_MIN_SNOWFLAKE <= btn.role_id <= _MAX_SNOWFLAKE):
                errors.append(
                    f"Row {row_idx}: button has an invalid or missing role ID ({btn.role_id!r})"
                )

            if btn.label is None and btn.emoji is None:
                errors.append(
                    f"Row {row_idx}: button for role {btn.role_id} needs a label or emoji"
                )

            if btn.color not in _VALID_COLORS:
                errors.append(
                    f"Row {row_idx}: button for role {btn.role_id} has invalid color {btn.color!r}"
                )

            if btn.mode not in _VALID_MODES:
                errors.append(
                    f"Row {row_idx}: button for role {btn.role_id} has invalid mode {btn.mode!r}"
                )

    return errors
