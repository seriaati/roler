# Template Tag

## Syntax

```
[template id=my-template-id]
```

Place this tag at the **top of a message** to mark it as a reusable template definition. The rest of the message is the template content - text, buttons, separators, images, etc.

## Attributes

| Attribute | Required | Description |
|---|---|---|
| `id` | ✅ | Unique identifier for this template within the server |

## ID Constraints

- Alphanumeric characters, hyphens (`-`), and underscores (`_`) only
- Length: 1-64 characters
- Scoped per-guild - the same ID can exist in different servers without conflict

## Placement

The `[template id=...]` tag must appear at the top of the message. Content before it is not supported.

## Scoping

Templates are scoped to the server (guild) where they are defined. A template with `id=color-roles` in Server A is completely separate from one with the same ID in Server B.

## Full Workflow

See [Reusable Templates](../guide/reusable-templates.md) for the complete define → reference → auto-update workflow with examples.
