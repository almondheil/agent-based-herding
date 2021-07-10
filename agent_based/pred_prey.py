#! usr/bin/python3

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
# from mesa.datacollection import DataCollector
# from mesa.batchrunner import BatchRunner

class PreyAgent(Agent):
    """A prey agent who herds with other prey 
    and is attacked by predators"""
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y

    def move(self):
        print("Prey %s moves." % (self.unique_id))

    def step(self):
        self.move()


class PredatorAgent(Agent):
    """A predator agent who attacks prey."""
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        
    def move(self):
        print("Predator %s moves." % (self.unique_id))

    def step(self):
        self.move()


class HerdModel(Model):
    def __init__(self, N_predator, N_prey, width, height):
        self.num_predator = N_predator
        self.num_prey = N_prey
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.make_agents()

    def make_agents(self):
        for i in range(self.num_predator):
            print("Predator %s placed" % i)
        for i in range(self.num_prey):
            print("Prey %s placed" % i)
