import esper
from py4godot import gdclass
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.Area2D import Area2D
from py4godot.classes.CollisionShape2D import CollisionShape2D

from ..components import (
    BodyComponent,
    EnemyComponent,
    HealthComponent,
    VelocityComponent,
    SimpleAIComponent,
    HitboxComponent,
    HurtboxComponent,
    AnimationComponent,
    FacingComponent,
)


@gdclass
class Slime(CharacterBody2D):
    health: float = 10
    min_damage: float = 1
    max_damage: float = 10
    speed: float = 30.0
    min_state_cycles: int = 1
    max_state_cycles: int = 2

    def _ready(self) -> None:
        self.hitbox = self.get_node("%HitBox")
        self.hurtbox = self.get_node("%HurtBox")

        body = BodyComponent(self)
        enemy = EnemyComponent()
        health = HealthComponent(self.health)
        velocity = VelocityComponent(self.speed)
        ai = SimpleAIComponent(
            min_state_cycles=self.min_state_cycles,
            max_state_cycles=self.max_state_cycles,
        )
        animation = AnimationComponent(self.get_node("%Animator"))
        collider: CollisionShape2D = self.get_node("%Collider")
        facing = FacingComponent()

        def new_collider() -> CollisionShape2D:
            return collider.duplicate(7)

        self.hitbox.add_child(new_collider())
        self.hurtbox.add_child(new_collider())

        hitbox = HitboxComponent(self.hitbox, (self.min_damage, self.max_damage))
        hurtbox = HurtboxComponent(self.hurtbox)

        ent = esper.create_entity(
            body,
            enemy,
            health,
            velocity,
            ai,
            hitbox,
            hurtbox,
            animation,
            facing,
        )

        body.bind_entity(ent)
        enemy.bind_entity(ent)
        health.bind_entity(ent)
        velocity.bind_entity(ent)
        ai.bind_entity(ent)
        hitbox.bind_entity(ent)
        hurtbox.bind_entity(ent)
        animation.bind_entity(ent)
        facing.bind_entity(ent)

        self.entity = ent
