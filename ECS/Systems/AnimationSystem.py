from typing import Literal
import esper
from py4godot.classes.core import Vector2
from ..components import VelocityComponent, AnimationComponent


class AnimationSystem(esper.Processor):
    state: Literal["idle", "walk"] = "idle"
    cardinal_direction: Vector2 = Vector2.DOWN
    direction: Vector2 = Vector2.DOWN
    anim_comp: AnimationComponent

    def process(self, delta: float) -> None:
        # Query every entity in the game containing both data components
        for ent, (vel, anim) in esper.get_components(
            VelocityComponent, AnimationComponent
        ):
            if vel and anim:
                self.anim_comp = anim
                self.direction = Vector2.new3(vel.x, vel.y)
                if self._update_direction() or self._update_state():
                    anim.animator.play(f"{self.state}_{self._anim_direction()}")

    def _update_state(self) -> bool:
        new_state: str = self.state
        new_state = "idle" if self.direction == Vector2.ZERO else "walk"
        if self.state == new_state:
            return False
        self.state = new_state
        return True

    def _update_direction(self) -> bool:
        new_dir: Vector2 = self.cardinal_direction
        if self.direction == Vector2.ZERO:
            return False
        if self.direction.y == 0:
            new_dir = Vector2.LEFT if self.direction.x < 0 else Vector2.RIGHT
        elif self.direction.x == 0:
            new_dir = Vector2.UP if self.direction.y < 0 else Vector2.DOWN

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
