import math
import esper

from random import random, uniform

from py4godot.classes.core import Vector2
from ECS.components import (
    BodyComponent,
    EnemyComponent,
    PlayerComponent,
    State,
    StateComponent,
    VelocityComponent,
)


class AISystem(esper.Processor):
    def process(self, delta: float) -> None:

        player_list = esper.get_component(PlayerComponent)
        if not player_list:
            return

        _, player = player_list[0]

        player_pos = player.model.global_position

        for enemy_ent, (enemy, vel, state) in esper.get_components(
            EnemyComponent, VelocityComponent, StateComponent
        ):
            if enemy.model.is_queued_for_deletion():
                continue

            # if enemy is attacking don't move him.
            if state.current == State.ATTACK:
                continue

            enemy_pos = enemy.model.global_position
            diff_x = player_pos.x - enemy_pos.x
            diff_y = player_pos.y - enemy_pos.y

            distance = math.sqrt(diff_x**2 + diff_y**2)

            # Check if the enemy is close enough to attack
            if distance < enemy.attack_range:
                vel.x = 0.0
                vel.y = 0.0

                # if the enemy has an attack animation place him in the attack state
                if enemy.has_attack:
                    state.current = State.ATTACK
                continue

            vel.x = diff_x / distance
            vel.y = diff_y / distance

            if state.current == State.IDLE:
                state.current = State.WALK
