import esper


class AISystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
