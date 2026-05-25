import esper
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.methods import private
from py4godot.signals import signal, SignalArg
from py4godot.classes import gdclass
from py4godot.classes.core import Vector3
from py4godot.classes.CharacterBody2D import CharacterBody2D

from ECS.components import (
    ENTITY_ID,
    AnimationComponent,
    BodyComponent,
    EnemyComponent,
    StateComponent,
    VelocityComponent,
)


@gdclass
class Enemy(CharacterBody2D):

    def _ready(self) -> None:
        animator: AnimationPlayer = self.get_node("%Animator")
        sprite: Sprite2D = self.get_node("%Sprite")

        self.entity = esper.create_entity(
            StateComponent(),
            AnimationComponent(animator, sprite),
            VelocityComponent(speed=50),
            BodyComponent(self),
            EnemyComponent(self, 10.0),
        )

        self.set_meta(ENTITY_ID, str(self.entity))
        sprite.set_meta(ENTITY_ID, str(self.entity))

        self.add_to_group("Enemy")
