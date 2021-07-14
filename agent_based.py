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


## Imports ##
# general packages
import math
import pandas as pd
import sys

# mesa-specific components
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation


# TODO: need to read in points, maybe from CSV but maybe from live session somehow
# it may also be helpful to read in the parameters the user does command-line like -q and -y


class PreyAgent(Agent):
    """A prey agent who herds with other prey
    and is attacked by predators"""
    def __init__(self, unique_id, model, config):
        super().__init__(unique_id, model)
        self.config = config

    def look(self):
        visible = self.model.space.get_neighbors(self.pos, self.config['prey-vision'])
        # print(len(visible))
        for agent in visible:
            if str(type(agent))[20:-7] == "Predator":
                print("!! Prey %s %s sees a predator near it at %s!" % (self.unique_id, self.pos, agent.pos))
            else:
                # print("Prey %s %s sees another prey near it at %s" % (self.unique_id, self.pos, agent.pos))
                pass
            # that garble gets the name of the thing it sees in lowercase, type(agent) gives you a bunch of <module.NameHere> garbo
        
    def step(self):
        self.look()


class PredatorAgent(Agent):
    """A predator agent who attacks prey."""
    def __init__(self, unique_id, model, config):
        super().__init__(unique_id, model)
        self.config = config
        
    def move(self):
        """Do a random walk or move towards any prey you notice"""
        # print("Predator %s moves (but not really I haven't coded that yet)." % (self.unique_id))
        pass

    def step(self):
        self.move()


class HerdModel(Model):
    def __init__(self, config, N_predator, prey_data, width, height):
        self.num_predator = N_predator
        self.prey_data = prey_data
        self.num_prey = len(self.prey_data)
        self.width = width
        self.height = height
        self.config = config
        
        self.space = ContinuousSpace(width, height, True) # create torus space with predefined width and height
        self.schedule = RandomActivation(self)
        # print("MODEL prey data %s" % (self.prey_data))
        self.make_agents(config, self.prey_data)

    def make_agents(self, config, prey_data): # this is where I feed in the prey placement code and also add RANDOM predator placement
        # print(self.num_predator + self.num_prey)
        id = 0 # least confusing way I can come up with to have unique ID for each agent regardless of predator or prey
        for i in range(int(self.num_predator)):
            a = PredatorAgent(id, self, config)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            print('PredatorAgent placed at (%s, %s)' % (x, y)) # slice prints PredatorAgent or PreyAgent from class
            id += 1
        for i in range(int(self.num_prey)):
            a = PreyAgent(id, self, config)
            # print("LOCATION \n%s" % prey_data.loc[row])
            # print("LENGTH %s" % (len(prey_data) -1))
            # print("ITER %s" % i)
            x = prey_data.loc[i][0] # locate the x and y in the prey_data DataFrame we generated already
            y = prey_data.loc[i][1]
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            print('PreyAgent placed at (%s, %s)' % (x, y)) # slice prints PredatorAgent or PreyAgent from class
            id += 1
        # print(prey_data)

    def step(self):
        self.schedule.step()
            

if __name__ == "__main__":
    main()

