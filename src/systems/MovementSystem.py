import esper
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.core import Vector2

from components import (
    VelocityComponent,
    KnockbackComponent,
    BodyComponent,
    FacingComponent,
    StateComponent,
    AttackSlowComponent,
    State,
)


class MovementSystem(esper.Processor):
    def process(self, delta: float) -> None:
        for ent, (vel, body_comp) in esper.get_components(
            VelocityComponent, BodyComponent
        ):
            body = body_comp.body

            if body.is_queued_for_deletion():
                continue

            multiplier: float = 1.0

            # Attack slow or freeze
            state = esper.try_component(ent, StateComponent)
            if state and state.current == State.ATTACK:
                slow = esper.try_component(ent, AttackSlowComponent)
                multiplier *= slow.factor if slow else 0.0

            # Base movement
            movement: Vector2 = vel.total_vel * multiplier

            # Facing update (intentional movement only)
            if movement.length() > 0:
                facing = esper.try_component(ent, FacingComponent)
                if facing:
                    facing.set_from_vector(movement)

            # Knockback
            knock = esper.try_component(ent, KnockbackComponent)
            if knock:
                movement += knock.force
                knock.force -= knock.force * knock.decay * delta

            # Apply movement
            if isinstance(body, CharacterBody2D):
                body.velocity = movement
                body.move_and_slide()
            else:
                displacement: Vector2 = movement * delta
                body.global_position += displacement
