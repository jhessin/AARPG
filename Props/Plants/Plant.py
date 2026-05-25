import esper

from py4godot.classes import gdclass
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Node2D import Node2D

from ECS.components import (
    BodyComponent,
    ENTITY_ID,
    HealthComponent,
    VelocityComponent,
)


@gdclass
class Plant(Node2D):
    starting_health: float = 1.0

    def __init__(self):
        super().__init__()
        self.entity: int = -1

    def _ready(self) -> None:
        # hurt_box_node: HurtBox = self.get_node("HurtBox").get_pyscript()
        self.starting_health = max(self.starting_health, 1.0)
        raw_hurtbox = self.get_node("HurtBox")
        hurt_box: Area2D = Area2D.cast(raw_hurtbox)
        unique_health_comp = HealthComponent(self, maximum=self.starting_health)

        self.entity = esper.create_entity(
            unique_health_comp,
            BodyComponent(self),
            VelocityComponent(),
        )

        # Stamp the entity ID on the hurtbox component
        self.set_meta(ENTITY_ID, str(self.entity))
        hurt_box.set_meta(ENTITY_ID, str(self.entity))

        self.add_to_group("Enemy")
