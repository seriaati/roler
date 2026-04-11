# Image

## Syntax

```
[image url=https://example.com/photo.png]
[image url=https://example.com/photo.png spoiler=true]
```

The `[image]` tag is self-closing - no closing tag is needed.

## Attributes

| Attribute | Required | Values | Default | Description |
|---|---|---|---|---|
| `url` | ✅ | `http://` or `https://` URL | - | The image URL to display |
| `spoiler` | ❌ | `true` `false` | `false` | Whether to hide the image behind a spoiler blur |

## Examples

```
## Server Banner

[image url=https://example.com/banner.png]

---

## Spoiler Preview

[image url=https://example.com/secret.png spoiler=true]
```

!!! tip
    For multiple images in a single block, use [`[gallery]`](gallery.md) instead.
