from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.Node import Vector2
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.InputEvent import InputEvent


@dataclass
class VelocityComponent:
    speed: float = 100.0
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
    ATTACK = auto()

    def __str__(self) -> str:
        match self:
            case PlayerState.IDLE:
                return "idle"
            case PlayerState.WALK:
                return "walk"
            case PlayerState.ATTACK:
                return "attack"


class StateComponent:
    current: PlayerState = PlayerState.IDLE
    previous: PlayerState = current
    cardinal_direction: Vector2 = Vector2.DOWN


class InputComponent:
    queue: list[InputEvent] = []
