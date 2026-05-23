import esper
from py4godot.classes.core import Vector2
from py4godot.classes.CharacterBody2D import CharacterBody2D

from ECS.components import BodyComponent, PlayerState, StateComponent, VelocityComponent


class MovementSystem(esper.Processor):
    def process(self, delta: float) -> None:
        for ent, (vel, body_comp) in esper.get_components(
            VelocityComponent, BodyComponent
        ):

            if state := esper.try_component(ent, StateComponent):
                if state.current == PlayerState.ATTACK:
                    vel.x -= vel.x * state.decelerate_speed * delta
                    vel.y -= vel.y * state.decelerate_speed * delta

            if isinstance(body_comp.body, CharacterBody2D):
                body_comp.body.velocity = Vector2.new3(vel.x, vel.y) * vel.speed

                body_comp.body.move_and_slide()
            else:
                vel.x = 0.0
                vel.y = 0.0
