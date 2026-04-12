# Text Display

Plain text lines in a template are rendered as **TextDisplay** components, which support Discord markdown.

## Grouping Behavior

How text lines are grouped into TextDisplay components depends on newline separation:

| Separation | Result |
|---|---|
| Single newline | Lines are merged into **one** TextDisplay |
| Blank line (2+ newlines) | Each group becomes a **separate** TextDisplay |

### Example: Single TextDisplay

```
First line
Second line
```

Renders as one TextDisplay with content `First line\nSecond line`.

### Example: Two Separate TextDisplays

```
First paragraph

Second paragraph
```

Renders as two separate TextDisplay components.

## Usage in Sections

The same grouping rules apply to text lines inside a [`[section]`](section.md) block.
