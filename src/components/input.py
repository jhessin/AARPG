from dataclasses import dataclass, field
from .util import clamp


@dataclass
class InputComponent:
    init_move_x: float = 0.0
    init_move_y: float = 0.0
    init_attack: bool = False
    init_dash: bool = False
    init_interact: bool = False
    _move_x: float = field(init=False, repr=False)
    _move_y: float = field(init=False, repr=False)
    _attack: bool = field(init=False, repr=False)
    _dash: bool = field(init=False, repr=False)
    _interact: bool = field(init=False, repr=False)
    _entity_id: int = field(init=False, repr=False)

    def __post_init__(self):
        self.move_x = self.init_move_x
        self.move_y = self.init_move_y
        self.attack = self.init_attack
        self.dash = self.init_dash
        self.interact = self.init_interact

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id

    @property
    def move_x(self) -> float:
        return self._move_x

    @move_x.setter
    def move_x(self, value: float):
        self._move_x = clamp(value, -1.0, 1.0)

    @property
    def move_y(self) -> float:
        return self._move_y

    @move_y.setter
    def move_y(self, value: float):
        self._move_y = clamp(value, -1.0, 1.0)

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
