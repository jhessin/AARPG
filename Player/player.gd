class_name Player
extends Entity

var cardinal_direction: Vector2 = Vector2.DOWN
var state: String = 'idle'

@onready var character: CharacterBody2D = $CharacterBody2D
@onready var sprite: Sprite2D = $CharacterBody2D/Sprite2D
@onready var animator: AnimationPlayer = $CharacterBody2D/AnimationPlayer


func define_components() -> Array:
	var anim_comp: AnimationComponent = AnimationComponent.new(animator, sprite)
	return [
		HealthComponent.new(100),
		VelocityComponent.new(100.0),
		IsPlayer.new(),
		anim_comp,
	]
