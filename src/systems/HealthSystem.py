import esper

from components import (
    HealthComponent,
)
from components.movement import BodyComponent


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        # Reserve for future use
