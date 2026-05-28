from dataclasses import dataclass, field


@dataclass
class PlayerComponent:
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id


@dataclass
class EnemyComponent:
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id
