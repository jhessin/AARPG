from dataclasses import InitVar, dataclass, field
import math
from enum import Enum, auto
from py4godot.classes.Node2D import Node2D
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.AudioStream import AudioStream
from py4godot.classes.Node import Node
from py4godot.classes.core import Vector2
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer

# === CONSTANTS
ATTACK = "attack"
IDLE = "idle"
WALK = "walk"
ENTITY_ID = "ecs_entity_id"
MAX_ENGINE_SPEED = 1200.0
FACINGS = [
    Vector2.RIGHT,
    Vector2.DOWN,
    Vector2.LEFT,
    Vector2.UP,
]


# === UTILITY FUNCTIONS
def clamp(val: float, low: float, high: float):
    return low if val < low else high if val > high else val


def avg(*args: float) -> float:
    return sum(args) / len(args)


# === COMPONENTS


# == Player/Enemy Identity
@dataclass
class PlayerComponent:
    pass


@dataclass
class EnemyComponent:
    pass


# == State & AI
class State(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()
    # HURT = auto()
    # DEAD = auto()

    def __str__(self) -> str:
        match self:
            case State.IDLE:
                return IDLE
            case State.WALK:
                return WALK
            case State.ATTACK:
                return ATTACK


class AIState(Enum):
    IDLE = auto()
    WANDER = auto()
    CHASE = auto()
    ATTACK = auto()
    RETURN = auto()


@dataclass
class StateComponent:
    # constructor-only input
    init_state: State = State.IDLE

    # private storage
    _current: State = field(init=False, repr=False)
    _previous: State = field(init=False, repr=False)
    _time_in_state: float = field(default=0.0, init=False, repr=False)

    def __post_init__(self):
        # Route through setter for validation
        self.current = self.init_state
        self._previous = self.init_state

    # --- Public API ---

    @property
    def current(self) -> State:
        return self._current

    @current.setter
    def current(self, value: State):
        # Only allow valid states
        # if not isinstance(value, State):
        #     raise ValueError(f"Invalid state: {value}")

        # If changing state, update previous + reset timer
        if hasattr(self, "_current") and value != self._current:
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
        self._time_in_state += delta if delta > 0.0 else self._time_in_state


@dataclass
class AIComponent:
    # constructor-only inputs
    init_state: AIState = AIState.IDLE
    init_aggro_range: float = 150.0
    init_attack_range: float = 40.0
    init_wander_radius: float = 80.0
    init_spawn: InitVar[Vector2] = field(default_factory=Vector2.new0)

    # private storage
    _state: AIState = field(init=False, repr=False)
    _time_in_state: float = field(default=0.0, init=False, repr=False)
    _aggro_range: float = field(init=False, repr=False)
    _attack_range: float = field(init=False, repr=False)
    _wander_radius: float = field(init=False, repr=False)
    _spawn: Vector2 = field(init=False, repr=False)

    # AI memory
    target_entity: int | None = None
    last_known_x: float | None = None
    last_known_y: float | None = None

    def __post_init__(self, init_spawn: Vector2):
        self.state = self.init_state
        self.aggro_range = self.init_aggro_range
        self.attack_range = self.init_attack_range
        self.wander_radius = self.init_wander_radius
        self._spawn = init_spawn

    # --- Public API ---

    @property
    def state(self) -> AIState:
        return self._state

    @state.setter
    def state(self, value: AIState):
        # if not isinstance(value, AIState):
        #     raise ValueError(f"Invalid AI state: {value}")

        # Reset timer on state change
        if hasattr(self, "_state") and value != self._state:
            self._time_in_state = 0.0

        self._state = value

    @property
    def time_in_state(self) -> float:
        return self._time_in_state

    def tick(self, delta: float):
        self._time_in_state += delta

    @property
    def aggro_range(self) -> float:
        return self._aggro_range

    @aggro_range.setter
    def aggro_range(self, value: float):
        self._aggro_range = max(0.0, value)

    @property
    def attack_range(self) -> float:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: float):
        self._attack_range = max(0.0, value)

    @property
    def wander_radius(self) -> float:
        return self._wander_radius

    @wander_radius.setter
    def wander_radius(self, value: float):
        self._wander_radius = max(0.0, value)

    @property
    def spawn(self) -> Vector2:
        return self._spawn


@dataclass
class FacingComponent:
    facing: Vector2 = field(default=Vector2.DOWN)

    def set_from_vector(self, vec: Vector2):
        if vec.length() == 0.0:
            return
        idx = int(round((vec.angle() / math.tau) * len(FACINGS))) % len(FACINGS)
        self.facing = FACINGS[idx]


@dataclass
class AttackSlowComponent:
    factor: float = 0.5  # 50% speed while attacking

    def __post_init__(self):
        self.factor = clamp(self.factor, 0.0, 1.0)


@dataclass
class AnimationEventComponent:
    finished: bool = False


# == Input
@dataclass
class InputComponent:
    # constructor-only inputs
    init_move_x: float = 0.0
    init_move_y: float = 0.0
    init_attack: bool = False
    init_dash: bool = False
    init_interact: bool = False

    # private storage
    _move_x: float = field(init=False, repr=False)
    _move_y: float = field(init=False, repr=False)
    _attack: bool = field(init=False, repr=False)
    _dash: bool = field(init=False, repr=False)
    _interact: bool = field(init=False, repr=False)

    def __post_init__(self):
        # Route through setters for validation
        self.move_x = self.init_move_x
        self.move_y = self.init_move_y
        self.attack = self.init_attack
        self.dash = self.init_dash
        self.interact = self.init_interact

    # --- Public API ---

    @property
    def move_x(self) -> float:
        return self._move_x

    @move_x.setter
    def move_x(self, value: float):
        # Clamp to [-1, 1]
        self._move_x = max(-1.0, min(1.0, value))

    @property
    def move_y(self) -> float:
        return self._move_y

    @move_y.setter
    def move_y(self, value: float):
        # Clamp to [-1, 1]
        self._move_y = max(-1.0, min(1.0, value))

    @property
    def attack(self) -> bool:
        return self._attack

    @attack.setter
    def attack(self, value: bool):
        self._attack = bool(value)

    @property
    def dash(self) -> bool:
        return self._dash

    @dash.setter
    def dash(self, value: bool):
        self._dash = bool(value)

    @property
    def interact(self) -> bool:
        return self._interact

    @interact.setter
    def interact(self, value: bool):
        self._interact = bool(value)


# == Movement and Physics
@dataclass
class VelocityComponent:
    _speed: float = 100.0
    _direction: Vector2 = field(default_factory=Vector2.new0)

    def __post_init__(self):
        self._speed = clamp(self._speed, 0.0, MAX_ENGINE_SPEED)
        self._direction = (
            self._direction.normalized()
            if self._direction.length() > 0.0
            else Vector2.ZERO
        )

    @property
    def total_vel(self) -> Vector2:
        base = self._direction * self._speed
        return base

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = clamp(value, 0.0, MAX_ENGINE_SPEED)

    @property
    def direction(self) -> Vector2:
        return self._direction

    @direction.setter
    def direction(self, value: Vector2) -> None:
        self._direction = value.normalized() if value.length() > 0.0 else Vector2.ZERO


@dataclass
class KnockbackComponent:
    force: Vector2 = field(default=Vector2.ZERO)
    _decay: float = 10.0

    def __post_init__(self):
        self._decay = max(0.0, self._decay)

        if self.force.length() == 0.0:
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

    @property
    def id(self) -> int:
        return self._entity_id


# == Combat
@dataclass
class HealthComponent:
    parent: Node

    def __post_init__(self) -> None:
        self._maximum: float = max(1.0, self._maximum)
        self._current: float = self._maximum

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, value: float) -> None:
        self._current = clamp(value, 0.0, self._maximum)

    @property
    def maximum(self) -> float:
        return self._maximum

    @maximum.setter
    def maximum(self, value: float) -> None:
        self._maximum = max(value, 1.0)
        self._current = clamp(self._current, 0.0, self._maximum)


@dataclass
class HurtboxComponent:
    node: Area2D

    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int):
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id


@dataclass
class HitboxComponent:
    node: Area2D

    # constructor_only inputs
    damage_range: InitVar[tuple[float, float]] = (1.0, 1.0)
    init_knockback_force: InitVar[float] = 5.0

    # private storage
    _min_damage: float = field(init=False, repr=False)
    _max_damage: float = field(init=False, repr=False)
    _knockback_force: float = field(init=False, repr=False)
    _attack_duration: float = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(
        self, damage_range: tuple[float, float], init_knockback_force: float
    ) -> None:
        self.min_damage = damage_range[0]
        self.max_damage = damage_range[1]
        self.knockback_force = init_knockback_force
        self._attack_duration = 0.0

    def bind_entity(self, entity_id: int):
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def min_damage(self) -> float:
        return self._min_damage

    @min_damage.setter
    def min_damage(self, value: float) -> None:
        self._min_damage = max(value, 1.0)

    @property
    def max_damage(self) -> float:
        return self._max_damage

    @max_damage.setter
    def max_damage(self, value: float) -> None:
        self._max_damage = max(self._min_damage, value)

    @property
    def knockback_force(self) -> float:
        return self._knockback_force

    @knockback_force.setter
    def knockback_force(self, value: float) -> None:
        self._knockback_force = clamp(value, 0.0, 500.0)

    @property
    def attack_duration(self) -> float:
        return self._attack_duration

    @attack_duration.setter
    def attack_duration(self, value: float) -> None:
        self._attack_duration = max(0.0, value)


# == Animation
@dataclass
class AnimationComponent:
    player: AnimationPlayer

    # constructor-only inputs
    init_desired: str = ""
    init_speed: float = 1.0

    # private storage
    _desired: str = field(init=False, repr=False)
    _current: str = field(default="", init=False, repr=False)
    _speed: float = field(init=False, repr=False)
    _finished: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        # Route through setters for validation
        self.desired = self.init_desired
        self.speed = self.init_speed

    # --- Public API ---

    @property
    def desired(self) -> str:
        return self._desired

    @desired.setter
    def desired(self, value: str):
        # Empty string is allowed (means "no animation requested")
        self._desired = value or ""

    @property
    def current(self) -> str:
        return self._current

    @current.setter
    def current(self, value: str):
        self._current = value or ""

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        # Clamp to a safe range
        self._speed = max(0.1, min(4.0, value))

    @property
    def finished(self) -> bool:
        return self._finished

    @finished.setter
    def finished(self, value: bool):
        self._finished = bool(value)


# == Audio
@dataclass
class AudioComponent:
    sounds: dict[str, AudioStream] = field(default_factory=lambda: {})
    current_key: str = ""


# == Camera
@dataclass()
class CameraComponent:
    camera: Camera2D
    tile_map: TileMapLayer

    # Flags for advanced camera states
    map_changed: bool = True
    is_active: bool = True


@dataclass
class CameraShakeComponent:
    init_duration: InitVar[float] = 0.0
    init_intensity: InitVar[float] = 0.0

    _duration: float = field(init=False, repr=False)
    _intensity: float = field(init=False, repr=False)
    _elapsed_time: float = field(default=0.0, init=False, repr=False)

    def __post_init__(
        self, init_duration: float = 0.2, init_intensity: float = 8.0
    ) -> None:
        self.duration = init_duration
        self.intensity = init_intensity

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, value: float) -> None:
        self._duration = max(value, 0.1)

    @property
    def intensity(self) -> float:
        return self._intensity

    @intensity.setter
    def intensity(self, value: float) -> None:
        self._intensity = max(value, 0.0)

    @property
    def elapsed_time(self) -> float:
        return self._elapsed_time

    def tick(self, delta: float):
        self._elapsed_time += delta if delta > 0.0 else self._elapsed_time
