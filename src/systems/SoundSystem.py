import esper
from random import uniform

from ..components import AudioComponent, State, StateComponent, ATTACK


class SoundSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for _, (state, audio) in esper.get_components(StateComponent, AudioComponent):

            if state.current == State.ATTACK:
                if audio.current_key != ATTACK:
                    if attack_sound := audio.sounds.get(ATTACK):
                        if audio.player.get_stream() != attack_sound:
                            audio.player.stream = attack_sound
                        audio.player.pitch_scale = uniform(0.9, 1.1)
                        audio.player.play()
                        audio.current_key = ATTACK
            elif audio.current_key == ATTACK:
                # if the player is no longer attacking but the audio tag is active
                audio.current_key = ""
                # with one-shot sounds this is unnecessary.
                # audio.player.stop()
                # This crashes py4godot
                # audio.player.stream = None
