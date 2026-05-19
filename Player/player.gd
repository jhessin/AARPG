class_name Player
extends Entity

var cardinal_direction: Vector2 = Vector2.DOWN
var state: String = 'idle'

@onready var character: CharacterBody2D = $CharacterBody2D
@onready var sprite: Sprite2D = $CharacterBody2D/Sprite2D
@onready var animator: AnimationPlayer = $CharacterBody2D/AnimationPlayer


# func _process(_delta: float) -> void:
# 	var mov: VelocityComponent = get_component(VelocityComponent) as VelocityComponent
# 	var anim_comp: AnimationComponent = get_component(AnimationComponent) as AnimationComponent
#
# 	if mov:
# 		character.velocity = mov.direction * mov.speed
#
# 	if anim_comp:
# 		animator.play(anim_comp.animation_name)
# func _physics_process(_delta: float) -> void:
# 	character.move_and_slide()
func on_ready() -> void:
	var is_char: IsPlayer = IsPlayer.new()
	var anim_comp: AnimationComponent = AnimationComponent.new(animator)

	is_char.model = character
	add_component(anim_comp)
	add_component(is_char)


func define_components() -> Array:
	return [
		HealthComponent.new(100),
		VelocityComponent.new(100.0),
	]
