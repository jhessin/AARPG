import esper

from ..components import StateComponent, InputComponent, State


class StateSystem(esper.Processor):
    def process(self, _delta: float):
        del _delta

        for _, (state, input) in esper.get_components(StateComponent, InputComponent):

            # Attack overrides everything
            if input.attack:
                if state.current != State.ATTACK:
                    state.current = State.ATTACK
                continue

            # Movement
            if input.move_x or input.move_y:
                if state.current != State.WALK:
                    state.current = State.WALK
                continue

            # Idle fallback
            if state.current != State.IDLE:
                state.current = State.IDLE
