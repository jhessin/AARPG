# CleanupSystem
import esper
from ..components import HealthComponent, BodyComponent


class CleanupSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        for ent, (health, body) in esper.get_components(
            HealthComponent,
            BodyComponent,
        ):
            if health.dead:
                body.body.queue_free()
                esper.delete_entity(ent)
