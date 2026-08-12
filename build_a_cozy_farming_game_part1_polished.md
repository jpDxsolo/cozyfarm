# Build a Cozy Farming Game in Godot 4

## Part 1 -- Character Movement & Your First Farm Scene

> **What you'll build:** A playable prototype with a modular animated
> character, a following camera, and a small farm scene that already
> feels like the beginning of a cozy game.

![The finished Part 1 prototype](docs/screenshots/01_hero.png)

------------------------------------------------------------------------

# Project Setup

## Engine

-   **Godot 4.x**

## Asset Pack

This series uses **Sunnyside World** by Daniel Diggle.

Download: https://danieldiggle.itch.io/sunnyside

The pack includes modular characters, animated decorations, crops,
terrain, UI, and everything we'll need throughout the series.

Huge thanks to Daniel Diggle for creating such an excellent asset pack.
Please follow the included license when using it.

## Source Code

GitHub: https://github.com/jpDxsolo/cozyfarm

------------------------------------------------------------------------

# Series Roadmap

-   ✅ Part 1 -- Character Movement & First Farm Scene
-   ⬜ Part 2 -- Building Your First TileMap
-   ⬜ Part 3 -- World Interaction
-   ⬜ Part 4 -- Farming
-   ⬜ Part 5 -- Inventory
-   ⬜ Part 6 -- NPCs & Dialogue
-   ⬜ Part 7 -- Saving & Loading

------------------------------------------------------------------------

# Before You Begin

Throughout this series every section ends with a **Checkpoint**.

If your project doesn't match the checkpoint, stop and fix it before
moving on. It is much easier to correct mistakes immediately than
several chapters later.

------------------------------------------------------------------------

# 1. Understand the Character

Explain:

-   Base and hair are separate `AnimatedSprite2D` nodes.
-   This asset pack uses a single side-facing walk animation.
-   Left is achieved with `flip_h`.
-   Up and down reuse the same walk animation.
-   Additional animations (tools, fishing, chopping, etc.) will be used
    later.

------------------------------------------------------------------------

# 2. Create the Player Scene

    Player (CharacterBody2D)
    ├── BaseSprite (AnimatedSprite2D)
    ├── HairSprite (AnimatedSprite2D)
    ├── CollisionShape2D
    └── Camera2D

Leave the collision shape empty for now.

![The Player scene tree](docs/screenshots/02_player_scene.png)

### ✅ Checkpoint

You should have the node tree above with no errors.

------------------------------------------------------------------------

# 3. Configure BaseSprite

Create a SpriteFrames resource.

Create:

-   `walk`
-   `idle`

Import the matching body sprite strips.

The strips are single-row sprite sheets, so each frame is a slice of one
image. Frame size is **96 x 64**.

-   `idle` -- `base_idle_strip9.png`, **9 frames**
-   `walk` -- `base_walk_strip8.png`, **8 frames**

Configure both:

-   1 row
-   Loop enabled
-   12 FPS

> The number at the end of each filename tells you the frame count.
> `strip9` means 9 frames, `strip8` means 8.

![The SpriteFrames editor with idle and walk](docs/screenshots/03_spriteframes.png)

### ✅ Checkpoint

-   Body visible.
-   Walk previews.
-   Idle previews.

------------------------------------------------------------------------

# 4. Configure HairSprite

Repeat the exact same process for your chosen hairstyle.

Keep both sprites at `(0, 0)`.

The body carries the character; the hair is a separate sprite drawn on top of
it. Because both play the same animation names in lockstep, you can swap
hairstyles later without touching the movement code at all.

![BaseSprite plus HairSprite equals the finished character](docs/screenshots/04_character_layers.png)

### ✅ Checkpoint

The finished player should look correct.

------------------------------------------------------------------------

# 5. Configure Collision

Now that the player is visible, add a `RectangleShape2D`.

Keep the collision around the feet instead of the whole body.

Suggested starting size:

-   Width: **10--14**
-   Height: **6--8**

Adjust visually.

![Collision box around the feet only](docs/screenshots/05_collision.png)

> **📌 Why this matters**
>
> A collision box that covers the whole sprite makes a top-down character feel
> like a fridge. Keeping it at the feet is what lets the player tuck in behind
> trees and walk close to scenery without snagging on it.

### ✅ Checkpoint

The collision only covers the player's feet.

------------------------------------------------------------------------

# 6. Configure Input

Create:

-   move_up
-   move_down
-   move_left
-   move_right

Bind WASD and the arrow keys.

![The four movement actions in the Input Map](docs/screenshots/06_input_map.png)

### ✅ Checkpoint

All four actions exist in the Input Map.

------------------------------------------------------------------------

# 7. Add Movement & Animation

Your movement script should:

-   Use `Input.get_vector()`
-   Move the `CharacterBody2D`
-   Call `play_character_animation("idle")` inside `_ready()`
-   Play `walk` while moving
-   Play `idle` when stopped
-   Flip both body and hair when moving left

Explain **why** `_ready()` is important:

> `AnimatedSprite2D` does not begin animating automatically. Until
> `play()` is called, it simply displays its current frame.

There is no separate "walk left" animation. Left is the *same* walk animation
with `flip_h` turned on for both sprites:

![The same walk frame with flip_h false and true](docs/screenshots/11_flip_h.png)

> **⚠️ Common mistake**
>
> Player not animating? Check that `_ready()` calls
> `play_character_animation("idle")`. Setting the animation in the Inspector
> only picks which one is *selected* — it doesn't start playback.

### ✅ Checkpoint

The player is already idling before you press any keys.

------------------------------------------------------------------------

# 8. Build a Tiny Test Farm

Create:

    World
    ├── Decorations
    └── Player

Use a simple green background for now.

Add one or two animated trees (or mushrooms) using `AnimatedSprite2D`. The
setup is identical to the player's — a SpriteFrames resource with the strip
sliced into frames:

![An animated tree's SpriteFrames](docs/screenshots/08_animated_tree.png)

Enable looping and either:

-   set **Autoplay** to `idle`, or
-   call `play("idle")` inside `_ready()`.

Once those work, decorate the scene with anything else from the asset
pack that you like:

-   rocks
-   crates
-   flowers
-   crops
-   fences
-   signs

Don't spend too much time here---this scene is temporary and will be
replaced with a proper TileMap in Part 2.

![The decorated test area](docs/screenshots/09_tiny_farm.png)

> **📌 Why this matters**
>
> We aren't using a TileMap yet because placing decorations by hand keeps the
> focus on movement. All that empty green is deliberate — Part 2 replaces it
> with a real tile-based map.

### ✅ Checkpoint

-   Background isn't gray.
-   Animated decorations move immediately.
-   You have a few landmarks to walk around.

------------------------------------------------------------------------

# 9. Make It Feel Cozy

Enable the Camera2D.

Try:

    Zoom
    X: 4
    Y: 4

Adjust until it feels comfortable.

Zoom `1` — the character is lost on screen:

![Camera2D at zoom 1](docs/screenshots/07a_camera_zoom_before.png)

Zoom `4` — cozy:

![Camera2D at zoom 4](docs/screenshots/07b_camera_zoom_after.png)

### ✅ Checkpoint

The character fills a reasonable amount of the screen and the camera
follows smoothly.

------------------------------------------------------------------------

# 10. Final Review

Before moving on to Part 2:

-   [x] Character renders correctly.
-   [x] Body and hair stay synchronized.
-   [x] Idle starts automatically.
-   [x] Walk animation works.
-   [x] Left flips correctly.
-   [x] Camera follows the player.
-   [x] Decorations animate automatically.
-   [x] The prototype feels like a tiny game, not just a tech demo.

![The finished Part 1 prototype](docs/screenshots/10_final_game.png)

------------------------------------------------------------------------

# Next Time

Now that movement is finished, we've hit the first pain point:

Building terrain by hand doesn't scale.

In **Part 2** we'll solve that by introducing Godot's TileSet and
TileMapLayer systems, replacing our temporary scene with a real farm
that we can continue expanding throughout the rest of the series.
