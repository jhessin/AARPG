import esper
from random import uniform
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Area2DTypedArray import Area2DTypedArray

from ..components import (
    ENTITY_ID,
    HitboxComponent,
    BodyComponent,
    HealthComponent,
    KnockbackComponent,  # <-- use this now
    CameraComponent,
    CameraShakeComponent,
    avg,
    clamp,
)


class CombatSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        # Loop through all entities with hitboxes
        for attacker_ent, (hitbox, attacker_body) in esper.get_components(
            HitboxComponent, BodyComponent
        ):
            hitbox_node: Area2D = Area2D.cast(hitbox.node)

            # Skip if hitbox is disabled or missing
            if not hitbox_node or not hitbox_node.is_monitoring():
                continue

            # Query overlapping areas
            overlapping: Area2DTypedArray = hitbox_node.get_overlapping_areas()

            for i in range(overlapping.size()):
                victim_area: Area2D = Area2D.cast(overlapping.get(i))

                # Check if this area belongs to an entity
                if not victim_area.has_meta(ENTITY_ID):
                    continue

                victim_ent = int(str(victim_area.get_meta(ENTITY_ID)))

                # Don't hit yourself
                if victim_ent == attacker_ent:
                    continue

                # --- Apply Damage ---
                damage = uniform(hitbox.min_damage, hitbox.max_damage)
                knockback_force = uniform(0, hitbox.knockback_force)

                if victim_health := esper.try_component(victim_ent, HealthComponent):
                    victim_health.current -= damage

                    print(
                        f"Attacker #{attacker_ent} hits #{victim_ent} for {damage:.1f}"
                    )
                    print(
                        f"Entity #{victim_ent} HP: {victim_health.current}/{victim_health.maximum}"
                    )

                    # Camera shake
                    if camera_list := esper.get_component(CameraComponent):
                        cam_ent, _ = camera_list[0]
                        esper.add_component(
                            cam_ent,
                            CameraShakeComponent(
                                clamp(knockback_force, 0.2, hitbox.attack_duration),
                                avg(knockback_force, damage),
                            ),
                        )

                # --- Apply Knockback ---
                victim_body = esper.try_component(victim_ent, BodyComponent)
                if victim_body and not victim_body.body.is_queued_for_deletion():
                    diff = (
                        victim_body.body.global_position
                        - attacker_body.body.global_position
                    )

                    direction = diff.normalized()

                    # Ensure victim has a KnockbackComponent
                    knock = esper.try_component(victim_ent, KnockbackComponent)
                    if not knock:
                        knock = KnockbackComponent()
                        esper.add_component(victim_ent, knock)

                    knock.force = direction * knockback_force

                # Disable hitbox until next attack
                hitbox_node.call_deferred("set_monitoring", False)
