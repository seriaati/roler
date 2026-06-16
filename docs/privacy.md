# Privacy Policy

**Last updated: June 16, 2026**

This Privacy Policy explains what data the Roler Discord bot ("Roler", "the bot", "we") collects, why, and how it is handled. By adding Roler to a Discord server or interacting with it, you agree to this policy.

If you self-host Roler, you are the data controller for your own instance and this policy describes the official hosted instance operated at [roler.seria.moe](https://roler.seria.moe).

## Summary

- Roler only reads the text content of a message when a server moderator **explicitly** turns that message into a role panel or template, or when a message that is *already* a panel/template source is edited.
- Roler does **not** read, log, or monitor general chat messages.
- Roler does **not** use Members or Presence data, and does **not** use any data to train machine-learning or AI models.

## What Roler does

Roler lets server moderators write a markup template in a normal Discord message and turn it into a persistent "role panel" — a message with clickable buttons that members use to give themselves or remove roles.

## What data we collect and store

Roler stores the minimum data needed to operate role panels and templates, in a PostgreSQL database hosted alongside the bot.

### Role panels

For each role panel created, we store:

- The server (guild) ID
- The source channel and message IDs
- The target channel and message IDs (where the panel is posted)
- The Discord user ID of the moderator who created the panel
- Creation timestamp
- If the optional webhook feature is used: the webhook ID, token, display name, and avatar URL used to post the panel

We do **not** store the text content of role-panel source messages. When a source message is edited, Roler re-fetches that single message from Discord, regenerates the panel, and discards the content.

### Templates

When a moderator explicitly saves a message as a reusable template ("Define as Template"), we additionally store:

- The template ID chosen in the markup
- **The full text content of that template message** (so the template can be re-used by other panels)
- The server ID, source channel and message IDs, creator user ID, and timestamps

This is the only case in which message content is persisted off-platform, and it only happens for messages a moderator deliberately designates as a template.

### Message content intent

Roler uses Discord's privileged **Message Content** intent. It is used to:

1. Read the content of a message a moderator selects via the "Create Role Panel" or "Define as Template" command, in order to parse the role-panel markup.
2. Keep a live panel or template in sync when its **source message is edited**. The edit handler ignores every message except those whose ID already matches a stored panel or template.

Roler does not read, store, or process the content of any other messages.

## What we do not collect

- We do not use the Server Members or Presence intents.
- We do not collect message attachments, voice data, or DMs (Roler may send you a DM to notify you of a template error, but does not read DMs).
- We do not collect or store personal data beyond Discord IDs and the template content described above.

## Third-party data sharing

Roler does not sell or share your data. The only outbound data transfer is for the optional sponsor-only webhook feature: to verify sponsor status, Roler sends the requesting user's Discord ID to the sponsor API at `api.seria.moe`. No message content is sent.

Data necessarily passes through Discord's platform, which is governed by [Discord's Privacy Policy](https://discord.com/privacy).

## Machine learning / AI

Roler does **not** use any collected data to train, fine-tune, or evaluate machine-learning or AI models, and does not provide data to any third party for that purpose.

## Data retention and deletion

- Deleting a role panel (via the "Delete Role Panel" command) removes its database record.
- Deleting or removing the `[template ...]` tag from a template message removes the stored template, including its content.
- Removing Roler from your server stops all further data collection. To request deletion of any remaining stored data associated with your server or user ID, contact us (below).

## Children's privacy

Roler is intended for use on Discord and is subject to Discord's minimum age requirements. It is not directed at children below those requirements.

## Changes to this policy

We may update this policy. Material changes will be reflected by the "Last updated" date above.

## Contact

Questions or data-deletion requests: contact **Seria** on Discord at [discord.com/users/410036441129943050](https://discord.com/users/410036441129943050), or open an issue at [github.com/seriaati/roler](https://github.com/seriaati/roler).
