import esper
from py4godot.classes.Node2D import Node2D
from py4godot.classes.core import Vector2
from py4godot.classes.Sprite2D import Sprite2D

from components import (
    FacingComponent,
    BodyComponent,
)


class FacingSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        for _, (facing, body_comp) in esper.get_components(
            FacingComponent,
            BodyComponent,
        ):
            node = body_comp.body

            # ---------------------------------------------------------
            # 1. Flip horizontally for left-facing orientation
            # ---------------------------------------------------------
            # LEFT = (-1, 0)
            sprite: Sprite2D | None = None
            for child in node.get_children():
                if (s := Sprite2D.cast(child)) is not None:
                    sprite = s
                    break

            if sprite:
                sprite.set_flip_h(facing.facing == Vector2.LEFT)

            # ---------------------------------------------------------
            # 2. Flip weapon pivot if it exists
            # ---------------------------------------------------------
            # This assumes your weapon pivot is a child named "WeaponPivot"
            if node.has_node("WeaponPivot") and (
                pivot := Node2D.cast(node.get_node("WeaponPivot"))
            ):

                # Mirror pivot horizontally
                if facing.facing == Vector2.LEFT:
                    pivot.scale.x = -1
                else:
                    pivot.scale.x = 1
