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
            # Get the input data from the user.
            move: Vector2 = Vector2.new3(
                input_manager.get_axis("left", "right"),
                input_manager.get_axis("up", "down"),
            ).normalized()

            # Set the velocity direction of the player
            if vel:
                vel.x = move.x
                vel.y = move.y

            # Update the player state
            if move.length() > 0.0:
                if state.current == PlayerState.IDLE:
                    state.previous = state.current
                    state.current = PlayerState.WALK
            else:
                if state.current == PlayerState.WALK:
                    state.previous = state.current
                    state.current = PlayerState.IDLE

            # update the facing of the player
            if move.length() == 0.0:
                pass
            elif move.y == 0:
                state.cardinal_direction = Vector2.LEFT if move.x < 0 else Vector2.RIGHT
            elif move.x == 0:
                state.cardinal_direction = Vector2.UP if move.y < 0 else Vector2.DOWN
