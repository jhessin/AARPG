from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
from py4godot.classes.Node2D import Node2D
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.AudioStream import AudioStream
from py4godot.classes.AudioStreamPlayer2D import AudioStreamPlayer2D
from py4godot.classes.Node import Vector2
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.InputEvent import InputEvent
from py4godot.classes.Area2D import Area2D

# from py4godot.classes.CharacterBody2D import CharacterBody2D

# Adding constants here
ATTACK = "attack"
IDLE = "idle"
WALK = "walk"
ENTITY_ID = "ecs_entity_id"


@dataclass
class VelocityComponent:
    speed: float = 100.0
    x: float = 0.0
    y: float = 0.0


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


@dataclass
class HealthComponent:
    parent: Node2D
    maximum: float
    current: float

    def __init__(self, parent: Node2D, maximum: float = 100.0) -> None:
        self.parent = parent
        self.maximum = maximum
        self.current = maximum


class IsPlayer:
    pass


class PlayerState(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()

    def __str__(self) -> str:
        match self:
            case PlayerState.IDLE:
                return IDLE
            case PlayerState.WALK:
                return WALK
            case PlayerState.ATTACK:
                return ATTACK


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


@dataclass()
class HitboxComponent:
    node: Area2D = field(default_factory=Area2D.new)
    damage: float = 10.0
    knockback_force: float = 300.0


@dataclass()
class HurtboxComponent:
    node: Area2D = field(default_factory=Area2D.new)
