from dataclasses import dataclass, field
from enum import Enum, auto
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.AudioStream import AudioStream
from py4godot.classes.AudioStreamPlayer2D import AudioStreamPlayer2D
from py4godot.classes.Node import Vector2
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.InputEvent import InputEvent

# Adding constants here
ATTACK = "attack"
IDLE = "idle"


@dataclass
class VelocityComponent:
    speed: float = 100.0
    x: float = 0.0
    y: float = 0.0


@dataclass
class AnimationComponent:
    animator: AnimationPlayer
    sprite: Sprite2D


@dataclass()
class AudioComponent:
    player: AudioStreamPlayer2D
    sounds: dict[str, AudioStream] = field(default_factory=dict)
    current_key: str = ""


@dataclass
class BodyComponent:
    body: CharacterBody2D


@dataclass
class HealthComponent:
    maximum: float = 100.0
    current: float = maximum


class IsPlayer:
    pass


class PlayerState(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()

    def __str__(self) -> str:
        match self:
            case PlayerState.IDLE:
                return "idle"
            case PlayerState.WALK:
                return "walk"
            case PlayerState.ATTACK:
                return "attack"


@dataclass()
class StateComponent:
    current: PlayerState = PlayerState.IDLE
    previous: PlayerState = current
    time_in_state: float = 0.0
    cardinal_direction: Vector2 = field(default_factory=lambda: Vector2.DOWN)
    animation_is_finished: bool = False
    decelerate_speed: float = 5.0


class InputComponent:
    queue: list[InputEvent] = []
