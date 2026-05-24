import esper

from ECS.components import HealthComponent


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for _entity, health in esper.get_component(HealthComponent):
            del _entity
            if health.current <= 0:
                health.parent.queue_free()
