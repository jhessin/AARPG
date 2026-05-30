import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Area2D import Area2D

from ..components import *


@gdclass
class Plant(Node2D):
    hurtbox: Area2D
    health: int = 1

    def _ready(self) -> None:
        if not self.hurtbox:
            self.hurtbox = self.get_node("%HurtBox")

        body = BodyComponent(self)
        health = HealthComponent(self.health)
        hurtbox = HurtboxComponent(self.hurtbox)
        anim = AnimationComponent(self.get_node("%Animator"))
        simple = SimpleAIComponent()

        ent = esper.create_entity(
            body,
            health,
            hurtbox,
            anim,
            simple,
        )

        body.bind_entity(ent)
        health.bind_entity(ent)
        hurtbox.bind_entity(ent)
        anim.bind_entity(ent)
        simple.bind_entity(ent)

        self.entity = ent
