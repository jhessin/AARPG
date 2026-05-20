import esper
from py4godot.classes.Input import Input
from ..components import IsPlayer, VelocityComponent


class InputSystem(esper.Processor):
    def process(self, _: float) -> None:
        for _, (vel, __) in esper.get_components(VelocityComponent, IsPlayer):
            del __
            if vel:
                vel.x = Input.instance().get_action_strength(
                    "right"
                ) - Input.instance().get_action_strength("left")
                vel.y = Input.instance().get_action_strength(
                    "down"
                ) - Input.instance().get_action_strength("up")
