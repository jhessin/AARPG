import esper
from py4godot import gdclass, gdmethod
from py4godot.classes.Node2D import Node2D
from ECS.Systems.AnimationSystem import AnimationSystem
from ECS.Systems.MovementSystem import MovementSystem
from ECS.Systems.InputSystem import InputSystem


@gdclass
class GameWorld(Node2D):

    @gdmethod
    def _ready(self) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        print("Preparing GameWorldManager")
        esper.add_processor(InputSystem(), priority=1)
        esper.add_processor(MovementSystem())
        esper.add_processor(AnimationSystem())

    @gdmethod
    def _process(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, delta: "float"
    ) -> None:
        esper.process(delta)
