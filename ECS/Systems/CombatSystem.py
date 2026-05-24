import esper
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Area2DTypedArray import Area2DTypedArray
from ..components import (
    ENTITY_ID,
    BodyComponent,
    HitboxComponent,
    HealthComponent,
    HurtboxComponent,
    VelocityComponent,
)


class CombatSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        # Not using delta so we can safely delete it for now.
        del _delta

        # Loop through any entities with active attacking weapon components this requires a hitbox and a body
        for attacker_ent, (hitbox, attacker_body) in esper.get_components(
            HitboxComponent, BodyComponent
        ):
            # Access the node tracking property saved inside the component data
            hitbox_node: Area2D = Area2D.cast(hitbox.node)

            # Check if we have already hit something or we are not attacking
            if not hitbox_node or not hitbox_node.is_monitoring():
                continue

            # Query overlapping vectors natively
            overlapping_areas: Area2DTypedArray = hitbox_node.get_overlapping_areas()

            # Loop through each area that was hit.
            for i in range(overlapping_areas.size()):
                victim_area_node: Area2D = Area2D.cast(overlapping_areas.get(i))

                # Check for a hurtbox component
                if victim_area_node.has_meta(ENTITY_ID):
                    victim_ent = int(str(victim_area_node.get_meta(ENTITY_ID)))

                    # If our victim doesn't have a hurtbox these aren't the
                    # droids we are looking for 😁.
                    if not esper.has_component(victim_ent, HurtboxComponent):
                        continue

                    # Do not attack yourself
                    if attacker_ent == victim_ent:
                        continue

                    # Apply Damage
                    if victim_health := esper.try_component(
                        victim_ent, HealthComponent
                    ):
                        # process health stuff here
                        victim_health.current -= hitbox.damage

                    # Apply knockback direction if the victim has a body and
                    # VelocityComponent
                    if (
                        victim_body := esper.try_component(victim_ent, BodyComponent)
                    ) and (
                        victim_vel := esper.try_component(victim_ent, VelocityComponent)
                    ):
                        diff = (
                            victim_body.body.global_position
                            - attacker_body.body.global_position
                        )
                        dir_vector = diff.normalized()

                        victim_vel.x = dir_vector.x * hitbox.knockback_force
                        victim_vel.y = dir_vector.y * hitbox.knockback_force

                    # Disable the hitbox node until the next attack
                    hitbox_node.call_deferred("set_monitoring", False)
