import esper
from py4godot import gdclass
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.CharacterBody2D import CharacterBody2D


from ..components import *


@gdclass
class Player(CharacterBody2D):
    min_damage: float = 1
    max_damage: float = 10
    knockback_force: float = 200.0
    health: float = 100

    def _ready(self) -> None:
        self.hitbox = self.get_node("%HitBox")
        self.hurtbox = self.get_node("%HurtBox")
        animation_player: AnimationPlayer = self.get_node("%AnimationPlayer")

        animation = AnimationComponent(animation_player)
        input = InputComponent()
        body = BodyComponent(self)
        player = PlayerComponent()
        health = HealthComponent(self.health)
        velocity = VelocityComponent()
        state = StateComponent()
        facing = FacingComponent()

        hitbox = HitboxComponent(
            self.hitbox, (self.min_damage, self.max_damage), self.knockback_force
        )
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

        self.entity = ent
