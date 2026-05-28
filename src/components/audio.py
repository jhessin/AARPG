from dataclasses import dataclass, field
from typing import Dict
from py4godot.classes.AudioStream import AudioStream


@dataclass
class AudioComponent:
    sounds: Dict[str, AudioStream] = field(default_factory=dict)
    current_key: str = ""
    _entity_id: int = field(init=False, repr=False)

    def bind_entity(self, entity_id: int) -> None:
        self._entity_id = entity_id

    @property
    def id(self) -> int:
        return self._entity_id
