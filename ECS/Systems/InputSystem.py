import esper
from py4godot.classes.Input import Input
from py4godot.classes.Node import Vector2

from ..components import (
    ATTACK,
    FACINGS,
    InputComponent,
    PlayerComponent,
    State,
    StateComponent,
    VelocityComponent,
)
import math


class InputSystem(esper.Processor):
    """
    The InputSystem should handle all use input and then respond by informing
    the proper components
    """

    def process(self, _delta: float) -> None:
        # delta is unused so we can delete it for now.
        del _delta

        # First get an instance of the input manager
        input_manager = Input.instance()

        # Get the basic movement input from the user
        input_vector: Vector2 = Vector2.new3(
            input_manager.get_axis("left", "right"),
            input_manager.get_axis("up", "down"),
        ).normalized()

        # Next we get the player and pass that on to them
        player_list = esper.get_component(PlayerComponent)
        if player_list:

            # Get the player
            player_id: int
            player_id, _ = player_list[0]

            # attack phase:
            # See if our player is attacking or intends to attack
            if (state := esper.try_component(player_id, StateComponent)) and (
                unhandled := esper.try_component(player_id, InputComponent)
            ):

                if state.current == State.ATTACK:
                    # Player is already attacking
                    # Do not accept any more movement input
                    # or attack input
                    input_vector = Vector2.ZERO
                    unhandled.queue.clear()

                attack_intent = False
                for evt in unhandled.queue:
                    if evt.is_action_pressed(ATTACK):
                        attack_intent = True
                        break
                unhandled.queue.clear()

                if attack_intent:
                    state.current = State.ATTACK
                    # Do not process any more until the other systems handle the attack.
                    return

            # movement phase:
            # If our player is not attacking or intending to attack move as normal
            if (vel := esper.try_component(player_id, VelocityComponent)) and (
                state := esper.try_component(player_id, StateComponent)
            ):
                vel.x = input_vector.x
                vel.y = input_vector.y

                if input_vector.length() > 0.0:
                    if state.current == State.IDLE:
                        state.current = State.WALK
                elif state.current == State.WALK:
                    state.current = State.IDLE

                # Update the player's cardinal_direction
                if input_vector.length() > 0.0:
                    # This is now automatically done by the StateComponent
                    state.cardinal_direction = input_vector
