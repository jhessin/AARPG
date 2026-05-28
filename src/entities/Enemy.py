import esper
from py4godot import gdclass
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.Area2D import Area2D

from components import (
    BodyComponent,
    EnemyComponent,
    HealthComponent,
    VelocityComponent,
    StateComponent,
    AIComponent,
    HitboxComponent,
    HurtboxComponent,
)


@gdclass
class Enemy(CharacterBody2D):
    hitbox: Area2D
    hurtbox: Area2D

    def _ready(self) -> None:
        body = BodyComponent(self)
        enemy = EnemyComponent()
        health = HealthComponent(30)
        velocity = VelocityComponent()
        state = StateComponent()
        ai = AIComponent()

        hitbox = HitboxComponent(self.hitbox)
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            enemy,
            health,
            velocity,
            state,
            ai,
            hitbox,
            hurtbox,
        )

        body.bind_entity(ent)
        enemy.bind_entity(ent)
        health.bind_entity(ent)
        velocity.bind_entity(ent)
        state.bind_entity(ent)
        ai.bind_entity(ent)
        hitbox.bind_entity(ent)
        hurtbox.bind_entity(ent)

        self.entity = ent
