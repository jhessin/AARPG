import esper

from py4godot import gdclass
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer

from ..components import CameraComponent


@gdclass
class Camera(Camera2D):
    tile_map: TileMapLayer
    NOTIFICATION_RESIZED: int

    def _ready(self) -> None:
        if not self.tile_map:
            self.tile_map = self.get_node("%TileMap")
        if not self.tile_map:
            print("❌❌ YOU FORGOT TO ADD YOUR TILE MAP TO THE CAMERA ❌❌")
            return

        # Clear out any other cameras - you are the only camera!
        for ent, _ in esper.get_component(CameraComponent):
            esper.delete_entity(ent)

        # Create the camera component
        cam_comp = CameraComponent(self, self.tile_map)
        self.entity = esper.create_entity(cam_comp)
        cam_comp.bind_entity(self.entity)

    def _notification(self, what: int) -> None:
        if what == self.NOTIFICATION_RESIZED:
            self._update_half_screen_size()

    def _update_half_screen_size(self) -> None:
        viewport = self.get_viewport()
        rect = viewport.get_visible_rect()

        if cam_comp := esper.try_component(self.entity, CameraComponent):
            cam_comp._half_screen_size = rect.size * 0.5
