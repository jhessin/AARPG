import esper
from random import uniform
from py4godot.classes.core import Vector2

from ..components import *


class CameraSystem(esper.Processor):
    def process(self, delta: float) -> None:
        # Get the camera entity (there should only be one)
        for cam_ent, cam_comp in esper.get_component(CameraComponent):
            camera = cam_comp.camera
            tilemap = cam_comp.tile_map

            # Find the player (or any entity with a BodyComponent marked as player)
            target_pos: Vector2 | None = None
            for _, (body, *_) in esper.get_components(BodyComponent, PlayerComponent):
                target_pos = body.body.global_position
                break

            if target_pos is None:
                return  # No player yet

            # --- Smooth follow ---
            cam_pos = camera.global_position
            desired = target_pos + cam_comp.offset
            smoothed = cam_pos.lerp(desired, cam_comp.smoothing)

            # --- Camera shake ---
            shake = esper.try_component(cam_ent, CameraShakeComponent)
            if shake:
                smoothed += Vector2.new3(
                    shake.intensity * uniform(-1.0, 1.0),
                    shake.intensity * uniform(-1.0, 1.0),
                )
                shake.duration -= delta
                if shake.duration <= 0:
                    esper.remove_component(cam_ent, CameraShakeComponent)

            # --- Clamp to tilemap bounds ---
            rect = tilemap.get_used_rect()
            cell_size = tilemap.tile_set.tile_size

            map_min = Vector2.new3(
                rect.position.x * cell_size.x, rect.position.y * cell_size.y
            )
            map_max = Vector2.new3(
                (rect.position.x + rect.size.x) * cell_size.x,
                (rect.position.y + rect.size.y) * cell_size.y,
            )

            half_screen = cam_comp.half_screen_size

            clamped = Vector2.new3(
                max(
                    map_min.x + half_screen.x,
                    min(smoothed.x, map_max.x - half_screen.x),
                ),
                max(
                    map_min.y + half_screen.y,
                    min(smoothed.y, map_max.y - half_screen.y),
                ),
            )

            # Apply final camera position
            camera.global_position = clamped
