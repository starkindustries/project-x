# from .logger import Logger 
from . import logger as Logger

# https://pypi.org/project/xstate/

class Metabolism:
  def __init__(self, lifecyle_stages = []):
    """
    a metabolic entity that receives resources (i.e. time, food) every simulation tick.
    tracks its internal state of resources to progress lifecycle stage
    """
    # Logger.info('Metabolism')

    self.age = 0
    self.lifecyle_stages = lifecyle_stages

  def tick(self, time):
    """
    call once per fixed update 
    """
    self.age += time
    self.update_lifecycle()

  def set_lifecycle_stage(self, name, progression):
    # TODO define finite state machine for lifecycle progression
    Logger.info('set_lifecycle_stage')

  def update_lifecycle(self):
    # TODO check if state machine progresses
    Logger.info('update_lifecycle')

class Potato(Metabolism):
  def __init__(self):
    Metabolism.__init__(self)


class Android(Metabolism):
  def __init__(self):
    Metabolism.__init__(self)