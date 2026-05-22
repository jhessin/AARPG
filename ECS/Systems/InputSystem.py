import esper
from py4godot.classes.Input import Input
from py4godot.classes.Node import Vector2

from ..components import IsPlayer, PlayerState, StateComponent, VelocityComponent


class InputSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        input_manager = Input.instance()
        for _, (vel, state, *_) in esper.get_components(
            VelocityComponent, StateComponent, IsPlayer
        ):
            move: Vector2 = Vector2.new3(
                input_manager.get_action_strength("right")
                - input_manager.get_action_strength("left"),
                input_manager.get_action_strength("down")
                - input_manager.get_action_strength("up"),
            )

            length = move.length()
            print(length)
            move = move.normalized()
            if vel:
                vel.x = move.x
                vel.y = move.y

            if length > 0.0:
                if state.current == PlayerState.IDLE:
                    state.previous = state.current
                    state.current = PlayerState.WALK
            else:
                if state.current == PlayerState.WALK:
                    state.previous = state.current
                    state.current = PlayerState.IDLE
