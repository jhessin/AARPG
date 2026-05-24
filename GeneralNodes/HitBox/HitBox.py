# from py4godot.methods import private

# from py4godot.signals import signal, SignalArg
from typing import Optional
from py4godot.classes import gdclass

# from py4godot.classes.core import Vector3
from py4godot.classes.Area2D import Area2D

from ECS.components import HitboxComponent


@gdclass
class HitBox(Area2D):

    damage: float = 10.0
    knockback_force: float = 300.0

    def __init__(self):
        super().__init__()
        self.component: Optional[HitboxComponent] = None

    def _ready(self) -> None:
        self.component = HitboxComponent(self, self.damage, self.knockback_force)
