# Getting Started

## Invite the Bot

[>> Invite Roler to your server <<](https://discord.com/oauth2/authorize?client_id=1488089368924000367)

## Required Permissions

Grant Roler the following permissions in your server:

| Permission | Required | Purpose |
|---|---|---|
| **Manage Roles** | ✅ | Assign and remove roles from members |
| **Send Messages** | ✅ | Post role panels in channels |
| **Read Message History** | ✅ | Fetch and update existing panels |
| **View Channels** | ✅ | Access channels where panels are posted |
| **Manage Webhooks** | ❌ Optional | Post panels with custom webhook identities |
| **Manage Messages** | ❌ Optional | Delete the original panel when webhook identity changes |

!!! warning "Role Hierarchy"
    The bot's role must be positioned **above** any role it needs to assign in the server's role hierarchy. If the bot's role is below a target role, it will fail to assign or remove it.

## Your First Panel

Here's the quickest path to a working role panel:

**Step 1 - Write a template**

In any channel the bot can read, send a message with your panel template. For example:

```
## 🎨 Pick your color

[button color=red]Red[/button] [button color=green]Green[/button] [button color=blurple]Blue[/button]
```

!!! tip
    The bot matches roles by the button's label text when no `role=` attribute is given. Make sure the label matches the exact role name in your server (case-sensitive).

**Step 2 - Create the panel**

Right-click (or long-press on mobile) the template message → **Apps** → **Roler** → **Create Role Panel**.

**Step 3 - Pick a channel**

A channel picker will appear. Select the channel where the panel should be posted.

**Step 4 - Done**

The bot validates your template and posts the panel. Members can now click buttons to get or lose roles.

**Step 5 - Edit anytime**

Edit your original template message and the bot automatically updates the live panel.

---

## Next Steps

- [Creating Panels](guide/creating-panels.md) - full workflow including update and delete
- [Reusable Templates](guide/reusable-templates.md) - define once, reference from any panel
- [Reference](reference/button.md) - complete syntax for every tag
