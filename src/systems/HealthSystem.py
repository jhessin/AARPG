import esper

from ..components import *


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for ent, health in esper.get_component(HealthComponent):
            if health.dead:
                # Change state to death if there is a state component for it
                if ai := esper.try_component(ent, SimpleAIComponent):
                    ai.state = AIState.DEAD
