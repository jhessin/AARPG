import esper

# from py4godot.methods import private
# from py4godot.signals import signal, SignalArg
# from py4godot.classes.core import Vector3
from py4godot.classes import gdclass
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Node2D import Node2D

from ECS.components import (
    # BodyComponent,
    ENTITY_ID,
    HealthComponent,
    HurtboxComponent,
    # VelocityComponent,
)
from GeneralNodes.HurtBox.HurtBox import HurtBox


@gdclass
class Plant(Node2D):
    def __init__(self):
        super().__init__()
        self.entity = -1

    def _ready(self) -> None:
        # hurt_box_node: HurtBox = self.get_node("HurtBox").get_pyscript()
        raw_hurtbox = self.get_node("HurtBox")
        hurtbox_area2d = Area2D.cast(raw_hurtbox)
        unique_hurtbox_comp = HurtboxComponent(hurtbox_area2d)
        unique_health_comp = HealthComponent(self, maximum=1.0)

        self.entity = esper.create_entity(
            unique_hurtbox_comp,
            unique_health_comp,
            # BodyComponent(self),
            # VelocityComponent(0.0, 0.0)
        )

        self.set_meta(ENTITY_ID, str(self.entity))
        raw_hurtbox.set_meta(ENTITY_ID, str(self.entity))

        print(f"Stamped Godot C++ Node with absolute Entity ID: #{self.entity}")
