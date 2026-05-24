import esper
from py4godot.classes.core import Vector2
from ..components import (
    State,
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
                self.state: StateComponent = state
                self.anim: AnimationComponent = anim
                anim.sprite.flip_h = state.cardinal_direction == Vector2.LEFT
                anim.sprite.get_node("%EffectAnchor").scale.x = (
                    -1 if state.cardinal_direction == Vector2.LEFT else 1
                )
                anim_direction = (
                    "down"
                    if state.cardinal_direction == Vector2.DOWN
                    else "up" if state.cardinal_direction == Vector2.UP else "side"
                )
                if anim.weapon_pivot:
                    anim.weapon_pivot.rotation_degrees = (
                        0
                        if state.cardinal_direction == Vector2.DOWN
                        else (
                            90
                            if state.cardinal_direction == Vector2.LEFT
                            else 180 if state.cardinal_direction == Vector2.UP else -90
                        )
                    )
                target_animation = f"{state.current}_{anim_direction}"
                if anim.animator.get_current_animation() != target_animation:
                    anim.animator.play(target_animation)

                if state.current == State.ATTACK:
                    if state.animation_is_finished:
                        prev: State = state.previous
                        state.previous = state.current
                        state.current = prev
                        state.animation_is_finished = False
