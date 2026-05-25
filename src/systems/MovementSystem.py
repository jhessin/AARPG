import esper
from py4godot.classes.Node2D import Node2D
from py4godot.classes.core import Vector2
from py4godot.classes.CharacterBody2D import CharacterBody2D

from ..components import BodyComponent, State, StateComponent, VelocityComponent


class MovementSystem(esper.Processor):
    def process(self, delta: float) -> None:
        for ent, (vel, body_comp) in esper.get_components(
            VelocityComponent, BodyComponent
        ):
            # Don't touch dead things!
            if body_comp.body.is_queued_for_deletion():
                continue

            if state := esper.try_component(ent, StateComponent):
                if state.current == State.ATTACK:
                    vel.direction -= vel.direction * state.decelerate_speed * delta

            if isinstance(body_comp.body, CharacterBody2D):
                # delta slows my player to a crawl for some reason.
                body_comp.body.velocity = vel.total_vel  # * delta

                body_comp.body.move_and_slide()
            elif isinstance(body_comp.body, Node2D):
                # Calculate displacement
                displacement = vel.total_vel * delta

                # Apply velocity
                cur_pos = body_comp.body.global_position
                body_comp.body.global_position = Vector2.new3(
                    cur_pos.x + displacement.x,
                    cur_pos.y + displacement.y,
                )

            # apply friction to knockback effect afterward
            FRICTION_COEFFICIENT = 10.0
            vel.knockback *= max(0.0, 1.0 - FRICTION_COEFFICIENT * delta)

