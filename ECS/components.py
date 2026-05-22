from dataclasses import dataclass
from enum import Enum, auto
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.Node import Vector2
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.CharacterBody2D import CharacterBody2D


@dataclass
class VelocityComponent:
    speed: float = 200.0
    x: float = 0.0
    y: float = 0.0


@dataclass
class AnimationComponent:
    animator: AnimationPlayer
    sprite: Sprite2D


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

    def __str__(self) -> str:
        match self:
            case PlayerState.IDLE:
                return "idle"
            case PlayerState.WALK:
                return "walk"


@dataclass()
class StateComponent:
    current: PlayerState
    previous: PlayerState

    def __init__(self, initial_state: PlayerState = PlayerState.IDLE) -> None:
        self.current = initial_state
        self.previous = initial_state
