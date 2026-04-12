# Validation Rules

The bot validates your template before creating or updating a panel. If any rule is violated, the operation is rejected and you receive an error message describing the problem.

## Button Rules

- A button with no `role=` attribute must have a label (used for name-based role matching)
- A button must have either a label or an `emoji` (or both)
- Two buttons cannot reference the same role ID.
- Two buttons cannot reference the same template ID.
- Two name-based buttons (no `role=`) cannot share the same label (case-insensitive).
- **Disabled buttons are exempt from all uniqueness rules.**

## Row Rules

- A row cannot contain more than **5 buttons**
- A template cannot contain more than **5 rows**

## Webhook Rules

- The `[webhook]` `name` must be between 1 and 80 characters
- The `[webhook]` `avatar` must be a valid `http://` or `https://` URL

## Template Button Rules

- A template button (`template=`) cannot also have a `role=` attribute (mutually exclusive)
- A template button must have a label

## URL Button Rules

- A URL button (`url=`) cannot also have a `role=` or `template=` attribute (mutually exclusive)
- A URL button's `url` must start with `http://` or `https://`

## Template ID Rules

- A template ID may only contain alphanumeric characters, hyphens, and underscores
- A template ID cannot be longer than 64 characters

## Image Rules

- An `[image]` tag's `url` must start with `http://` or `https://`

## Gallery Rules

- A `[gallery]` must contain at least **1** item and no more than **10** items
- Each `[gallery]` item's `url` must start with `http://` or `https://`

## Section Rules

- A `[section]` must have between **1 and 3** text children
- A `[section]` must have exactly **1** accessory (`[thumbnail]` or `[button]`)

## Thumbnail Rules

- A `[thumbnail]` `url` must start with `http://` or `https://`
- A `[thumbnail]` `description` must be **256 characters or fewer**
