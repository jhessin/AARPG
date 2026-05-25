# from py4godot.methods import private

# from py4godot.signals import signal, SignalArg
from typing import Optional
from py4godot.classes import gdclass

# from py4godot.classes.core import Vector3
from py4godot.classes.Area2D import Area2D

from ECS.components import HitboxComponent, clamp


@gdclass
class HitBox(Area2D):

    min_damage: float = 10.0
    max_damage: float = 20.0
    knockback_force: float = 500.0

    def __init__(self):
        super().__init__()
        self.component: Optional[HitboxComponent] = None

    def _ready(self) -> None:
        self.min_damage = max(self.min_damage, 1.0)
        self.max_damage = max(self.min_damage, self.max_damage)
        self.knockback_force = clamp(self.knockback_force, 0.1, 1000.0)
        self.component = HitboxComponent(
            self, self.min_damage, self.max_damage, self.knockback_force
        )
