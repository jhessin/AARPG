class_name MovementSystem
extends System


func query() -> QueryBuilder:
	return q.with_all([VelocityComponent, IsPlayer])


func process(entities: Array[Entity], _components: Array, _delta: float) -> void:
	for entity in entities:
		var vel_comp: VelocityComponent = entity.get_component(VelocityComponent) as VelocityComponent
		var player_comp: IsPlayer = entity.get_component(IsPlayer) as IsPlayer

		if vel_comp and player_comp:
			player_comp.model.velocity = vel_comp.direction * vel_comp.speed
			player_comp.model.move_and_slide()
