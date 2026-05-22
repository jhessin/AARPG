import esper
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot import gdclass

from ECS.components import (
    AnimationComponent,
    BodyComponent,
    HealthComponent,
    IsPlayer,
    VelocityComponent,
    StateComponent,
)


@gdclass
class Player(CharacterBody2D):
    sprite: Sprite2D
    animator: AnimationPlayer
    _entity: int

    def _ready(self) -> None:
        self.sprite = self.get_node("Sprite2D")
        self.animator = self.get_node("AnimationPlayer")

        self._entity = esper.create_entity(
            HealthComponent(),
            VelocityComponent(),
            IsPlayer(),
            AnimationComponent(self.animator, self.sprite),
            BodyComponent(self),
            StateComponent(),
        )
        print(f"Player initialized as entity #{self._entity}")
