import esper
from py4godot.classes.Input import Input
from py4godot.classes.Node import Vector2

from ..components import (
    ATTACK,
    DIR_4,
    InputComponent,
    IsPlayer,
    PlayerState,
    StateComponent,
    VelocityComponent,
)
import math


class InputSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        input_manager = Input.instance()
        for _, (vel, state, input_q, *_) in esper.get_components(
            VelocityComponent, StateComponent, InputComponent, IsPlayer
        ):
            state.time_in_state += _delta

            # Get the input data from the user.
            move: Vector2 = Vector2.new3(
                input_manager.get_axis("left", "right"),
                input_manager.get_axis("up", "down"),
            ).normalized()

            # Check if I'm already attacking
            if state.current == PlayerState.ATTACK:
                move.x = move.y = 0.0
                input_q.queue.clear()  # don't queue any more attacks
                continue  # skip directional evaluations until the attack finishes

            # Check for discrete attack intent
            has_attacked = False
            for event in input_q.queue:
                if event.is_action_pressed(ATTACK):
                    has_attacked = True
                    break
            input_q.queue.clear()  # clean evnt buffer for this frame

            if has_attacked:
                state.previous = state.current
                state.current = PlayerState.ATTACK
                state.time_in_state = 0.0
                continue  # Instantly switch states

            # Set the velocity direction of the player
            if vel:
                vel.x = move.x
                vel.y = move.y

            # Update the player state
            if move.length() > 0.0:
                if state.current == PlayerState.IDLE:
                    state.previous = state.current
                    state.current = PlayerState.WALK
                    state.time_in_state = 0.0
            else:
                if state.current == PlayerState.WALK:
                    state.previous = state.current
                    state.current = PlayerState.IDLE
                    state.time_in_state = 0.0

            # update the facing of the player
            if move.length() == 0.0:
                pass
            else:
                # raw_angle = move.angle()
                direction_id: int = int(round((move.angle() / math.tau * len(DIR_4))))
                state.cardinal_direction = DIR_4[direction_id]
