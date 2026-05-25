import math
import esper

from random import random, uniform

from py4godot.classes.core import Vector2
from ECS.components import IDLE, BodyComponent, State, StateComponent, VelocityComponent

MIN_STATE_TIME = 2.0
MAX_STATE_TIME = 5.0


class AISystem(esper.Processor):
    def process(self, delta: float) -> None:
        for _, (state, vel, body) in esper.get_components(
            StateComponent, VelocityComponent, BodyComponent
        ):
            if not state or not vel or not body or body.body.is_queued_for_deletion():
                continue

            state.time_in_state += delta

            if state.time_in_state > uniform(MIN_STATE_TIME, MAX_STATE_TIME):
                match state.current:
                    case State.IDLE:
                        move: Vector2 = Vector2.from_angle(
                            random() * math.tau
                        ).normalised()
                        print(f"AISystem is moving: {move}")
                        print(f"AISystem is moving.length: {move.length()}")
                        state.cardinal_direction = vel.direction = move
                        state.current = State.WALK
                    case State.WALK:
                        print("AISystem is stopping")
                        state.cardinal_direction = vel.direction = Vector2.ZERO
                        state.current = State.IDLE
                    case _:
                        state.current = State.IDLE
