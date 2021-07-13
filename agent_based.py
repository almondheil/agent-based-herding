#! usr/bin/python3

'''
    $NAME: Agent-based Monte Carlo modeling of herding dynamics.
    Copyright (C) 2021 Raymond Heil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import math
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
import prey_distribution_montecarlo as prey_place
# from mesa.datacollection import DataCollector
# from mesa.batchrunner import BatchRunner


class PreyAgent(Agent):
    """A prey agent who herds with other prey
    and is attacked by predators"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        print("Prey %s moves." % (self.unique_id))
        
        
    def step(self):
        self.move()


class PredatorAgent(Agent):
    """A predator agent who attacks prey."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def move(self):
        """Do a random walk or move towards any prey you notice"""
        print("Predator %s moves." % (self.unique_id))

    def step(self):
        self.move()


class HerdModel(Model):
    def __init__(self, N_predator, N_prey, width, height):
        self.num_predator = N_predator
        self.num_prey = N_prey
        self.width = width
        self.height = height
        self.space = ContinuousSpace(width, height, True) # create torus space with predefined width and height
        self.schedule = RandomActivation(self)
        self.make_agents()


    def make_agents(self): # this is where I feed in the prey placement code and also add RANDOM predator placement
        for i in range(self.num_predator + self.num_prey):
            if i < self.num_predator:
                a = PredatorAgent(i, self)
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            else: # TODO: feed in the locations we've tried so hard to generate, rather than doing this randomly
                a = PreyAgent(i, self)
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            print('%s placed at (%s, %s)' % (str(type(a))[20:-2], x, y)) # slice prints PredatorAgent or PreyAgent from class
            

    def step(self):
        self.schedule.step()



if __name__ == "__main__":
    main()

