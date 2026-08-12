# Screenshot harness for the tutorial series. Not part of the game itself.
#
#   godot --path . res://tools/capture_screenshots.tscn --resolution 1152x648
#
# 1152x648 is the project's own viewport size. At any other resolution the
# canvas_items stretch applies a non-integer scale, which throws off the camera
# framing maths below AND smears the pixel art. Upscale the PNGs afterwards.
extends Node2D

const OUT := "res://docs/screenshots/"

var out_dir: String
var world: Node2D
var player: CharacterBody2D
var cam: Camera2D
var base_sprite: AnimatedSprite2D
var hair_sprite: AnimatedSprite2D


func _ready() -> void:
	out_dir = ProjectSettings.globalize_path(OUT)
	DirAccess.make_dir_recursive_absolute(out_dir)

	# Must run at the project's native 1152x648. Any other window size goes
	# through a non-integer canvas_items stretch, which both breaks the camera
	# framing math and smears the pixel art. Upscale x2 afterwards instead.
	assert(get_viewport().get_final_transform().get_scale().is_equal_approx(Vector2.ONE),
		"run with --resolution 1152x648")

	world = load("res://scenes/world.tscn").instantiate()
	add_child(world)

	player = world.get_node("Player")
	cam = player.get_node("Camera2D")
	base_sprite = player.get_node("BaseSprite")
	hair_sprite = player.get_node("HairSprite")

	await settle(20)

	# --- 01 hero: whole farm framed tight, player standing by the crop plot ---
	player.position = Vector2(28, 12)
	fit_all(14.0)
	await settle(8)
	await shoot("01_hero")

	# --- 07a camera zoom BEFORE (zoom 1 = character lost on screen) ---
	player.position = Vector2(0, 1)
	frame(player.position, 1.0)
	await settle(6)
	await shoot("07a_camera_zoom_before")

	# --- 07b camera zoom AFTER (zoom 4 = cozy) ---
	frame(player.position, 4.0)
	await settle(6)
	await shoot("07b_camera_zoom_after")

	# --- 09 tiny farm: the decorated test area, trees + mushrooms ---
	player.position = Vector2(-46, 16)
	frame(Vector2(-50, -2), 6.0)
	await settle(6)
	await shoot("09_tiny_farm")

	# --- 10 final game: player standing in the finished prototype ---
	# Zoom 4 is what the article tells the reader to set, so shoot it honestly.
	player.position = Vector2(24, 12)
	frame(player.position, 4.0)
	await settle(6)
	await shoot("10_final_game")

	# --- 04 layered character: body only / hair only / combined, big ---
	await capture_layers()

	# --- flip_h diagram source: walking right vs walking left ---
	await capture_flip()

	get_tree().quit()


## Union of every decoration/crop sprite's world-space rect, using the actual
## texture size of the frame currently on screen.
func content_bounds() -> Rect2:
	var box := Rect2()
	var first := true
	for group in ["Decorations", "Crops"]:
		for n in world.get_node(group).get_children():
			var size := Vector2.ZERO
			if n is AnimatedSprite2D:
				var tex: Texture2D = n.sprite_frames.get_frame_texture(n.animation, n.frame)
				if tex:
					size = tex.get_size()
			elif n is Sprite2D and n.texture:
				size = n.texture.get_size()
			if size == Vector2.ZERO:
				continue
			# Sprites here are centered on their position.
			var r := Rect2(n.global_position - size * 0.5, size)
			box = r if first else box.merge(r)
			first = false
	return box


## Frame the whole farm with `margin` world units of breathing room on all sides.
func fit_all(margin: float) -> void:
	var box := content_bounds().grow(margin)
	var vp := Vector2(get_viewport().size)
	var z: float = minf(vp.x / box.size.x, vp.y / box.size.y)
	print("  content bounds ", box, " -> zoom ", z)
	cam.zoom = Vector2(z, z)
	cam.position = box.get_center() - player.position


## Put world-space `center` at the middle of the frame at the given zoom.
## Camera2D is a child of Player, so its position is an offset from the player.
func frame(center: Vector2, zoom: float) -> void:
	cam.zoom = Vector2(zoom, zoom)
	cam.position = center - player.position


## Advance n rendered frames so animations and the camera settle.
func settle(n: int) -> void:
	for i in n:
		await get_tree().process_frame


## Grab the viewport and write it to OUT/<name>.png.
func shoot(name: String) -> void:
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	img.save_png(out_dir + name + ".png")
	print("wrote ", name, ".png  ", img.get_width(), "x", img.get_height())


## Isolate the player against a flat backdrop for the layering shots.
func capture_layers() -> void:
	world.get_node("Decorations").visible = false
	world.get_node("Crops").visible = false
	player.position = Vector2.ZERO
	# The drawn character is only ~11x18 units inside a 96x64 frame, so these
	# isolated shots need a much closer zoom than the gameplay ones.
	cam.position = Vector2(0, -2)
	cam.zoom = Vector2(22, 22)

	# Pin to one idle frame, otherwise the three panels are grabbed at whatever
	# point the animation happens to be at and don't line up between runs.
	player.set_physics_process(false)
	player.play_character_animation("idle")
	for s in [base_sprite, hair_sprite]:
		s.pause()
		s.frame = 0

	base_sprite.visible = true
	hair_sprite.visible = false
	await settle(6)
	await shoot("04a_body_only")

	base_sprite.visible = false
	hair_sprite.visible = true
	await settle(6)
	await shoot("04b_hair_only")

	base_sprite.visible = true
	hair_sprite.visible = true
	await settle(6)
	await shoot("04c_combined")

	world.get_node("Decorations").visible = true
	world.get_node("Crops").visible = true
	cam.position = Vector2.ZERO


## Same walk animation, flipped, for the flip_h diagram.
func capture_flip() -> void:
	world.get_node("Decorations").visible = false
	world.get_node("Crops").visible = false
	player.position = Vector2.ZERO
	# The drawn character is only ~11x18 units inside a 96x64 frame, so these
	# isolated shots need a much closer zoom than the gameplay ones.
	cam.position = Vector2(0, -2)
	cam.zoom = Vector2(22, 22)

	# The player's own _physics_process sees no input and calls
	# play_character_animation("idle") every frame, which would un-pause the
	# sprites and switch them off "walk". Stop it driving them first.
	player.set_physics_process(false)

	player.play_character_animation("walk")

	# Freeze on one identical frame so the pair differs ONLY by flip_h,
	# which is the entire point of the diagram.
	for s in [base_sprite, hair_sprite]:
		s.pause()
		s.frame = 2

	base_sprite.flip_h = false
	hair_sprite.flip_h = false
	await settle(2)
	await shoot("11a_walk_right")

	base_sprite.flip_h = true
	hair_sprite.flip_h = true
	await settle(2)
	await shoot("11b_walk_left_fliph")
