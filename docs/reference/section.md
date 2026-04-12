# Section

A `[section]` groups up to 3 text lines with a single **accessory** - either a [`[thumbnail]`](#thumbnail-accessory) or a [`[button]`](button.md).

## Syntax

### With a Thumbnail accessory

```
[section]
Line of text
Another line
[thumbnail url=https://example.com/thumb.png]
[/section]
```

### With a Thumbnail + description and spoiler

```
[section]
Some description text
[thumbnail url=https://example.com/thumb.png description=Alt_text spoiler=true]
[/section]
```

### With a Button accessory

```
[section]
Pick your color role
[button role=123456789012345678 color=green]Green[/button]
[/section]
```

## Section Rules

- Non-tag, non-empty lines inside `[section]...[/section]` become text children (max 3).
- Text grouping follows the same rules as top-level text - see [Text Display](text.md) for details.
- The last `[thumbnail]` or `[button]` found inside the block becomes the accessory.
- A section must have exactly 1 accessory.

## Thumbnail Accessory

`[thumbnail]` can only appear as a section accessory - it cannot be used outside a `[section]` block.

### Thumbnail Attributes

| Attribute | Required | Values | Default | Description |
|---|---|---|---|---|
| `url` | ✅ | `http://` or `https://` URL | - | The image URL for the thumbnail |
| `description` | ❌ | String (≤ 256 chars) | none | Alt text / description for the thumbnail |
| `spoiler` | ❌ | `true` `false` | `false` | Whether to hide the thumbnail behind a spoiler blur |

## Limits

| Constraint | Value |
|---|---|
| Text children per section | 1 - 3 |
| Accessories per section | exactly 1 |
| Thumbnail description length | ≤ 256 characters |

## Examples

```
[section]
## 🎨 Color Roles
Pick a color to represent yourself.
[thumbnail url=https://example.com/palette.png description=Color_palette]
[/section]

[button role=111111111111111111 color=red]Red[/button]
[button role=222222222222222222 color=green]Green[/button]
```

```
[section]
Spoiler preview
[thumbnail url=https://example.com/secret.png spoiler=true]
[/section]
```
