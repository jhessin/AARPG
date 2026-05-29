import esper
from random import uniform
from py4godot.classes.AudioStreamPlayer2D import AudioStreamPlayer2D
from py4godot.classes.Node2D import Node2D

from ..components import (
    AudioComponent,
    State,
    StateComponent,
    ATTACK,
    PlayerComponent,
    BodyComponent,
)


class SoundSystem(esper.Processor):

    def process(self, _delta: float) -> None:
        del _delta
        player: int | None = None
        body_comp: BodyComponent | None = None
        player_body: Node2D | None = None
        audio_player: AudioStreamPlayer2D | None = None

        if player_list := esper.get_component(PlayerComponent):
            player, _ = player_list[0]

        if (
            player
            and (body_comp := esper.try_component(player, BodyComponent))
            and (player_body := body_comp.body)
        ):
            audio_player = player_body.get_node("%AudioPlayer")

        if not audio_player:
            print("❌❌❌ AudioStreamPlayer2D NOT FOUND!!! ❌❌❌")
            return

        for _, (state, audio) in esper.get_components(StateComponent, AudioComponent):

            if state.current == State.ATTACK:
                if audio.current_key != ATTACK:
                    if attack_sound := audio.sounds.get(ATTACK):
                        if audio_player.get_stream() != attack_sound:
                            audio_player.set_stream(attack_sound)
                        audio_player.pitch_scale = uniform(0.9, 1.1)
                        audio_player.play()
                        audio.current_key = ATTACK
                    else:
                        print("ATTACK SOUND NOT FOUND!")
            elif audio.current_key == ATTACK:
                # if the player is no longer attacking but the audio tag is active
                audio.current_key = ""
                # with one-shot sounds this is unnecessary.
                # audio.player.stop()
                # This crashes py4godot
                # audio.player.stream = None
