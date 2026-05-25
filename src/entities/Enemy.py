import esper
from py4godot.classes.AnimationPlayer import AnimationPlayer
from py4godot.classes.CollisionShape2D import CollisionShape2D
from py4godot.classes.Sprite2D import Sprite2D
from py4godot.classes.Area2D import Area2D
from py4godot.classes import gdclass
from py4godot.classes.CharacterBody2D import CharacterBody2D

from ..components import (
    ENTITY_ID,
    AnimationComponent,
    BodyComponent,
    EnemyComponent,
    HealthComponent,
    StateComponent,
    VelocityComponent,
    HitboxComponent,
)


@gdclass
class Enemy(CharacterBody2D):

    def _ready(self) -> None:
        animator: AnimationPlayer = self.get_node("%Animator")
        sprite: Sprite2D = self.get_node("%Sprite")

        def new_shape() -> CollisionShape2D:
            collider: CollisionShape2D = CollisionShape2D.cast(
                self.get_node("%Collider")
            )
            return collider.duplicate(7)

        hurtbox: Area2D = Area2D.cast(self.get_node("%HurtBox"))
        hitbox: Area2D = Area2D.cast(self.get_node("%HitBox"))

        hurtbox.add_child(new_shape())
        hitbox.add_child(new_shape())

        self.entity = esper.create_entity(
            HitboxComponent(hitbox),
            HealthComponent(self, 50),
            StateComponent(),
            AnimationComponent(animator, sprite),
            VelocityComponent(speed=50),
            BodyComponent(self),
            EnemyComponent(self, 10.0),
        )

        self.set_meta(ENTITY_ID, str(self.entity))
        sprite.set_meta(ENTITY_ID, str(self.entity))
        hitbox.set_meta(ENTITY_ID, str(self.entity))
        hurtbox.set_meta(ENTITY_ID, str(self.entity))

        self.add_to_group("Enemy")
