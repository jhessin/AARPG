import esper

# from py4godot.methods import private
# from py4godot.signals import signal, SignalArg
# from py4godot.classes.core import Vector3
from py4godot.classes import gdclass
from py4godot.classes.Node2D import Node2D

from ECS.components import (
    # BodyComponent,
    HealthComponent,
    # VelocityComponent,
)
from GeneralNodes.HurtBox.HurtBox import HurtBox


@gdclass
class Plant(Node2D):
    def _ready(self) -> None:
        hurt_box_node: HurtBox = self.get_node("HurtBox").get_pyscript()
        self.entity = esper.create_entity(
            hurt_box_node.component,
            HealthComponent(self, maximum=1.0),
            # BodyComponent(self),
            # VelocityComponent(0.0, 0.0)
        )
