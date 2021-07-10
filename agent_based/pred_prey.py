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
''''''
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
