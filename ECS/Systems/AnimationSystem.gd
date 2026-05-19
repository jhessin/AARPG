class_name AnimationSystem
extends System

var state: String = 'walk'
var cardinal_direction: Vector2 = Vector2.DOWN
var direction: Vector2 = Vector2.DOWN
var anim_comp: AnimationComponent


func query() -> QueryBuilder:
	return q.with_all([VelocityComponent, AnimationComponent])


func process(entities: Array[Entity], _components: Array, _delta: float) -> void:
	for e in entities:
		anim_comp = e.get_component(AnimationComponent) as AnimationComponent
		var vel_comp: VelocityComponent = e.get_component(VelocityComponent) as VelocityComponent

		if vel_comp and anim_comp:
			direction = vel_comp.direction
			if _update_state() and _update_direction():
				anim_comp.animator.play(state + '_' + _anim_direction())


func _update_state() -> bool:
	var new_state: String = 'idle' if direction == Vector2.ZERO else 'walk'
	if state == new_state:
		return false
	state = new_state
	return true


func _update_direction() -> bool:
	return true


func _anim_direction() -> String:
	if cardinal_direction == Vector2.DOWN:
		return 'down'
	elif cardinal_direction == Vector2.UP:
		return 'up'
	else:
		return 'side'
