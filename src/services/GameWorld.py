import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer
from src.systems.AISystem import AISystem
from src.systems.AnimationSystem import AnimationSystem
from src.systems.CameraSystem import CameraSystem
from src.systems.HealthSystem import HealthSystem
from src.systems.MovementSystem import MovementSystem
from src.systems.InputSystem import InputSystem
from src.systems.SoundSystem import SoundSystem
from src.systems.CombatSystem import CombatSystem
from src.components import ENTITY_ID, CameraComponent


@gdclass
class GameWorld(Node2D):

    def _ready(self) -> None:
        self.camera_entity: int
        esper.add_processor(InputSystem(), priority=1)
        esper.add_processor(AnimationSystem())
        esper.add_processor(SoundSystem())
        esper.add_processor(CombatSystem())
        esper.add_processor(HealthSystem())
        esper.add_processor(CameraSystem())
        esper.add_processor(AISystem())

        # Use one or the other
        # esper.add_processor(MovementSystem())
        self.physics_systems: list[esper.Processor] = []
        self.physics_systems.append(MovementSystem())

        self.register_camera()

    def _process(self, delta: "float") -> None:
        esper.process(delta)

    def _physics_process(self, delta: "float") -> None:
        for system in self.physics_systems:
            system.process(delta)

    def register_camera(self) -> None:
        """
        Register a camera entity and stamp the node with the entity ID
        """
        raw_camera = self.get_node("%Camera")
        raw_tile_layer = self.get_node("%TileMap")

        if not raw_camera or not raw_tile_layer:
            print("❌⚠️ The camera and tile map couldn't be found. Were they renamed?")
            return

        camera_node = Camera2D.cast(raw_camera)
        tile_layer = TileMapLayer.cast(raw_tile_layer)

        self.camera_entity = esper.create_entity(
            CameraComponent(camera_node, tile_layer),
        )

        camera_node.set_meta(ENTITY_ID, self.camera_entity)
