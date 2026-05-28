from dataclasses import dataclass, field
from py4godot.classes.AnimationPlayer import AnimationPlayer
from .util import clamp


@dataclass
class AnimationComponent:
    player: AnimationPlayer
    init_desired: str = ""
    init_speed: float = 1.0
    _desired: str = field(init=False, repr=False)
    _current: str = field(default="", init=False, repr=False)
    _speed: float = field(init=False, repr=False)
    _finished: bool = field(default=False, init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self.desired = self.init_desired
        self.speed = self.init_speed

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def desired(self) -> str:
        return self._desired

    @desired.setter
    def desired(self, value: str):
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
        self._speed = clamp(value, 0.1, 4.0)

    @property
    def finished(self) -> bool:
        return self._finished

    @finished.setter
    def finished(self, value: bool):
        self._finished = bool(value)
