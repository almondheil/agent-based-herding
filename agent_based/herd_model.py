#! usr/bin/python3

## Imports ##
# general packages
import math
import sys

# mesa-specific components
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

# agents with their own files because they're complex
from agent_based.prey import PreyAgent
from agent_based.predator import PredatorAgent

def compute_alive_prey(model):
    agents = model.schedule.agents
    for agent in agents:
        if str(type(agent))[-15:-2] == "PredatorAgent":
            agents.remove(agent)
        elif agent.alive == False:
            agents.remove(agent)
    return(len(agents))

class HerdModel(Model):
    def __init__(self, params, config, prey_data):
        self.config = config
        self.params = params
        self.prey_data = prey_data
        if self.config['seed'] != None:
            self.random.seed(self.config['seed'])
        
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
        self.datacollector = DataCollector(
            model_reporters = {"Alive": compute_alive_prey})

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
    
        
    def count_agents(self):
        return len(self.schedule.agents)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

