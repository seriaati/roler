![Banner](images/BannerWithLogo.png)
![Showcase](images/Showcase.png)

# Roler

Discord bot for easy and descriptive role management.

[>> Click to invite <<](https://discord.com/oauth2/authorize?client_id=1488089368924000367)

## Overview

Roler lets server admins write a simple markup template in any message, then turn it into a persistent role panel with clickable buttons. Members click a button to get (or lose) a role.

## Why is this better?

- **Components v2**: Create beautiful role panels that look far more superior than Embeds. Mix markdown texts, emojis, buttons, and separators in any order to create a consistent, visually appealing look.
- **Customizability**: Change button colors, emojis, and even webhook identities for posting panels.
- **Easy edits**: Do inline edits for existing role panels without having to reconstruct everything from scratch.
- **Version control**: Keep old versions of your panel templates in message history and revert to them whenever you want.
- **Portability**: Move panels around different channels without having to redo the setup.
- **Shareability**: Use the same template to create the same panels across different servers or share them with others.
- **Reusable templates**: Define a role panel once and reference it from any other panel with a single button — no duplication needed.

## Bot permissions

The bot requires the following permissions in your server:

- **Manage Roles** to assign and remove roles from members
- **Send Messages** to post role panels in channels
- **Read Message History** to fetch and update existing panels
- **View Channels** to access channels where panels are posted
- **Manage Webhooks** if you want to post panels with custom webhook identities (optional)
- **Manage Messages** to delete the original panel when webhook identity changes (optional)

The bot's role must be positioned **above** any role it needs to assign in the server's role hierarchy.

## Usage

### 1. Write a template

In any channel the bot can read, send a message containing your role panel template. You can wrap it in a code block (` ``` `) or write it as plain text.

A template is made up of **text lines** (rendered as panel description), **button tags**, and **separator tags**.

#### Button syntax

```
[button role=ROLE_ID]Label[/button]
```

The `role` attribute is optional. When omitted, the bot matches the role by the button's label text (exact name match, case-sensitive). When provided, the bot looks up the role by its ID and the label is purely cosmetic.

All attributes:

| Attribute | Required | Values | Default | Description |
|-----------|----------|--------|---------|-------------|
| `role` | ❌ | Discord role ID (snowflake) | - | The role to assign/remove. If omitted, the role is matched by the button's label text. Mutually exclusive with `template` |
| `template` | ❌ | Template ID (alphanumeric, hyphens, underscores) | - | References a saved template. Clicking the button shows the template as an ephemeral panel. Mutually exclusive with `role` |
| `color` | ❌ | `blurple` `green` `red` `grey` | `blurple` | Button color |
| `mode` | ❌ | `toggle` `add` `remove` | `toggle` | How the role is applied |
| `emoji` | ❌ | Unicode emoji or custom Discord emoji | - | Emoji shown on the button |

**Modes:**

- `toggle` adds the role if the member doesn't have it, removes it if they do
- `add` always adds the role
- `remove` always removes the role

#### Custom Discord emojis

To use a custom emoji from your server (or any server the bot is in), paste the emoji's raw mention string as the `emoji` value:

```
emoji=<:emoji_name:emoji_id>
```

For animated custom emojis, prefix with `a`:

```
emoji=<a:emoji_name:emoji_id>
```

To get the raw string, type `\:emoji_name:` in Discord and send it, the message will show the full `<:name:id>` format. Copy that and use it as the attribute value.

Example:

```
[button role=1351855807167463424 emoji=<:pepe:1234567890123456789>]Pepe[/button]
[button role=1475117545122959380 emoji=<a:dance:9876543210987654321>]Dance[/button]
```

> The bot must be in a server that has access to the emoji, or the emoji must be from a server the bot shares with the user.

#### Rows

Buttons on the **same line** form one action row (up to 5 buttons per row). A **blank line** between button lines starts a new row. Up to **5 rows** are allowed per panel.

#### Separator syntax

```
[separator]
[separator size=large]
[separator size=small visible=false]
```

Alias:

```
---
```

Will translate to `[separator size=large visible=true]`.

All attributes:

| Attribute | Required | Values | Default | Description |
|-----------|----------|--------|---------|-------------|
| `size` | ❌ | `small` `large` | `large` | Spacing size of the separator |
| `visible` | ❌ | `true` `false` | `true` | Whether the divider line is visible |

#### Webhook identity syntax

By default, panels are posted by the bot. However, you can customize the profile avatar and name of the poster by providing the `[webhook]` tag:

```
[webhook name=ServerName avatar=https://example.com/avatar.png]
```

Place it anywhere in the template (it is not rendered as part of the panel). Both attributes are optional — omit either to keep the bot's default.

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | ❌ | Display name shown on the panel message (1–80 characters) |
| `avatar` | ❌ | Avatar URL shown on the panel message (must be `http://` or `https://`) |

> If you later edit the template and change the `name` or `avatar`, the bot will automatically delete the old panel message and re-send it with the new identity.

### 2. Example template

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
```

> The last two buttons have no `role=` attribute — the bot will look up roles named exactly **Genshin Impact** and **Honkai: Star Rail** in the server at the time a member clicks the button.

### 3. Create the panel

Right-click (or long-press on mobile) the message containing your template → **Apps** → **Roler** → **Create Role Panel**.

A channel picker will appear. Select the channel where the panel should be posted. The bot will validate your template and send the panel there.

> Requires the **Manage Roles** permission.

### 4. Update the panel

Edit your original template message. The bot automatically detects the edit, re-parses the template, and updates the live panel. If the edited template has errors, the bot will DM you with the details and leave the existing panel unchanged.

### 5. Delete the panel

Right-click the original template message **or** the live panel message → **Apps** → **Roler** → **Delete Role Panel**.

The bot removes the panel message and cleans up its database record.

> Requires the **Manage Roles** permission.

---

## Reusable Templates

Templates let you define a reusable role panel once and reference it from any other panel via a button. When a member clicks the button, the bot sends them an ephemeral message with the fully functional template panel.

### The `[template id=...]` tag

Place this tag at the top of a message to mark it as a template definition:

```
[template id=color-roles]
Pick your favorite color!
[button role=1234 color=red]Red[/button]
[button role=5678 color=green]Green[/button]
```

The `id` must be alphanumeric and may contain hyphens and underscores (1–64 characters). It is scoped to your server — the same ID can exist in different servers.

### Defining a template

Right-click the message containing your `[template id=...]` tag → **Apps** → **Roler** → **Define as Template**.

The bot validates the markup and saves the template. You'll receive an ephemeral confirmation: `✅ Template color-roles defined.`

> Requires the **Manage Roles** permission.

### Referencing a template from a panel

Use the `template=` attribute on a button in any role panel:

```
Welcome! Pick your roles below, or browse color roles.
[button role=9999]Member[/button]
[button template=color-roles]🎨 Color Roles[/button]
```

When a member clicks **🎨 Color Roles**, the bot sends them an ephemeral message with the fully rendered `color-roles` template, including all its functional role buttons.

> A template button **must** have a label and **cannot** also have a `role=` attribute.

### Auto-update on edit

Edit the original template message and the bot automatically re-parses it and updates the saved template. The next time anyone clicks a button referencing that template, they get the updated panel.

If the edited message has validation errors, the bot DMs the template creator with the details and leaves the existing template unchanged.

If you remove the `[template id=...]` tag entirely, the bot deletes the template record.

### End-to-end example

1. Send a message:
   ```
   [template id=color-roles]
   Pick your favorite color!
   [button role=1234 color=red]Red[/button]
   [button role=5678 color=green]Green[/button]
   ```
2. Right-click → **Apps** → **Roler** → **Define as Template**.
3. In another channel, send a role panel message:
   ```
   Welcome! Pick your roles below, or browse color roles.
   [button role=9999]Member[/button]
   [button template=color-roles]🎨 Color Roles[/button]
   ```
4. Right-click → **Apps** → **Roler** → **Create Role Panel**, select a channel.
5. Members can click **Member** to toggle their role, or **🎨 Color Roles** to open the color picker.

---

## Template validation rules

The bot will reject a template and show an error if:

- A button has no `role=` attribute **and** no label (name-based buttons require a label to match against)
- A button has neither a label nor an `emoji`
- Two buttons reference the same role ID
- Two name-based buttons share the same label (case-insensitive)
- A row contains more than **5 buttons**
- The template contains more than **5 rows**
- The `[webhook]` `name` is not between 1 and 80 characters
- The `[webhook]` `avatar` is not a valid HTTP(S) URL
- A template button (`template=`) also has a `role=` attribute (mutually exclusive)
- A template button has no label
- A template ID contains characters other than alphanumeric, hyphens, or underscores, or is longer than 64 characters

## Self-Hosting

### Requirements

- Python 3.14+
- PostgreSQL

### Environment variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token
ENV=prod

POSTGRES_PASSWORD=your_password
POSTGRES_DB=roler
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
```

### Running locally

```bash
uv sync
uv run main.py
```

### Running with Docker

```bash
docker build -t roler .
docker run --env-file .env roler
```

## Acknowledgements

Original idea by Algoinde on Enka Network Discord server.
