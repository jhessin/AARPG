from random import randint
import esper


from py4godot.classes.Node2D import Node2D
from py4godot.classes.CharacterBody2D import CharacterBody2D
from py4godot.classes.core import Vector2
from ..components import (
    AIComponent,
    AIState,
    BodyComponent,
    PlayerComponent,
    VelocityComponent,
    SimpleAIComponent,
    FACINGS,
)


class AISystem(esper.Processor):
    def process(self, delta: float) -> None:
        player_list = esper.get_component(PlayerComponent)
        if not player_list:
            return

        player: int
        player, _ = player_list[0]
        player_body: Node2D = esper.component_for_entity(player, BodyComponent).body
        player_pos: Vector2 = player_body.global_position

        # Loop through simple AI enemies
        for _, (ai, body, vel) in esper.get_components(
            SimpleAIComponent, BodyComponent, VelocityComponent
        ):
            ai.tick(delta)
            pos = body.body.global_position

            # Simple State Logic
            match ai.state:
                case AIState.IDLE:
                    vel.direction = Vector2.ZERO
                case AIState.WANDER:
                    direction = randint(0, 3)
                    if vel.direction == Vector2.ZERO:
                        vel.direction = FACINGS[direction]

        # Loop through all enemies with AI
        for _, (ai, body, vel) in esper.get_components(
            AIComponent, BodyComponent, VelocityComponent
        ):
            ai.tick(delta)
            pos = body.body.global_position

            # Distance to player
            to_player = player_pos - pos
            dist = to_player.length()

            # --- STATE LOGIC ---
            #
            match ai.state:
                # 1. IDLE -> CHASE
                case AIState.IDLE | AIState.WANDER:
                    if dist < ai.aggro_range:
                        ai.state = AIState.CHASE
                        ai.target_entity = player

                # 2. CHASE -> ATTACK or RETURN
                case AIState.CHASE:
                    if dist < ai.attack_range:
                        ai.state = AIState.ATTACK
                    elif dist > ai.aggro_range * 1.5:
                        ai.state = AIState.RETURN

                # 3. ATTACK -> CHASE (after bump)
                case AIState.ATTACK:
                    # Slime attacks by bumping; CombatSystem handles damage
                    # After attacking, go back to chase
                    # TODO: Place check here to see if the attack has finished for future enemies.
                    ai.state = AIState.CHASE

                # 4. RETURN -> IDLE
                case AIState.RETURN:
                    home = ai.spawn
                    to_home = home - pos
                    if to_home.length() < 4:
                        ai.state = AIState.IDLE

            # --- MOVEMENT LOGIC ---
            match ai.state:
                case AIState.CHASE:
                    vel.direction = to_player.normalized()
                case AIState.RETURN:
                    vel.direction = (ai.spawn - pos).normalized()
                case _:
                    vel.direction = Vector2.ZERO
