from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from enum import Enum, auto
from random import randint
from typing import Optional
from py4godot.classes.core import Vector2
from .util import clamp, FACINGS, IDLE, WALK, ATTACK


class State(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()

    def __str__(self) -> str:
        return {State.IDLE: IDLE, State.WALK: WALK, State.ATTACK: ATTACK}[self]


class AIState(Enum):
    IDLE = auto()
    WANDER = auto()
    CHASE = auto()
    ATTACK = auto()
    RETURN = auto()

    def __str__(self) -> str:
        match self:
            case AIState.IDLE:
                return IDLE
            case _:
                return WALK


@dataclass
class StateComponent:
    init_state: State = State.IDLE
    _current: State = field(init=False, repr=False)
    _previous: State = field(init=False, repr=False)
    _time_in_state: float = field(default=0.0, init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self._current = self._previous = self.init_state

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def current(self) -> State:
        return self._current

    @current.setter
    def current(self, value: State):
        if value != self._current:
            self._previous = self._current
            self._time_in_state = 0.0
        self._current = value

    @property
    def previous(self) -> State:
        return self._previous

    @property
    def time_in_state(self) -> float:
        return self._time_in_state

    def tick(self, delta: float):
        self._time_in_state += max(delta, 0.0)


@dataclass
class SimpleAIComponent:
    min_state_cycles: InitVar[int] = 1
    max_state_cycles: InitVar[int] = 3
    anim_length: InitVar[float] = 0.3
    init_speed: InitVar[float] = 1.0

    _state: AIState = field(repr=False, init=False)
    _toggle_state: AIState = field(repr=False, init=False)
    _min_state_cycles: int = field(repr=False, init=False)
    _max_state_cycles: int = field(repr=False, init=False)
    _anim_length: float = field(repr=False, init=False)
    _speed: float = field(repr=False, init=False)
    _timer: float = field(repr=False, init=False)
    _time_in_state: float = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(
        self,
        min_state_cycles: int,
        max_state_cycles: int,
        anim_length: float,
        init_speed: float,
    ):
        self._speed = max(1.0, init_speed)
        self._state = AIState.IDLE
        self._toggle_state = AIState.WANDER
        self._max_state_cycles = max(max_state_cycles, 1)
        self._min_state_cycles = (
            1
            if min_state_cycles < 1
            else (
                min_state_cycles
                if min_state_cycles < self._max_state_cycles
                else self._max_state_cycles
            )
        )
        self._anim_length = max(anim_length, 0.01)
        self._timer = randint(min_state_cycles, max_state_cycles) * self._anim_length
        self._time_in_state = 0

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def state(self) -> AIState:
        return self._state

    @property
    def speed(self) -> float:
        return self._speed

    def tick(self, delta: float):
        self._time_in_state += delta if delta > 0 else 0
        print(f"Time in state: {self._time_in_state}")
        print(f"Timer: {self._timer}")
        print(f"Current State: {self.state}")
        if self._time_in_state >= self._timer:
            self._state, self._toggle_state = self._toggle_state, self._state
            self._time_in_state = 0
            self._timer = (
                randint(self._min_state_cycles, self._max_state_cycles)
                * self._anim_length
            )


@dataclass
class AIComponent:
    # Initial configuration
    init_state: AIState = AIState.IDLE
    init_aggro_range: float = 150.0
    init_attack_range: float = 40.0
    init_wander_radius: float = 80.0
    init_spawn: InitVar[Vector2] = Vector2.ZERO

    # Internal state
    _state: AIState = field(init=False, repr=False)
    _time_in_state: float = field(default=0.0, init=False, repr=False)

    _aggro_range: float = field(init=False, repr=False)
    _attack_range: float = field(init=False, repr=False)
    _wander_radius: float = field(init=False, repr=False)
    _spawn: Vector2 = field(init=False, repr=False)

    # Entity binding
    _entity_id: int = field(init=False, repr=False)

    # Dynamic AI data
    target_entity: Optional[int] = None
    last_known_x: Optional[float] = None
    last_known_y: Optional[float] = None

    def __post_init__(self, init_spawn: Vector2) -> None:
        # Initial state
        self._state = self.init_state
        self._time_in_state = 0.0

        # Ranges
        self._aggro_range = max(0.0, self.init_aggro_range)
        self._attack_range = max(0.0, self.init_attack_range)
        self._wander_radius = max(0.0, self.init_wander_radius)

        # Spawn point
        self._spawn = init_spawn

    # Entity binding
    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    # State machine
    @property
    def state(self) -> AIState:
        return self._state

    @state.setter
    def state(self, value: AIState) -> None:
        if value != self._state:
            self._time_in_state = 0.0
        self._state = value

    @property
    def time_in_state(self) -> float:
        return self._time_in_state

    def tick(self, delta: float) -> None:
        self._time_in_state += delta

    # Ranges
    @property
    def aggro_range(self) -> float:
        return self._aggro_range

    @aggro_range.setter
    def aggro_range(self, value: float) -> None:
        self._aggro_range = max(0.0, value)

    @property
    def attack_range(self) -> float:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: float) -> None:
        self._attack_range = max(0.0, value)

    @property
    def wander_radius(self) -> float:
        return self._wander_radius

    @wander_radius.setter
    def wander_radius(self, value: float) -> None:
        self._wander_radius = max(0.0, value)

    # Spawn point
    @property
    def spawn(self) -> Vector2:
        return self._spawn


@dataclass
class FacingComponent:
    _facing: Vector2 = field(
        default_factory=lambda: Vector2.DOWN, init=False, repr=False
    )
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def animation_string(self) -> str:
        match self.facing:
            case Vector2.UP:
                return "up"
            case Vector2.DOWN:
                return "down"
            case _:
                return "side"

    @property
    def facing(self) -> Vector2:
        return self._facing

    def set_from_vector(self, vec: Vector2):
        if vec.length() == 0.0:
            return
        idx = int(round((vec.angle() / (2 * 3.14159)) * len(FACINGS))) % len(FACINGS)
        self._facing = FACINGS[idx]


@dataclass
class AttackSlowComponent:
    factor: float = 0.5
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self.factor = clamp(self.factor, 0.0, 1.0)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id


@dataclass
class AnimationEventComponent:
    finished: bool = False
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id
