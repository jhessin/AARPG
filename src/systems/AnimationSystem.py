from typing import Optional
import esper
from py4godot.classes.AnimationPlayer import AnimationPlayer


from ..components import *


class AnimationSystem(esper.Processor):
    def process(self, _delta: float) -> None:
        del _delta

        # This is for AI animation
        for ent, (anim, facing) in esper.get_components(
            AnimationComponent,
            FacingComponent,
        ):
            player: AnimationPlayer = anim.player

            # ---------------------------------------------------------
            # 1. Build animation name using your animation_string
            # ---------------------------------------------------------
            desired: Optional[str] = None
            if state := esper.try_component(ent, AIComponent) or (
                state := esper.try_component(ent, SimpleAIComponent)
            ):
                desired = f"{(state.state)}_{facing.animation_string}"
            elif state := esper.try_component(ent, StateComponent):
                desired = f"{(state.current)}_{facing.animation_string}"
            else:
                continue

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
                if evt := esper.try_component(ent, AnimationEventComponent):
                    evt.finished = False
                else:
                    evt = AnimationEventComponent(False)
                    esper.add_component(ent, evt)
                player.play(anim.current)
                player.set_speed_scale(anim.speed)

            # ---------------------------------------------------------
            # 4. Detect animation completion
            # ---------------------------------------------------------
            if not anim.finished and not player.is_playing():
                anim.finished = True

                if evt := esper.try_component(ent, AnimationEventComponent):
                    evt.finished = True
                else:
                    evt = AnimationEventComponent(True)
                    esper.add_component(ent, evt)
