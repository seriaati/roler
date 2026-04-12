# Creating Panels

## Writing a Template

In any channel the bot can read, send a message containing your role panel template. You can wrap it in a code block (` ``` `) or write it as plain text - the bot strips the fences before parsing.

A template is composed of:

| Node type | Description |
|---|---|
| **Text lines** | Rendered as panel description (supports Discord markdown) |
| **`[button]`** | A clickable role button |
| **`[separator]`** | A visual divider (or use `---`) |
| **`[image]`** | A single image |
| **`[gallery]`** | A block of multiple images |
| **`[section]`** | Groups 1–3 text lines with a thumbnail or button accessory |
| **`[webhook]`** | Sets the poster identity (not rendered in the panel) |

See the [Reference](../reference/button.md) section for full syntax on each tag.

## Full Example Template

```
[webhook name=MyServer avatar=https://example.com/server-icon.png]

# Welcome to role picker
## 🎨 Pick your color roles

[button role=1351855807167463424 color=red]Red[/button] [button role=1475117545122959380 color=green]Green[/button] [button role=1475119322501353564 color=blurple]Blue[/button]

-# Note: Ask admin if you want other colors.

---

## 🎮 Gaming roles

[button color=grey mode=add]Genshin Impact[/button]

[button color=grey mode=add]Honkai: Star Rail[/button]

## 🔔 Notification roles

[button disabled=true color=grey]Ping: [/button] [button color=grey mode=add]Genshin Impact[/button]
[button disabled=true color=grey]Ping: [/button] [button color=grey mode=add]Honkai: Star Rail[/button]
```

!!! note
    The last two buttons have no `role=` attribute - the bot will look up roles named exactly **Genshin Impact** and **Honkai: Star Rail** in the server at the time a member clicks the button. The `Ping:` buttons are disabled labels that can share the same label across rows. Disabled buttons are exempt from uniqueness rules.

## Creating a Panel

1. Right-click (or long-press on mobile) the message containing your template.
2. Navigate to **Apps** → **Roler** → **Create Role Panel**.
3. A channel picker will appear - select the destination channel.
4. The bot validates your template and posts the panel there.

!!! warning "Permission required"
    You must have the **Manage Roles** permission to create a panel.

## Updating a Panel

Edit your original template message. The bot automatically detects the edit, re-parses the template, and updates the live panel.

If the edited template contains errors, the bot will **DM you** with the details and leave the existing panel unchanged.

!!! tip
    Your message history acts as version control. You can copy an older version of your template back into the message to revert the panel.

## Deleting a Panel

1. Right-click the original template message **or** the live panel message.
2. Navigate to **Apps** → **Roler** → **Delete Role Panel**.

The bot removes the panel message and cleans up its database record.

!!! warning "Permission required"
    You must have the **Manage Roles** permission to delete a panel.

---

## Reference

- [Button](../reference/button.md) - full attribute table, modes, emojis, URL buttons, rows
- [Separator](../reference/separator.md) - size and visibility options
- [Image](../reference/image.md) - single image display
- [Gallery](../reference/gallery.md) - multi-image blocks
- [Section](../reference/section.md) - grouped text with thumbnail or button accessory
- [Webhook](../reference/webhook.md) - custom poster identity
