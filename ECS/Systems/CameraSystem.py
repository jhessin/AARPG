import random
import esper
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.core import Vector2
from py4godot.classes.TileMapLayer import TileMapLayer

from ECS.components import (
    BodyComponent,
    CameraComponent,
    CameraShakeComponent,
    PlayerComponent,
)


class CameraSystem(esper.Processor):
    def process(self, delta: float) -> None:

        camera_list = esper.get_component(CameraComponent)
        if not camera_list:
            return

        cam_ent, cam_comp = camera_list[0]

        if not cam_comp.is_active or not cam_comp.camera or not cam_comp.tile_map:
            return

        # Set camera bounds if needed
        if cam_comp.map_changed:
            cam: Camera2D = Camera2D.cast(cam_comp.camera)
            tile_layer: TileMapLayer = TileMapLayer.cast(cam_comp.tile_map)

            tile_set = tile_layer.get_tile_set()
            cell_size = tile_set.get_tile_size()
            map_rect = tile_layer.get_used_rect()

            cam.set_limit(0, map_rect.position.x * cell_size.x)
            cam.set_limit(1, map_rect.position.y * cell_size.y)
            cam.set_limit(2, (map_rect.position.x + map_rect.size.x) * cell_size.x)
            cam.set_limit(3, (map_rect.position.y + map_rect.size.y) * cell_size.y)
            cam_comp.map_changed = False

        # Start with a clean position
        target_position = cam_comp.camera.global_position

        # Get the player so the camera can follow them.
        player_list = esper.get_component(PlayerComponent)
        if player_list:
            player_ent, _ = player_list[0]

            if (cam_comp.is_active) and (
                player_body := esper.try_component(player_ent, BodyComponent)
            ):
                target_position = player_body.body.global_position

                # Smoothly update the camera's position to follow the player
                # If you have Position Smoothing enabled on Camera2D, setting its global_position
                # will let Godot's internal engine handle the interpolation interpolation cleanly!

        if shake := esper.try_component(cam_ent, CameraShakeComponent):
            shake.elapsed_time += delta

            if shake.elapsed_time >= shake.duration:
                esper.remove_component(cam_ent, CameraShakeComponent)
            else:
                current_fade = 1.0 - (shake.elapsed_time / shake.duration)
                current_intensity = shake.intensity * current_fade

                # Roll randomized screen offsets using standard python tools
                offset_x = random.uniform(-current_intensity, current_intensity)
                offset_y = random.uniform(-current_intensity, current_intensity)

                target_position += Vector2.new3(offset_x, offset_y)

        cam_comp.camera.global_position = target_position
