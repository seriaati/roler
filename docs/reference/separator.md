# Separator

## Syntax

```
[separator]
[separator size=large]
[separator size=small visible=false]
```

### Alias

```
---
```

The `---` alias is equivalent to `[separator size=large visible=true]`.

## Attributes

| Attribute | Required | Values | Default | Description |
|---|---|---|---|---|
| `size` | ❌ | `small` `large` | `large` | Spacing size of the separator |
| `visible` | ❌ | `true` `false` | `true` | Whether the divider line is visible |

## Examples

```
## Section One

[button]Role A[/button]

---

## Section Two

[button]Role B[/button]
```

```
[separator size=small visible=false]
```

Use `visible=false` for invisible spacing between sections without a visible line.
