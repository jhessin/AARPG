# CleanupSystem
import esper
from ..components import *


class CleanupSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        for ent, (health, body, anim) in esper.get_components(
            HealthComponent,
            BodyComponent,
            AnimationEventComponent,
        ):
            if health.dead and anim.finished:
                body.body.queue_free()
                esper.delete_entity(ent)
