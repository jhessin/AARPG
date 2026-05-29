import esper


class HealthSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        # Reserve for future use
