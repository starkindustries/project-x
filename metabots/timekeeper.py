from .metabolism import Metabolism

class Timekeeper:
  def __init__(self):
    self.metabolic_entities = []
    self.time = 0

  def track_metabolism(self, metabolism:Metabolism):
    self.metabolic_entities.append(metabolism)

  def tick(self, time = 1):
    self.time += time

    for metabolism in self.metabolic_entities:
      metabolism.tick(time)

