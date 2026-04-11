# Reusable Templates

Templates let you define a reusable role panel once and reference it from any other panel via a button. When a member clicks the button, the bot sends them an ephemeral message with the fully functional template panel.

## The `[template id=...]` Tag

Place this tag at the top of a message to mark it as a template definition:

```
[template id=color-roles]
Pick your favorite color!
[button role=1234 color=red]Red[/button]
[button role=5678 color=green]Green[/button]
```

See [`[template id=...]` reference](../reference/template-tag.md) for ID constraints and scoping rules.

## Defining a Template

1. Send a message with the `[template id=...]` tag at the top.
2. Right-click the message → **Apps** → **Roler** → **Define as Template**.
3. The bot validates the markup and saves the template.
4. You'll receive an ephemeral confirmation: `✅ Template color-roles defined.`

!!! warning "Permission required"
    You must have the **Manage Roles** permission to define a template.

## Referencing a Template from a Panel

Use the `template=` attribute on a button in any role panel:

```
Welcome! Pick your roles below, or browse color roles.
[button role=9999]Member[/button]
[button template=color-roles]🎨 Color Roles[/button]
```

When a member clicks **🎨 Color Roles**, the bot sends them an ephemeral message with the fully rendered `color-roles` template, including all its functional role buttons.

!!! note
    A template button **must** have a label and **cannot** also have a `role=` attribute. See [Button reference](../reference/button.md) for details.

## Auto-Update on Edit

Edit the original template message and the bot automatically re-parses it and updates the saved template. The next time anyone clicks a button referencing that template, they get the updated panel.

If the edited message has validation errors, the bot DMs the template creator with the details and leaves the existing template unchanged.

If you **remove the `[template id=...]` tag entirely**, the bot deletes the template record.

## End-to-End Example

**Step 1** - Send the template definition message:

```
[template id=color-roles]
Pick your favorite color!
[button role=1234 color=red]Red[/button]
[button role=5678 color=green]Green[/button]
```

**Step 2** - Right-click → **Apps** → **Roler** → **Define as Template**.

**Step 3** - In another channel, send a role panel message:

```
Welcome! Pick your roles below, or browse color roles.
[button role=9999]Member[/button]
[button template=color-roles]🎨 Color Roles[/button]
```

**Step 4** - Right-click → **Apps** → **Roler** → **Create Role Panel**, select a channel.

**Step 5** - Members can click **Member** to toggle their role, or **🎨 Color Roles** to open the color picker as an ephemeral panel.
