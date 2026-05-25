import esper


from py4godot.classes.core import Vector2
from ..components import (
    EnemyComponent,
    PlayerComponent,
    State,
    StateComponent,
    VelocityComponent,
)


class AISystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta
        player_list = esper.get_component(PlayerComponent)
        if not player_list:
            return

        _, player = player_list[0]

        player_pos = player.model.global_position

        for _enemy_ent, (enemy, vel, state) in esper.get_components(
            EnemyComponent, VelocityComponent, StateComponent
        ):
            del _enemy_ent
            if enemy.model.is_queued_for_deletion():
                continue

            # if enemy is attacking don't move him.
            if state.current == State.ATTACK:
                continue

            # see if the enemy is being knocked back
            if vel.direction.length() > vel.speed:
                continue

            enemy_pos = enemy.model.global_position
            diff = Vector2.new3(player_pos.x - enemy_pos.x, player_pos.y - enemy_pos.y)

            distance = diff.length()

            # Check if the enemy is close enough to attack
            if distance < enemy.attack_range:
                vel.direction = Vector2.ZERO

                # if the enemy has an attack animation place him in the attack state
                if enemy.has_attack:
                    state.current = State.ATTACK
                continue

            vel.direction = diff

            if state.current == State.IDLE:
                state.current = State.WALK
