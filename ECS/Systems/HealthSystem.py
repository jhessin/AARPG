import esper

from ECS.components import HealthComponent


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for entity, health in esper.get_component(HealthComponent):
            if health.current <= 0 and not health.parent.is_queued_for_deletion():
                health.parent.queue_free()
                esper.delete_entity(entity)
