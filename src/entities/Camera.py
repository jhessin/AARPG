import esper

from py4godot import gdclass
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer

from components import CameraComponent


@gdclass
class Camera(Camera2D):
    tile_map: TileMapLayer

    def _ready(self) -> None:
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
