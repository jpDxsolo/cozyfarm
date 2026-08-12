# Screenshot guide — Part 1

The milestone shot list for Part 1, and the house style every article follows.

## House style

Keep these identical across the whole series — the consistency is most of the
polish, and it means later articles need no re-decisions.

| Setting | Value |
| --- | --- |
| Editor theme | Godot **Dark** |
| Editor scale | **100%** |
| Window size | **1600 x 900** |
| Scene tree | expanded to the nodes being discussed, nothing else |
| Inspector | scrolled so the relevant property is visible |
| Highlight | red rounded box, via `tools/annotate.py` |

Crop out anything irrelevant. Don't capture the whole desktop.

## Automated shots

These ten are generated — do not take them by hand. Re-run:

```bash
godot --path . res://tools/capture_screenshots.tscn --resolution 1152x648
```

then:

```bash
python tools/postprocess.py
```

Capture **must** run at 1152x648. That's the project's own viewport size; at any
other resolution the `canvas_items` stretch applies a non-integer scale, which
both throws off the harness's camera framing and smears the pixel art.
`postprocess.py` then upscales x2 with nearest-neighbour to 2304x1296.

| File | Shows |
| --- | --- |
| `01_hero.png` | Blog cover / README banner — whole farm, player, crops |
| `04_character_layers.png` | Diagram: BaseSprite + HairSprite = finished character |
| `04a/b/c_*.png` | The three raw panels behind that diagram |
| `07a_camera_zoom_before.png` | Camera2D zoom 1 — character lost on screen |
| `07b_camera_zoom_after.png` | Camera2D zoom 4 — cozy |
| `09_tiny_farm.png` | The decorated test area |
| `10_final_game.png` | Player in the finished prototype |
| `11_flip_h.png` | Diagram: one walk frame, `flip_h` false vs true |
| `11a/b_*.png` | The two raw panels behind that diagram |

## Editor shots — captured by hand

These five need the Godot editor UI, so they're captured manually rather than
generated. Each is stored twice: `*_clean.png` is the untouched capture, and
`*.png` is the annotated version the article links. Numbers match the article
sections. Re-annotate with the commands under [Annotating](#annotating).

### `02_player_scene.png` — section 2

Open `scenes/player.tscn`. Scene dock fully expanded:

```
Player  (CharacterBody2D)
├── BaseSprite       (AnimatedSprite2D)
├── HairSprite       (AnimatedSprite2D)
├── CollisionShape2D
└── Camera2D
```

Box the whole tree. Readers use this to confirm they built it correctly.

### `03_spriteframes.png` — section 3

Select **BaseSprite**, then click its `SpriteFrames` resource to open the
SpriteFrames editor in the bottom panel. Make sure the shot shows:

- both animations in the list — `idle` and `walk`
- `idle` selected, with all **9** frames visible in the strip
- **Speed 12 FPS** and the **Loop** toggle on

This is the single most useful screenshot in Part 1 — give it room.

### `05_collision.png` — section 5

Select **CollisionShape2D**. Zoom the 2D viewport right in on the player so the
blue rectangle around the feet is unmistakably small relative to the body.
Inspector should show `Shape > Size = (9, 2)` and `Transform > Position = (0.5, 6)`.

Box the collision rect at the feet.

### `06_input_map.png` — section 6

**Project > Project Settings > Input Map**. Clear the filter box. Expand all four
actions so their bindings are visible:

```
move_up      W, Up
move_down    S, Down
move_left    A, Left
move_right   D, Right
```

### `08_animated_tree.png` — section 8

Open `scenes/world.tscn`, select `Decorations/Tree01`. Show the SpriteFrames
editor with its **4** frames, plus the Inspector's **Autoplay on Load** enabled.
Readers copy this pattern straight from the player.

## Annotating

`--box x,y,w,h`, `--arrow x1,y1,x2,y2` (points at x2,y2), `--label x,y,text`.
Coordinates are in image pixels. Always annotate *from* the `_clean` master and
write to the article filename, so the clean capture is never overwritten and the
callouts can be redone at any time.

The exact commands behind the current set:

```bash
python tools/annotate.py docs/screenshots/02_player_scene_clean.png --box 6,140,428,116 --out docs/screenshots/02_player_scene.png
```
```bash
python tools/annotate.py docs/screenshots/03_spriteframes_clean.png --box 238,670,342,82 --box 588,643,714,265 --box 456,605,130,32 --out docs/screenshots/03_spriteframes.png
```
```bash
python tools/annotate.py docs/screenshots/05_collision_clean.png --box 122,448,205,58 --box 632,250,210,70 --out docs/screenshots/05_collision.png
```
```bash
python tools/annotate.py docs/screenshots/06_input_map_clean.png --box 18,182,1096,292 --out docs/screenshots/06_input_map.png
```
```bash
python tools/annotate.py docs/screenshots/08_animated_tree_clean.png --box 586,643,580,140 --box 412,606,28,30 --out docs/screenshots/08_animated_tree.png
```
