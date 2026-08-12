# cozyfarm

A small top-down farming game built in **Godot 4.7** (GL Compatibility renderer).

## Current state

Very early. There's a world scene and a player `CharacterBody2D` with 8-way
WASD/arrow movement and layered sprite animation (a base body sprite plus a
separate hair sprite that stays in sync).

- [scenes/player.gd](scenes/player.gd) — movement + animation state
- [scenes/player.tscn](scenes/player.tscn) — player scene
- [scenes/world.tscn](scenes/world.tscn) — main scene

## Art assets are not included

This project uses the [Sunnyside World](https://danieldiggle.itch.io/sunnyside)
asset pack by Daniel Diggle. That pack is commercially licensed and cannot be
redistributed, so `art/` is gitignored and the scenes here will show missing
resources on a fresh clone.

To run it, buy the pack and extract it into `art/` matching the layout the
scenes expect:

```
art/
  Tileset/spr_tileset_sunnysideworld_16px.png
  characters/Human/IDLE/...
  characters/Human/WALKING/...
  characters/Human/ATTACK/...
  Elements/Other/...
```

Godot will regenerate the `.import` files on first open.

## Running

Open the project folder in Godot 4.7 and press F5.

## Controls

| Action | Keys |
| --- | --- |
| Move | `WASD` or arrow keys |

## License

The code in this repository is MIT licensed (see [LICENSE](LICENSE)). The art
assets are **not** covered by that license and are not distributed here.
