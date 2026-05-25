import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer
from ECS.Systems.AISystem import AISystem
from ECS.Systems.AnimationSystem import AnimationSystem
from ECS.Systems.CameraSystem import CameraSystem
from ECS.Systems.HealthSystem import HealthSystem
from ECS.Systems.MovementSystem import MovementSystem
from ECS.Systems.InputSystem import InputSystem
from ECS.Systems.SoundSystem import SoundSystem
from ECS.Systems.CombatSystem import CombatSystem
from ECS.components import ENTITY_ID, CameraComponent


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
        print(f"📷 Camera successfully registered as entity #{self.camera_entity}")

        camera_node.set_meta(ENTITY_ID, self.camera_entity)

    def set_camera_bounds(self) -> None:
        raw_camera = self.get_node("%Player").get_node("%Camera2D")
        raw_tile_layer = self.get_node("%Grass01")

        if not raw_camera or not raw_tile_layer:
            print("❌ Camera or TileMapLayer unique name nodes missing!")
            return

        camera = Camera2D.cast(raw_camera)
        tile_layer = TileMapLayer.cast(raw_tile_layer)

        tile_set = tile_layer.get_tile_set()
        if not tile_set:
            return
        cell_size = tile_set.get_tile_size()

        map_rect = tile_layer.get_used_rect()

        left_bound = map_rect.position.x * cell_size.x
        top_bound = map_rect.position.y * cell_size.y
        right_bound = (map_rect.position.x + map_rect.size.x) * cell_size.x
        bottom_bound = (map_rect.position.y + map_rect.size.y) * cell_size.y

        camera.set_limit(0, left_bound)
        camera.set_limit(1, top_bound)
        camera.set_limit(2, right_bound)
        camera.set_limit(3, bottom_bound)
