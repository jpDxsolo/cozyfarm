extends CharacterBody2D

@export var speed := 100.0

@onready var base_sprite = $BaseSprite
@onready var hair_sprite = $HairSprite

func _ready():
	play_character_animation("idle")

func _physics_process(delta: float):
	var direction = Input.get_vector("move_left","move_right","move_up","move_down")
	
	velocity = direction * speed
	move_and_slide()
	
	update_animation(direction)

func play_character_animation(name: StringName) :
	if base_sprite.animation != name:
		base_sprite.play(name)
	
	if hair_sprite.animation != name:
		hair_sprite.play(name)
		

func update_animation(direction):
	if direction != Vector2.ZERO:
		
		if direction.x < 0 :
			base_sprite.flip_h = true
			hair_sprite.flip_h = true
		
		elif direction.x > 0 :
			base_sprite.flip_h = false
			hair_sprite.flip_h = false
			
		play_character_animation("walk")
	else:
		play_character_animation("idle")
