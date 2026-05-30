from __future__ import annotations
from py4godot.classes.core import Vector2

ATTACK: str = "attack"
IDLE: str = "idle"
WALK: str = "walk"
STUN: str = "stun"
DESTROY: str = "destroy"

ENTITY_ID: str = "ecs_entity_id"
MAX_ENGINE_SPEED: float = 1200.0

FACINGS: list[Vector2] = [
    Vector2.RIGHT,
    Vector2.DOWN,
    Vector2.LEFT,
    Vector2.UP,
]


def clamp(val: float, low: float, high: float) -> float:
    return low if val < low else high if val > high else val


def avg(*args: float) -> float:
    return sum(args) / len(args) if args else 0.0
