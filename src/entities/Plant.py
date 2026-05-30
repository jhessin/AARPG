import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Area2D import Area2D

from ..components import *


@gdclass
class Plant(Node2D):
    hurtbox: Area2D
    health: float = 1

    def _ready(self) -> None:
        if not self.hurtbox:
            self.hurtbox = self.get_node("%HurtBox")

        body = BodyComponent(self)
        vel = VelocityComponent()
        health = HealthComponent(self.health)
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            health,
            hurtbox,
            vel,
        )

        body.bind_entity(ent)
        health.bind_entity(ent)
        hurtbox.bind_entity(ent)
        vel.bind_entity(ent)

        self.entity = ent
