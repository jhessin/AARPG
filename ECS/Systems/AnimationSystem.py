from typing import Literal
import esper
from py4godot.classes.core import Vector2
from ..components import (
    PlayerState,
    StateComponent,
    VelocityComponent,
    AnimationComponent,
)


class AnimationSystem(esper.Processor):
    state: PlayerState = PlayerState.IDLE
    state_comp: StateComponent
    cardinal_direction: Vector2 = Vector2.DOWN
    direction: Vector2 = Vector2.DOWN
    anim_comp: AnimationComponent

    def process(self, _delta: float) -> None:
        del _delta
        # Query every entity in the game containing both data components
        for _, (vel, anim, state) in esper.get_components(
            VelocityComponent, AnimationComponent, StateComponent
        ):
            if vel and anim and state:
                self.anim_comp = anim
                self.direction = Vector2.new3(vel.x, vel.y)
                self.state_comp = state
                if self._update_direction() or self._update_state():
                    anim.animator.play(f"{self.state}_{self._anim_direction()}")

    def _update_state(self) -> bool:
        new_state: PlayerState = self.state
        new_state = self.state_comp.current
        if self.state == new_state:
            return False
        self.state = new_state
        return True

    def _update_direction(self) -> bool:
        new_dir: Vector2 = self.state_comp.cardinal_direction

        if new_dir == self.cardinal_direction:
            return False
        self.cardinal_direction = new_dir
        self.anim_comp.sprite.scale.x = (
            -1 if self.cardinal_direction == Vector2.LEFT else 1
        )
        return True

    def _anim_direction(self) -> Literal["down", "up", "side"]:
        if self.cardinal_direction == Vector2.DOWN:
            return "down"
        elif self.cardinal_direction == Vector2.UP:
            return "up"
        return "side"
