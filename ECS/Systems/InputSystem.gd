class_name InputSystem
extends System


func query() -> QueryBuilder:
	return q.with_all(
		[
			IsPlayer,
			VelocityComponent,
		],
	)


func process(entities: Array[Entity], _components: Array, _delta: float) -> void:
	for entity in entities:
		var v_comp: VelocityComponent = entity.get_component(VelocityComponent) as VelocityComponent

		if v_comp:
			# v_comp.direction = Input.get_vector('left', 'right', 'up', 'down')
			v_comp.direction.x = Input.get_action_strength('right') - Input.get_action_strength('left')
			v_comp.direction.y = Input.get_action_strength('down') - Input.get_action_strength('up')
