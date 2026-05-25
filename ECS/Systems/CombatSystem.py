import esper
import math
from random import uniform
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Area2DTypedArray import Area2DTypedArray
from ..components import (
    ENTITY_ID,
    BodyComponent,
    CameraComponent,
    CameraShakeComponent,
    HitboxComponent,
    HealthComponent,
    VelocityComponent,
    avg,
    clamp,
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

                    # Do not attack yourself
                    if attacker_ent == victim_ent:
                        continue

                    # Apply Damage
                    damage_taken = uniform(hitbox.min_damage, hitbox.max_damage)
                    knockback_applied = uniform(0, hitbox.knockback_force)
                    if victim_health := esper.try_component(
                        victim_ent, HealthComponent
                    ):
                        # process health stuff here
                        victim_health.current -= damage_taken

                        # Shake the camera here
                        if camera_list := esper.get_component(CameraComponent):
                            camera_ent, _ = camera_list[0]

                            esper.add_component(
                                camera_ent,
                                CameraShakeComponent(
                                    clamp(
                                        knockback_applied, 0.2, hitbox.attack_duration
                                    ),
                                    avg(knockback_applied, damage_taken),
                                ),
                            )

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
                        if victim_body.body.is_queued_for_deletion():
                            return

                        victim_vel.x = dir_vector.x * hitbox.knockback_force
                        victim_vel.y = dir_vector.y * hitbox.knockback_force

                    # Disable the hitbox node until the next attack
                    hitbox_node.call_deferred("set_monitoring", False)
