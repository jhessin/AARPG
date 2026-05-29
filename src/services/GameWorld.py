import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from src.systems import init_systems


@gdclass
class GameWorld(Node2D):

    def _ready(self) -> None:
        self.camera_entity: int
        self.physics_systems: list[esper.Processor] = init_systems()

    def _process(self, delta: "float") -> None:
        esper.process(delta)

    def _physics_process(self, delta: "float") -> None:
        for system in self.physics_systems:
            system.process(delta)
