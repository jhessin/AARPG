import esper
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.core import Vector2

from components import (
    FacingComponent,
    BodyComponent,
)


def find_first_sprite(node: Node2D) -> Sprite2D | None:
    # Depth-first search for Sprite2D
    for child in node.get_children():
        if (s := Sprite2D.cast(child)) is not None:
            return s
        if isinstance(child, Node2D):
            if (nested := find_first_sprite(child)) is not None:
                return nested
    return None


def find_weapon_pivot(node: Node2D) -> Node2D | None:
    # Depth-first search for any Node2D with "pivot" in its name
    for child in node.get_children():
        if isinstance(child, Node2D):
            if "pivot" in str(child.name).lower():
                return child
            if (nested := find_weapon_pivot(child)) is not None:
                return nested
    return None


class FacingSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        for _, (facing, body_comp) in esper.get_components(
            FacingComponent,
            BodyComponent,
        ):
            body = body_comp.body

            # ---------------------------------------------------------
            # 1. Recursively find the first Sprite2D
            # ---------------------------------------------------------
            sprite = find_first_sprite(body)
            if sprite:
                sprite.set_flip_h(facing.facing == Vector2.LEFT)

            # ---------------------------------------------------------
            # 2. Recursively find the first pivot node
            # ---------------------------------------------------------
            pivot = find_weapon_pivot(body)
            if pivot:
                pivot.scale.x = -1 if facing.facing == Vector2.LEFT else 1
