import esper
from py4godot.classes.AnimationPlayer import AnimationPlayer

from components import (
    AnimationComponent,
    AnimationEventComponent,
    StateComponent,
    FacingComponent,
)


class AnimationSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        for ent, (anim, state, facing) in esper.get_components(
            AnimationComponent,
            StateComponent,
            FacingComponent,
        ):
            player: AnimationPlayer = anim.player

            # ---------------------------------------------------------
            # 1. Build animation name using your animation_string
            # ---------------------------------------------------------
            desired = f"{str(state.current)}_{facing.animation_string}"

            # ---------------------------------------------------------
            # 2. Update desired animation if changed
            # ---------------------------------------------------------
            if desired != anim.desired:
                anim.desired = desired

            # ---------------------------------------------------------
            # 3. If desired != current, switch animations
            # ---------------------------------------------------------
            if anim.desired != anim.current:
                anim.current = anim.desired
                anim.finished = False
                player.play(anim.current)
                player.set_speed_scale(anim.speed)

            # ---------------------------------------------------------
            # 4. Detect animation completion
            # ---------------------------------------------------------
            if not anim.finished and not player.is_playing():
                anim.finished = True

                if evt := esper.try_component(ent, AnimationEventComponent):
                    evt.finished = True
