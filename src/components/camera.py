from __future__ import annotations
from dataclasses import dataclass, field
from random import uniform
from py4godot.classes.Camera2D import Camera2D
from py4godot.classes.TileMapLayer import TileMapLayer
from py4godot.classes.core import Vector2
from .util import ENTITY_ID


@dataclass
class CameraComponent:
    camera: Camera2D
    tile_map: TileMapLayer

    map_changed: bool = True
    is_active: bool = True
    offset: Vector2 = field(default_factory=lambda: Vector2.ZERO)
    smoothing: float = 0.15

    _half_screen_size: Vector2 = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        viewport = self.camera.get_viewport()
        rect = viewport.get_visible_rect()
        self._half_screen_size = rect.size * 0.5

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id
        self.camera.set_meta(ENTITY_ID, entity_id)

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def half_screen_size(self) -> Vector2:
        return self._half_screen_size

    @half_screen_size.setter
    def half_screen_size(self, value: Vector2) -> None:
        self._half_screen_size = value


@dataclass
class CameraShakeComponent:
    duration: float
    intensity: float

    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    def tick(self, delta: float) -> None:
        self.duration -= delta

    def random_offset(self) -> Vector2:
        return Vector2.new3(
            uniform(-self.intensity, self.intensity),
            uniform(-self.intensity, self.intensity),
        )
