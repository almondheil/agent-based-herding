#! usr/bin/python3

## Imports ##
# general packages
import math
import sys

# mesa-specific components
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

# agents with their own files because they're complex
from agent_based.prey import PreyAgent
from agent_based.predator import PredatorAgent

class HerdModel(Model):
    def __init__(self, params, config, prey_data):
        self.config = config
        self.params = params
        self.prey_data = prey_data
        self.random.seed(78371649) # this should keep prey constant, but NOT placement code
        # I HATE IT. TODO: Fix literally all of this garbage

        self.num_predator = self.config['predator-number']
        self.num_prey = len(self.prey_data)
        self.width = self.config['width']
        self.height = self.config['height']
                
        self.space = ContinuousSpace(self.width, self.height, True)
        # create torus space with predefined width and height
        self.schedule = RandomActivation(self)
        # print("MODEL prey data %s" % (self.prey_data))
        self.make_agents(self.config, self.params, self.prey_data)
        self.running = True

    def make_agents(self, config, params, prey_data):
        # print(self.num_predator + self.num_prey)
        id = 0
        for i in range(int(self.num_predator)):
            a = PredatorAgent(id, self, config, params)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            # print('PredatorAgent placed at (%s, %s)' % (x, y))
            id += 1
        for i in range(int(self.num_prey)):
            a = PreyAgent(id, self, config, params)
            # print("LOCATION \n%s" % prey_data.loc[row])
            # print("LENGTH %s" % (len(prey_data) -1))
            # print("ITER %s" % i)
            x = prey_data.loc[i][0] 
            y = prey_data.loc[i][1]
            # locate the x and y in the prey_data DataFrame we generated already
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            # print('PreyAgent placed at (%s, %s)' % (x, y))
            id += 1
        # if params['verbose']: print("%i agents successfully added to model"
        #                             % (int(self.num_predator + self.num_prey)))

    def count_agents(self):
        return len(self.schedule.agents)

    def step(self):
        self.schedule.step()

