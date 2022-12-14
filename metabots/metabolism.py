# from .logger import Logger
from . import logger as Logger

# https://pypi.org/project/xstate/

SEED = "."
SEEDLING = ","
SPROUT = "i"
POTATO = "p"


class Metabolism:
    def __init__(self, age_seconds=0, lifecycle_stages=[]):
        """
        a metabolic entity that receives resources (i.e. time, food) every simulation tick.
        tracks its internal state of resources to progress lifecycle stage
        """
        # Logger.info('Metabolism')
        self.age_seconds = age_seconds
        self.lifecycle_stages = lifecycle_stages

    def tick(self, delta):
        """
        call once per fixed update 
        """
        self.age_seconds += delta
        # self.update_lifecycle()

    def set_lifecycle_stage(self, name, progression):
        # TODO define finite state machine for lifecycle progression        
        Logger.info('set_lifecycle_stage')

    def update_lifecycle(self):
        # TODO check if state machine progresses
        for stage in lifecycle_stages:
            # [(SEED, 30), (SEEDLING, 40), (SPROUT, 50), (POTATO, 60)]
            stage_icon, age = stage
        Logger.info('update_lifecycle')

    def get_current_lifecycle(self):
        Logger.info('get_current_lifecycle')
        if self.age_seconds >= self.lifecycle_stages[-1][1]:
            return self.lifecycle_stages[-1][0]
        for stage in self.lifecycle_stages:
            # [(SEED, 30), (SEEDLING, 40), (SPROUT, 50), (POTATO, 60)]
            stage_sprite, age_seconds = stage
            if self.age_seconds <= age_seconds:
                return stage_sprite


class Potato(Metabolism):

    # self.position = (x, y)

    def __init__(self, position):
        stages = [(SEED, 5), (SEEDLING, 6), (SPROUT, 7), (POTATO, 8)]
        Metabolism.__init__(self, 0, stages)
        self.position = position


class Android(Metabolism):
    def __init__(self):
        Metabolism.__init__(self)
