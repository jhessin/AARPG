import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from ECS.Systems.AnimationSystem import AnimationSystem
from ECS.Systems.MovementSystem import MovementSystem
from ECS.Systems.InputSystem import InputSystem


@gdclass
class GameWorld(Node2D):
    physics_system: esper.Processor

    def _ready(self) -> None:
        print("Preparing GameWorldManager")
        esper.add_processor(InputSystem(), priority=1)
        esper.add_processor(AnimationSystem())

        # Use one or the other
        # esper.add_processor(MovementSystem())
        self.physics_system = MovementSystem()

    def _process(self, delta: "float") -> None:
        esper.process(delta)

    def _physics_process(self, delta: "float") -> None:
        self.physics_system.process(delta)
