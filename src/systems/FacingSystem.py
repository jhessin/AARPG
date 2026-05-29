from typing import Optional
import esper
from math import pi
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.CollisionShape2D import CollisionShape2D
from py4godot.classes.core import Vector2

from ..components import (
    FacingComponent,
    BodyComponent,
)


def find_first_sprite(node: Node2D) -> Sprite2D | None:
    s = Sprite2D.cast(node)
    if s is not None:
        return s

    for child in node.get_children():

        # 1. Try to cast THIS child into a Sprite2D
        s = Sprite2D.cast(child)
        if s is not None:
            return s

        # 2. Do NOT recurse into CollisionShape2D
        if CollisionShape2D.cast(child) is not None:
            continue

        # 3. Recurse only into Node2D children
        if Node2D.cast(child) is not None:
            nested = find_first_sprite(child)
            if nested is not None:
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

            if body is None:
                continue

            # ---------------------------------------------------------
            # 1. Flip the player sprite
            # ---------------------------------------------------------
            if body.has_node("%Sprite"):
                sprite = body.get_node("%Sprite")
                if sprite:
                    sprite.set_flip_h(facing.facing == Vector2.LEFT)
                else:
                    print("NO SPRITE FOUND!!!")

            # ---------------------------------------------------------
            # 2. Recursively find the first pivot node
            # ---------------------------------------------------------
            if body.has_node("%WeaponPivot"):
                pivot: Optional[Node2D] = body.get_node("%WeaponPivot")
                if pivot:
                    pivot.rotation = facing.facing.angle() - pi / 2
                # else:
                #     print("NO PIVOT FOUND")

            if body.has_node("%EffectAnchor"):
                pivot = body.get_node("%EffectAnchor")
                if pivot:
                    pivot.scale.x = -1 if facing.facing == Vector2.LEFT else 1
                # else:
                #     print("NO PIVOT FOUND")
