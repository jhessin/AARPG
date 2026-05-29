from dataclasses import dataclass, field
from py4godot.classes.Node2D import Node2D
from py4godot.classes.core import Vector2
from .util import clamp, MAX_ENGINE_SPEED, ENTITY_ID


@dataclass
class VelocityComponent:
    _speed: float = 100.0
    _direction: Vector2 = field(default_factory=Vector2.new0)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self._speed = clamp(self._speed, 0.0, MAX_ENGINE_SPEED)
        self._direction = (
            self._direction.normalized()
            if self._direction.length() > 0
            else Vector2.ZERO
        )

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def total_vel(self) -> Vector2:
        return self._direction * self._speed

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = clamp(value, 0.0, MAX_ENGINE_SPEED)

    @property
    def direction(self) -> Vector2:
        return self._direction

    @direction.setter
    def direction(self, value: Vector2):
        self._direction = value.normalized() if value.length() > 0 else Vector2.ZERO


@dataclass
class KnockbackComponent:
    force: Vector2 = field(default_factory=lambda: Vector2.ZERO)
    _decay: float = 10.0

    def __post_init__(self):
        self._decay = max(0.0, self._decay)
        if self.force.length() == 0:
            self.force = Vector2.ZERO

    @property
    def decay(self) -> float:
        return self._decay


@dataclass
class BodyComponent:
    body: Node2D
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id
        self.body.set_meta(ENTITY_ID, entity_id)

    @property
    def id(self) -> int:
        return self._entity_id
