import esper
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Engine import Engine
from py4godot.classes.SceneTree import SceneTree
from ..components import (
    BodyComponent,
    HitboxComponent,
    HurtboxComponent,
    HealthComponent,
    VelocityComponent,
)


class CombatSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        # Loop through any entities with active attacking weapon components
        for attacker_ent, (hitbox, attacker_body) in esper.get_components(
            HitboxComponent, BodyComponent
        ):
            # Access the node tracking property saved inside the component data
            hitbox_node: Area2D = Area2D.cast(hitbox.node)

            if not hitbox_node or not hitbox_node.is_monitoring():
                continue

            # Query overlapping vectors natively
            overlapping_areas = hitbox_node.get_overlapping_areas()

            for i in range(overlapping_areas.size()):
                victim_area_node: Area2D = Area2D.cast(overlapping_areas.get(i))

                # Grab all entities that have a hurtbox component
                for victim_ent, hurtbox in esper.get_component(HurtboxComponent):
                    hurtbox_node = Area2D.cast(overlapping_areas.get(i))

                    # Check if the Area2D nodes match
                    if (
                        hurtbox_node.get_instance_id()
                        == victim_area_node.get_instance_id()
                    ):
                        if attacker_ent == victim_ent:
                            continue

                        # Apply Damage
                        if victim_health := esper.try_component(
                            victim_ent, HealthComponent
                        ):
                            # process health stuff here
                            victim_health.current -= hitbox.damage
                            print(
                                f"Entity #{victim_ent} damaged by #{attacker_ent}! HP: {victim_health.current}/{victim_health.maximum}"
                            )

                        # Apply knockback direction vectors
                        if (
                            victim_body := esper.try_component(
                                victim_ent, BodyComponent
                            )
                        ) and (
                            victim_vel := esper.try_component(
                                victim_ent, VelocityComponent
                            )
                        ):
                            diff = (
                                victim_body.body.global_position
                                - attacker_body.body.global_position
                            )
                            dir_vector = diff.normalized()

                            victim_vel.x = dir_vector.x * hitbox.knockback_force
                            victim_vel.y = dir_vector.y * hitbox.knockback_force

                        hitbox_node.set_deferred("monitoring", False)

        # # --- ENGINE PROBE TRACKER ---
        # raw_loop = Engine.instance().get_main_loop()
        # if raw_loop:
        #     # Cast the generic MainLoop up to its true running type: SceneTree
        #     scene_tree = SceneTree.cast(raw_loop)
        #     player_nodes = scene_tree.get_nodes_in_group("Player")
        #
        #     for i in range(player_nodes.size()):
        #         player_node = player_nodes.get(i)
        #         if hitbox_node := player_node.get_node("HitBox"):
        #             hitbox_area = Area2D.cast(hitbox_node)
        #
        #             # Print properties directly to pinpoint the failure
        #             print(
        #                 f"[DEBUG] Hitbox Monitoring: {hitbox_area.is_monitoring()} | Mask: {hitbox_area.get_collision_mask()}"
        #             )
        #
        #             overlaps = hitbox_area.get_overlapping_areas()
        #             print(
        #                 f"[DEBUG] Active Area Overlaps detected by Godot: {overlaps.size()}"
        #             )
        # # --- ENGINE PROBE TRACKER ---
