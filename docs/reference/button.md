# Button

## Syntax

```
[button attrs]Label[/button]
```

The label is the text displayed on the button. It is also used to match the role by name when no `role=` attribute is provided.

## Attributes

| Attribute | Required | Values | Default | Description |
|---|---|---|---|---|
| `role` | ❌ | Discord role ID (snowflake) | - | The role to assign/remove. If omitted, the role is matched by the button's label text (exact name, case-sensitive). Mutually exclusive with `template` and `url`. |
| `template` | ❌ | Template ID | - | References a saved template. Clicking the button shows the template as an ephemeral panel. Mutually exclusive with `role` and `url`. |
| `url` | ❌ | `http://` or `https://` URL | - | Makes the button a link that opens the URL. Mutually exclusive with `role` and `template`. Always grey. |
| `color` | ❌ | `blurple` `green` `red` `grey` | `blurple` | Button color. Ignored when `url` is set. |
| `mode` | ❌ | `toggle` `add` `remove` | `toggle` | How the role is applied. |
| `emoji` | ❌ | Unicode emoji or custom Discord emoji | - | Emoji shown on the button. |
| `disabled` | ❌ | `true` `false` | `false` | Whether the button is greyed out and non-interactive. |

## Modes

| Mode | Behavior |
|---|---|
| `toggle` | Adds the role if the member doesn't have it; removes it if they do. |
| `add` | Always adds the role, even if the member already has it. |
| `remove` | Always removes the role, even if the member doesn't have it. |

## Custom Discord Emojis

To use a custom emoji from your server (or any server the bot is in), paste the emoji's raw mention string as the `emoji` value:

```
emoji=<:emoji_name:emoji_id>
```

For animated custom emojis, prefix with `a`:

```
emoji=<a:emoji_name:emoji_id>
```

!!! tip "Getting the raw string"
    Type `\:emoji_name:` in Discord and send it. The message will show the full `<:name:id>` format. Copy that and use it as the attribute value.

```
[button role=1351855807167463424 emoji=<:pepe:1234567890123456789>]Pepe[/button]
[button role=1475117545122959380 emoji=<a:dance:9876543210987654321>]Dance[/button]
```

!!! note
    The bot must be in a server that has access to the emoji, or the emoji must be from a server the bot shares with the user.

## URL Buttons

A button with a `url=` attribute becomes a link button that opens the URL when clicked.

- Always displayed in grey regardless of the `color` attribute
- Cannot assign or remove roles (`role=` is not allowed)
- Cannot open templates (`template=` is not allowed)
- Must use a valid `http://` or `https://` URL
- Multiple URL buttons with the same label or URL are allowed

```
[button url=https://discord.com]Visit Discord[/button]
[button url=https://example.com emoji=🔗]Website[/button]
```

## Disabled Buttons

Add `disabled=true` to render a button as greyed out and non-interactive:

```
[button disabled=true color=grey]Unavailable[/button]
[button role=1234567890 disabled=true]Coming Soon[/button]
```

Disabled buttons are **exempt from all uniqueness rules** — multiple disabled buttons can share the same `role=`, `template=`, or label without conflict. Only enabled buttons are tracked for uniqueness.

This makes disabled buttons useful for category prefixes, row headers, or "coming soon" placeholders:

```
[button disabled=true color=grey]Ping: [/button] [button]Genshin Impact[/button]
[button disabled=true color=grey]Ping: [/button] [button]Honkai: Star Rail[/button]
```

## Rows

Buttons on the **same line** form one action row. A **blank line** between button lines starts a new row.

- Maximum **5 buttons** per row
- Maximum **5 rows** per panel

```
[button]A[/button] [button]B[/button] [button]C[/button]

[button]D[/button] [button]E[/button]
```

This produces two rows: `A B C` and `D E`.

## Examples

```
[button role=1234567890]Member[/button]

[button role=1234567890 color=green mode=add]Join[/button]
[button role=1234567890 color=red mode=remove]Leave[/button]

[button role=1234567890 emoji=🎮 color=blurple]Gamer[/button]

[button template=color-roles]🎨 Color Roles[/button]

[button url=https://example.com]Website[/button]

[button disabled=true]Coming Soon[/button]
```
