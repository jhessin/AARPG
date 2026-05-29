from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import Tuple
from py4godot.classes.Area2D import Area2D
from .util import clamp, ENTITY_ID


@dataclass
class HealthComponent:
    init_max: InitVar[float] = 100.0
    _maximum: float = field(init=False, repr=False)
    _current: float = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self, init_max: float):
        self.maximum = init_max
        self.current = self._maximum

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, value: float):
        self._current = clamp(value, 0.0, self._maximum)

    @property
    def maximum(self) -> float:
        return self._maximum

    @maximum.setter
    def maximum(self, value: float):
        self._maximum = max(value, 1.0)
        self._current = clamp(
            getattr(self, "_current", self._maximum), 0.0, self._maximum
        )

    @property
    def dead(self) -> bool:
        return self._current <= 0


@dataclass
class HurtboxComponent:
    node: Area2D
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id
        self.node.set_meta(ENTITY_ID, entity_id)

    @property
    def id(self) -> int:
        return self._entity_id


@dataclass
class HitboxComponent:
    node: Area2D
    damage_range: InitVar[Tuple[float, float]] = (1.0, 1.0)
    init_knockback_force: InitVar[float] = 5.0
    _min_damage: float = field(init=False, repr=False)
    _max_damage: float = field(init=False, repr=False)
    _knockback_force: float = field(init=False, repr=False)
    _attack_duration: float = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(
        self, damage_range: Tuple[float, float], init_knockback_force: float
    ):
        self.min_damage = damage_range[0]
        self.max_damage = damage_range[1]
        self.knockback_force = init_knockback_force
        self._attack_duration = 0.0

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id
        self.node.set_meta(ENTITY_ID, entity_id)

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def min_damage(self) -> float:
        return self._min_damage

    @min_damage.setter
    def min_damage(self, value: float):
        self._min_damage = max(value, 1.0)

    @property
    def max_damage(self) -> float:
        return self._max_damage

    @max_damage.setter
    def max_damage(self, value: float):
        self._max_damage = max(self._min_damage, value)

    @property
    def knockback_force(self) -> float:
        return self._knockback_force

    @knockback_force.setter
    def knockback_force(self, value: float):
        self._knockback_force = clamp(value, 0.0, 500.0)

    @property
    def attack_duration(self) -> float:
        return self._attack_duration

    @attack_duration.setter
    def attack_duration(self, value: float):
        self._attack_duration = max(0.0, value)
