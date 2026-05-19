class_name MovementSystem
extends System


func query() -> QueryBuilder:
	return q.with_all([VelocityComponent, BodyComponent])


func process(entities: Array[Entity], _components: Array, _delta: float) -> void:
	for entity in entities:
		var vel_comp: VelocityComponent = entity.get_component(VelocityComponent) as VelocityComponent
		var body_comp: BodyComponent = entity.get_component(BodyComponent) as BodyComponent

		if vel_comp and body_comp:
			body_comp.body.velocity = vel_comp.direction * vel_comp.speed
			body_comp.body.move_and_slide()
