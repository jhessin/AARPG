import esper
from py4godot.classes.core import Vector2
from ..components import (
    HitboxComponent,
    State,
    StateComponent,
    AnimationComponent,
)


class AnimationSystem(esper.Processor):

    def process(self, _delta: float) -> None:
        del _delta
        # Query every entity in the game containing both data components
        for ent, (anim, state) in esper.get_components(
            AnimationComponent, StateComponent
        ):
            if anim and state:
                # Flip the sprite if the cardinal_direction is facing left
                anim.sprite.flip_h = state.cardinal_direction == Vector2.LEFT

                # similarly scale the EffectAnchor to flip the effects if there
                # is one
                if effect_anchor := anim.sprite.get_node("%EffectAnchor"):
                    effect_anchor.scale.x = (
                        -1 if state.cardinal_direction == Vector2.LEFT else 1
                    )

                # Get the directional portion of the animation to play
                anim_direction = (
                    "down"
                    if state.cardinal_direction == Vector2.DOWN
                    else "up" if state.cardinal_direction == Vector2.UP else "side"
                )

                # Pivot the weapon (Area2D) to match the direction the character
                # is facing
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

                # Put it all together
                target_animation = f"{state.current}_{anim_direction}"

                # Get the hitbox if there is one and store the animation duration in it.
                if hitbox := esper.try_component(ent, HitboxComponent):
                    hitbox.attack_duration = anim.animator.get_animation(
                        target_animation
                    ).get_length()

                # Only play if we aren't already playing
                if anim.animator.get_current_animation() != target_animation:
                    anim.animator.play(target_animation)

                # Check for the finished animation flag when attacking
                if state.current == State.ATTACK:
                    if state.animation_is_finished:
                        prev: State = state.previous
                        state.previous = state.current
                        state.current = prev
                        state.animation_is_finished = False
