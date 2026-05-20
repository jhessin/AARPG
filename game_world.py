import esper
from py4godot import gdclass
from py4godot.classes.Node2D import Node2D
from ECS.Systems.AnimationSystem import AnimationSystem
from ECS.Systems.MovementSystem import MovementSystem
from ECS.Systems.InputSystem import InputSystem


@gdclass
class GameWorldManager(Node2D):

    def _init(self) -> None:
        print("Preparing GameWorldManager")
        esper.add_processor(InputSystem(), priority=1)
        esper.add_processor(MovementSystem())
        esper.add_processor(AnimationSystem())

    def _process(self, delta: "float") -> None:
        esper.process(delta)
