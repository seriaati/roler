# Webhook

!!! tip "💎 Sponsor Feature"
    The `[webhook]` tag is a paid feature. To unlock it, [donate here](https://link.seria.moe/donate) and then contact [Seria on Discord](https://discord.com/users/410036441129943050).

!!! note "Normal panels only"
    The `[webhook]` tag only works in normal role panels. It cannot be used in reusable templates, since templates render as ephemeral messages which can only be sent as the bot.

## Syntax

```
[webhook name=ServerName avatar=https://example.com/avatar.png]
[webhook name="Server Name" avatar=https://example.com/avatar.png]
```

The `[webhook]` tag is not rendered as part of the panel content. It controls the identity of the bot account that posts the panel message.

Both attributes are optional - omit either to keep the bot's default name or avatar.

## Attributes

| Attribute | Required | Description |
|---|---|---|
| `name` | ❌ | Display name shown on the panel message (1-80 characters). Use quotes for names with spaces: `name="My Server"` |
| `avatar` | ❌ | Avatar URL shown on the panel message (must be `http://` or `https://`) |

## Behavior

By default, panels are posted by the bot using its own name and avatar. Adding a `[webhook]` tag causes the bot to use a Discord webhook to post the panel under the specified identity.

!!! warning "Identity changes trigger a re-post"
    If you later edit the template and change the `name` or `avatar`, the bot will automatically **delete the old panel message** and re-send it with the new identity. The panel's functionality is preserved.

!!! note "Required permissions"
    Posting with a custom webhook identity requires the **Manage Webhooks** permission. Deleting the old panel on identity change requires **Manage Messages**.

## Examples

```
[webhook name=MyServer avatar=https://example.com/server-icon.png]

# Welcome to role picker
[button]Member[/button]
```

```
[webhook name="Gaming Hub"]

## 🎮 Gaming roles
[button]Gamer[/button]
```
