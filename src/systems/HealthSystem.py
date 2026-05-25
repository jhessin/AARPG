import esper

from ..components import HealthComponent


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for entity, health in esper.get_component(HealthComponent):

            # Only kill things that aren't dead already.
            # This will later be changed to utilize a spawning system
            if health.current <= 0 and not health.parent.is_queued_for_deletion():
                # First remove it from godot
                health.parent.queue_free()

                # Then remove it from esper
                esper.delete_entity(entity)
