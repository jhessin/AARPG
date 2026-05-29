import esper
from py4godot import gdclass
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.Area2D import Area2D
from py4godot.classes.ResourceLoader import ResourceLoader


from ..components import (
    BodyComponent,
    PlayerComponent,
    HealthComponent,
    VelocityComponent,
    StateComponent,
    HitboxComponent,
    HurtboxComponent,
    InputComponent,
    AnimationComponent,
    FacingComponent,
    AudioComponent,
    ATTACK,
)


@gdclass
class Player(CharacterBody2D):
    hitbox: Area2D
    hurtbox: Area2D

    def _ready(self) -> None:
        if not self.hitbox:
            self.hitbox = self.get_node("%HitBox")
        if not self.hurtbox:
            self.hurtbox = self.get_node("%HurtBox")
        animation_player: AnimationPlayer = self.get_node("%AnimationPlayer")

        animation = AnimationComponent(animation_player)
        input = InputComponent()
        body = BodyComponent(self)
        player = PlayerComponent()
        health = HealthComponent(100)
        velocity = VelocityComponent()
        state = StateComponent()
        facing = FacingComponent()
        audio = AudioComponent(
            {
                ATTACK: ResourceLoader.instance().load(
                    "res://src/assets/sounds/SwordSwoosh.wav"
                )
            }
        )

        hitbox = HitboxComponent(self.hitbox)
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            animation,
            player,
            health,
            velocity,
            state,
            hitbox,
            hurtbox,
            input,
            facing,
            audio,
        )

        # Components handle stamping
        body.bind_entity(ent)
        animation.bind_entity(ent)
        input.bind_entity(ent)
        player.bind_entity(ent)
        health.bind_entity(ent)
        velocity.bind_entity(ent)
        state.bind_entity(ent)
        hitbox.bind_entity(ent)
        hurtbox.bind_entity(ent)
        facing.bind_entity(ent)
        audio.bind_entity(ent)

        self.entity = ent
