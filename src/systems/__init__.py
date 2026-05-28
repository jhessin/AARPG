import esper

from AISystem import *
from AnimationSystem import *
from CameraSystem import *
from CleanupSystem import *
from CombatSystem import *
from FacingSystem import *
from HealthSystem import *
from InputSystem import *
from MovementSystem import *
from SoundSystem import *


def init_systems():
    esper.add_processor(AISystem())
    esper.add_processor(AnimationSystem())
    esper.add_processor(CameraSystem())
    esper.add_processor(CombatSystem())
    esper.add_processor(FacingSystem())
    esper.add_processor(HealthSystem())
    esper.add_processor(InputSystem())
    esper.add_processor(MovementSystem())
    esper.add_processor(SoundSystem())
