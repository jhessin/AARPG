import esper
from py4godot.classes.Node2D import Node2D
from py4godot.classes.core import Vector2
from py4godot.classes.CharacterBody2D import CharacterBody2D

from ECS.components import BodyComponent, State, StateComponent, VelocityComponent


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
                    vel.x -= vel.x * state.decelerate_speed * delta
                    vel.y -= vel.y * state.decelerate_speed * delta

            if isinstance(body_comp.body, CharacterBody2D):
                body_comp.body.velocity = Vector2.new3(vel.x, vel.y) * vel.speed

                body_comp.body.move_and_slide()
            elif isinstance(body_comp.body, Node2D):
                # Calculate displacement
                displacement_x = vel.x * delta
                displacement_y = vel.y * delta

                # Apply velocity
                cur_pos = body_comp.body.global_position
                body_comp.body.global_position = Vector2.new3(
                    cur_pos.x + displacement_x,
                    cur_pos.y + displacement_y,
                )

                # apply friction
                FRICTION_COEFFICIENT = 10.0
                vel.x -= vel.x * FRICTION_COEFFICIENT * delta
                vel.y -= vel.y * FRICTION_COEFFICIENT * delta

                if abs(vel.x) < 1.0:
                    vel.x = 0.0
                if abs(vel.y) < 1.0:
                    vel.y = 0.0
