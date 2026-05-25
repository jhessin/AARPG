from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from py4godot.classes.Node2D import Node2D
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.AudioStream import AudioStream
from py4godot.classes.AudioStreamPlayer2D import AudioStreamPlayer2D
from py4godot.classes.Node import Node, Vector2
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.InputEvent import InputEvent
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.TileMapLayer import TileMapLayer

# Adding constants here
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


def clamp(val: float, low: float, high: float):
    return low if val < low else high if val > high else val


def avg(*args: float) -> float:
    return sum(args) / len(args)


class VelocityComponent:

    def __init__(self, speed: float = 100.0, x: float = 0.0, y: float = 0.0) -> None:
        speed = clamp(speed, 0.0, MAX_ENGINE_SPEED)
        self._speed: float = speed
        self._direction: Vector2 = Vector2.new3(x, y)

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = clamp(value, 0.0, MAX_ENGINE_SPEED)

    @property
    def direction(self) -> Vector2:
        return self._direction

    @property
    def x(self) -> float:
        return self._direction.x

    @x.setter
    def x(self, value: float) -> None:
        self._direction = Vector2.new3(
            value,
            self._direction.y,
        )

    @property
    def y(self) -> float:
        return self._direction.y

    @y.setter
    def y(self, value: float) -> None:
        self._direction = Vector2.new3(
            self._direction.x,
            value,
        )


@dataclass
class AnimationComponent:
    animator: AnimationPlayer
    sprite: Sprite2D
    weapon_pivot: Optional[Node2D] = None


@dataclass()
class AudioComponent:
    player: AudioStreamPlayer2D
    sounds: dict[str, AudioStream] = field(default_factory=dict)
    current_key: str = ""


@dataclass
class BodyComponent:
    body: Node2D


class HealthComponent:
    parent: Node

    def __init__(self, parent: Node2D, maximum: float = 100.0) -> None:
        self.parent = parent
        maximum = max(1.0, maximum)
        self._maximum: float = maximum
        self._current: float = maximum

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


@dataclass()
class PlayerComponent:
    model: CharacterBody2D


class State(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()

    def __str__(self) -> str:
        match self:
            case State.IDLE:
                return IDLE
            case State.WALK:
                return WALK
            case State.ATTACK:
                return ATTACK


class StateComponent:

    def __init__(self, decelerate_speed: float = 5.0) -> None:
        decelerate_speed = max(1.0, min(decelerate_speed, 20.0))
        self.current: State = State.IDLE
        self.previous: State = self.current
        self.animation_is_finished: bool = False
        self._cardinal_direction: Vector2 = Vector2.DOWN
        self._decelerate_speed: float = decelerate_speed

    @property
    def cardinal_direction(self) -> Vector2:
        return self._cardinal_direction

    @cardinal_direction.setter
    def cardinal_direction(self, value: Vector2) -> None:
        self._cardinal_direction = (
            value if value in FACINGS else self._cardinal_direction
        )

    @property
    def decelerate_speed(self) -> float:
        return self._decelerate_speed

    @decelerate_speed.setter
    def decelerate_speed(self, value: float) -> None:
        self._decelerate_speed = clamp(value, 1.0, 20.0)


class InputComponent:
    queue: list[InputEvent] = []


class HitboxComponent:
    node: Area2D = field(default_factory=Area2D.new)

    def __init__(
        self,
        node: Area2D,
        min_damage: float = 10.0,
        max_damage: float = 15.0,
        knockback_force: float = 300.0,
    ) -> None:
        self.node = node
        min_damage = max(min_damage, 1.0)
        max_damage = max(min_damage, max_damage)
        knockback_force = clamp(knockback_force, 0.0, 500.0)
        self._min_damage: float = min_damage
        self._max_damage: float = max_damage
        self._knockback_force: float = knockback_force
        self._attack_duration: float = 0.0

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


@dataclass()
class CameraComponent:
    camera: Camera2D
    tile_map: TileMapLayer

    # Flags for advanced camera states
    map_changed: bool = True
    is_active: bool = True


class CameraShakeComponent:

    def __init__(self, duration: float = 0.2, intensity: float = 8.0) -> None:
        duration = max(duration, 0.1)
        intensity = max(intensity, 0.0)
        self._duration: float = duration
        self._intensity: float = intensity
        self._elapsed_time: float = 0.0

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

    @elapsed_time.setter
    def elapsed_time(self, value: float):
        self._elapsed_time = value if value > self._elapsed_time else 0.0
