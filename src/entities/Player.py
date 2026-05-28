import esper
from py4godot import gdclass
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.Area2D import Area2D

from components import (
    BodyComponent,
    PlayerComponent,
    HealthComponent,
    VelocityComponent,
    StateComponent,
    HitboxComponent,
    HurtboxComponent,
)


@gdclass
class Player(CharacterBody2D):
    hitbox: Area2D
    hurtbox: Area2D

    def _ready(self) -> None:
        body = BodyComponent(self)
        player = PlayerComponent()
        health = HealthComponent(100)
        velocity = VelocityComponent()
        state = StateComponent()

        hitbox = HitboxComponent(self.hitbox)
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            player,
            health,
            velocity,
            state,
            hitbox,
            hurtbox,
        )

        # Components handle stamping
        body.bind_entity(ent)
        player.bind_entity(ent)
        health.bind_entity(ent)
        velocity.bind_entity(ent)
        state.bind_entity(ent)
        hitbox.bind_entity(ent)
        hurtbox.bind_entity(ent)

        self.entity = ent
