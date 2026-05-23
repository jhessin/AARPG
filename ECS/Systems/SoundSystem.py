import esper

from ECS.components import AudioComponent, PlayerState, StateComponent, ATTACK


class SoundSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        for _, (state, audio) in esper.get_components(StateComponent, AudioComponent):

            if state.current == PlayerState.ATTACK:
                if audio.current_key != "attack":
                    if attack_sound := audio.sounds.get("attack"):
                        if audio.player.get_stream() != attack_sound:
                            audio.player.stream = attack_sound
                        audio.player.play()
                        audio.current_key = ATTACK
            else:
                # if the player is no longer attacking but the audio tag is active
                if audio.current_key == "attack":
                    audio.player.stop()
                    # This crashes py4godot
                    # audio.player.stream = None
                    audio.current_key = ""
