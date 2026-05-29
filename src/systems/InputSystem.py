import esper
from py4godot.classes.Input import Input

from ..components import InputComponent


class InputSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        input = Input.instance()

        for _, input_comp in esper.get_component(InputComponent):

            # ---------------------------------------------------------
            # 1. Movement (uses Godot action map)
            # ---------------------------------------------------------
            vec = input.get_vector(
                "left",
                "right",
                "up",
                "down",
            )

            input_comp.move_x = vec.x
            input_comp.move_y = vec.y

            # ---------------------------------------------------------
            # 2. Attack
            # ---------------------------------------------------------
            input_comp.attack = input.is_action_pressed("attack")

            # ---------------------------------------------------------
            # 3. Dash
            # ---------------------------------------------------------
            # input_comp.dash = input.is_action_pressed("dash")

            # ---------------------------------------------------------
            # 4. Interact
            # ---------------------------------------------------------
            # input_comp.interact = input.is_action_pressed("interact")
