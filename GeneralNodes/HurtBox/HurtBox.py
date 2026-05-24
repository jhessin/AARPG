# from py4godot.methods import private
# from py4godot.signals import signal, SignalArg
from typing import Optional
from py4godot.classes import gdclass

# from py4godot.classes.core import Vector3
from py4godot.classes.Area2D import Area2D

from ECS.components import HurtboxComponent


@gdclass
class HurtBox(Area2D):

    def __init__(self):
        super().__init__()
        self.component: Optional[HurtboxComponent] = None

    def _ready(self) -> None:
        self.component = HurtboxComponent(self)
        # put initialization code here
