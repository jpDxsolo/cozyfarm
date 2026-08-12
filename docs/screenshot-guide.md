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

## Editor shots — capture by hand

These five need the Godot editor UI. Numbers below match the article sections.

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

```bash
python tools/annotate.py docs/screenshots/02_player_scene.png --box 40,120,360,190 --label 40,120,"Scene tree"
```

`--box x,y,w,h`, `--arrow x1,y1,x2,y2` (points at x2,y2), `--label x,y,text`.
Writes `*_annotated.png` beside the original, so the clean capture survives.
