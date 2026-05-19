class_name MovementSystem
extends System


func query() -> QueryBuilder:
	return q.with_all([VelocityComponent, AnimationComponent])


func process(entities: Array[Entity], _components: Array, _delta: float) -> void:
	for entity in entities:
		var vel_comp: VelocityComponent = entity.get_component(VelocityComponent) as VelocityComponent
		var anim_comp: AnimationComponent = entity.get_component(AnimationComponent) as AnimationComponent

		if vel_comp and anim_comp:
			anim_comp.model.velocity = vel_comp.direction * vel_comp.speed
			anim_comp.model.move_and_slide()
