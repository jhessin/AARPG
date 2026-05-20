from dataclasses import dataclass
from py4godot.classes.AnimationPlayer import AnimationPlayer
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
