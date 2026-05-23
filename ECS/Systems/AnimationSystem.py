from typing import Literal
import esper
from py4godot.classes.core import Vector2
from ..components import (
    StateComponent,
    AnimationComponent,
)


class AnimationSystem(esper.Processor):

    def process(self, _delta: float) -> None:
        del _delta
        # Query every entity in the game containing both data components
        for _, (anim, state) in esper.get_components(
            AnimationComponent, StateComponent
        ):
            if anim and state:
                print("AnimationComponent and StateComponent found!")
                anim.sprite.scale.x = (
                    -1 if state.cardinal_direction == Vector2.LEFT else 1
                )
                anim_direction = (
                    "down"
                    if state.cardinal_direction == Vector2.DOWN
                    else "up" if state.cardinal_direction == Vector2.UP else "side"
                )
                target_animation = f"{state.current}_{anim_direction}"
                if anim.animator.get_current_animation() != target_animation:
                    print(f"Running animation: {target_animation}")
                    anim.animator.play(target_animation)
