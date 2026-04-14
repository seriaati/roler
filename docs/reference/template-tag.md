# Template Tag

## Syntax

```
[template id=my-template-id]
[template id=my-template-id stateful=true]
[template id=color-roles stateful=true on=green off=red]
[template id=my-menu replace=true]
[template id=full stateful=true on=green off=grey replace=true]
```

Place this tag at the **top of a message** to mark it as a reusable template definition. The rest of the message is the template content - text, buttons, separators, images, etc.

## Attributes

| Attribute | Required | Description |
|---|---|---|
| `id` | ✅ | Unique identifier for this template within the server |
| `stateful` | ❌ | When `true`, role button colors reflect the user's current role state (default: `false`) |
| `on` | ❌ | Button color when the user **has** the role. Only effective when `stateful=true` (default: `blurple`) |
| `off` | ❌ | Button color when the user **does not have** the role. Only effective when `stateful=true` (default: `grey`) |
| `replace` | ❌ | When `true`, clicking a button that references this template will edit the current ephemeral message instead of sending a new one (default: `false`) |

Valid color values for `on` and `off`: `blurple`, `green`, `red`, `grey`.

## ID Constraints

- Alphanumeric characters, hyphens (`-`), and underscores (`_`) only
- Length: 1-64 characters
- Scoped per-guild - the same ID can exist in different servers without conflict

## Stateful Buttons

When `stateful=true`, role buttons in the ephemeral response shown to users will reflect their current role membership:

- **User has the role** → button appears in the `on` color (default: **blurple**)
- **User does not have the role** → button appears in the `off` color (default: **grey**)

You can customize these colors using the `on` and `off` attributes:

```
[template id=color-roles stateful=true on=green off=red]
```

With this configuration:
- **User has the role** → button appears **green**
- **User does not have the role** → button appears **red**

Any `color=` customization on role buttons is ignored when `stateful=true`. Non-role buttons (template-ref buttons, URL buttons) keep their configured colors.

This applies to both role-ID buttons (`role=123456`) and name-matched buttons (label-only buttons).

## Replace Mode

`replace=true` is defined on the **target** template — the one being navigated to. When a button references a template that has `replace=true`, clicking it edits the current ephemeral message in place rather than sending a new one.

```
[template id=main-menu]
[button template=settings]Settings[/button]

[template id=settings replace=true]
# Settings
...
```

In this example, clicking the Settings button edits the existing ephemeral message to show the settings template, rather than sending a new ephemeral reply.

This is useful for building multi-page menus where navigating between templates feels seamless.

**Notes:**
- `replace` has no effect when the template is opened as the first response (e.g. directly from a panel button), since there is no existing ephemeral message to replace at that point.
- Each template controls its own replace behavior independently.

## Placement

The `[template id=...]` tag must appear at the top of the message. Content before it is not supported.

## Scoping

Templates are scoped to the server (guild) where they are defined. A template with `id=color-roles` in Server A is completely separate from one with the same ID in Server B.

## Full Workflow

See [Reusable Templates](../guide/reusable-templates.md) for the complete define → reference → auto-update workflow with examples.
