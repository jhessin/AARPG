import esper
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.InputEvent import InputEvent
from py4godot.classes.AudioStream import AudioStream
from py4godot.classes.AudioStreamPlayer2D import AudioStreamPlayer2D
from py4godot.classes.Node2D import Node2D
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.ResourceLoader import ResourceLoader
from py4godot import gdclass, gdmethod, gdproperty
from py4godot.signals import Callable
from GeneralNodes.HitBox.HitBox import HitBox

from ECS.components import (
    ENTITY_ID,
    AnimationComponent,
    BodyComponent,
    HealthComponent,
    InputComponent,
    PlayerComponent,
    VelocityComponent,
    StateComponent,
    AudioComponent,
    ATTACK,
)


@gdclass
class Player(CharacterBody2D):
    decelerate_speed: float = gdproperty(float, 5.0)

    def __init__(self):
        super().__init__()
        self.entity = -1

    def _ready(self) -> None:
        sprite: Sprite2D = self.get_node("%PlayerSprite")
        animator: AnimationPlayer = self.get_node("%AnimationPlayer")
        self.audio_player: AudioStreamPlayer2D = self.get_node("%AudioPlayer")
        hit_box: HitBox = self.get_node("%HitBox").get_pyscript()
        weapon_pivot: Node2D = self.get_node("%WeaponPivot")
        sound_path: str = "res://Player/Audio/SwordSwoosh.wav"

        attack_sound: AudioStream = ResourceLoader.instance().load(sound_path)

        sounds: dict[str, AudioStream] = {ATTACK: attack_sound}

        self.entity = esper.create_entity(
            HealthComponent(
                self,
            ),
            VelocityComponent(),
            PlayerComponent(self),
            AnimationComponent(animator, sprite, weapon_pivot),
            BodyComponent(self),
            StateComponent(decelerate_speed=self.decelerate_speed),
            InputComponent(),
            AudioComponent(self.audio_player, sounds),
            hit_box.component,
        )
        self.set_meta(ENTITY_ID, str(self.entity))
        animator.animation_finished.connect(
            Callable.new2(self, "_on_animation_finished")
        )

        self.add_to_group("Player")

    def _unhandled_input(self, event: InputEvent) -> None:
        if input_cmp := esper.try_component(self.entity, InputComponent):
            input_cmp.queue.append(event.duplicate())

    @gdmethod
    def _on_animation_finished(self, anim_name: str) -> None:
        anim_name = str(anim_name)
        # Godot passes the name of the finished clip as a parameter
        if anim_name.startswith(ATTACK):
            if state := esper.try_component(self.entity, StateComponent):
                state.animation_is_finished = True
