import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Area2D import Area2D

from components import (
    BodyComponent,
    HealthComponent,
    HurtboxComponent,
)


@gdclass
class Plant(Node2D):
    hurtbox: Area2D

    def _ready(self) -> None:
        body = BodyComponent(self)
        health = HealthComponent(10)
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            health,
            hurtbox,
        )

        body.bind_entity(ent)
        health.bind_entity(ent)
        hurtbox.bind_entity(ent)

        self.entity = ent
