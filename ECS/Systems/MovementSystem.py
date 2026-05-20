import esper
from py4godot.classes.core import Vector2

from ECS.components import BodyComponent, VelocityComponent


class MovementSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for _ent, (vel, body_comp) in esper.get_components(
            VelocityComponent, BodyComponent
        ):
            del _ent

            if vel and body_comp:
                body_comp.body.velocity = Vector2.new3(vel.x, vel.y) * vel.speed
                body_comp.body.move_and_slide()
