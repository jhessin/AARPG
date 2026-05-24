import esper
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer

from ECS.components import BodyComponent, CameraComponent, PlayerComponent


class CameraSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        camera_list = esper.get_component(CameraComponent)
        if not camera_list:
            return

        _, cam_comp = camera_list[0]

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

        # Get the player so the camera can follow them.
        player_list = esper.get_component(PlayerComponent)
        if player_list:
            player_ent, _ = player_list[0]

            if (cam_comp.is_active) and (
                player_body := esper.try_component(player_ent, BodyComponent)
            ):
                player_pos = player_body.body.global_position

                # Smoothly update the camera's position to follow the player
                # If you have Position Smoothing enabled on Camera2D, setting its global_position
                # will let Godot's internal engine handle the interpolation interpolation cleanly!
                cam_comp.camera.global_position = player_pos
