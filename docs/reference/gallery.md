# Gallery

## Syntax

```
[gallery]
[item url=https://example.com/photo1.png]
[item url=https://example.com/photo2.png spoiler=true]
[item url=https://example.com/photo3.png]
[/gallery]
```

Each `[item]` must be on its own line inside the `[gallery]...[/gallery]` block.

## Item Attributes

| Attribute | Required | Values | Default | Description |
|---|---|---|---|---|
| `url` | ✅ | `http://` or `https://` URL | - | The image URL for this gallery item |
| `spoiler` | ❌ | `true` `false` | `false` | Whether to hide this item behind a spoiler blur |

## Limits

The gallery supports **1 to 10 items** (Discord's limit).

## Examples

```
## Screenshots

[gallery]
[item url=https://example.com/screen1.png]
[item url=https://example.com/screen2.png]
[item url=https://example.com/screen3.png]
[/gallery]
```

```
[gallery]
[item url=https://example.com/preview.png spoiler=true]
[item url=https://example.com/reveal.png]
[/gallery]
```

!!! tip
    For a single image, use [`[image]`](image.md) instead.
