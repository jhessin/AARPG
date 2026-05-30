from random import randint
import esper


from py4godot.classes.core import Vector2

from ..components import *

KNOCKBACK_SPEED = 200.0


class SimpleAISystem(esper.Processor):
    def process(self, delta: float) -> None:

        # Loop through simple AI enemies
        for ent, (ai, vel) in esper.get_components(
            SimpleAIComponent, VelocityComponent
        ):
            ai.tick(delta)

            # Simple State Logic
            match ai.state:
                case AIState.IDLE:
                    vel.direction = Vector2.ZERO
                    if ai.time_in_state > ai.timer:
                        ai.state = AIState.WANDER
                case AIState.WANDER:
                    direction = randint(0, 3)
                    if vel.direction == Vector2.ZERO:
                        vel.direction = FACINGS[direction]
                    if ai.time_in_state > ai.timer:
                        ai.state = AIState.IDLE
                case AIState.STUN:
                    if anim := esper.try_component(ent, AnimationEventComponent):
                        if anim.finished:
                            ai.state = AIState.IDLE
                            esper.remove_component(ent, AnimationEventComponent)
