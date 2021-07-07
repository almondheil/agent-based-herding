#! usr/bin/python3

""" Use Coding/mesa/examples/boid_flockers for info as you do this. He has continuout space Boids """

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from .predator import Predator # I need to write these ofc but I guess they need to happen at some point
from .prey import Prey

class PredPrey(Model):
    def __init__(
        self,
        population = 100,
        width = 100,
        height = 100,
        comfort_average = 10,
        comfort_variation = 3,
        placement_attempts = 500,
        # add other configuration settings here, then have them be imported with the function you already wrote.
        # they DO apply to the agents in the original code, it seems.
    ):
        self.population = population
        self.width = width
        self.height = height
        self.comfort_average = comfort_average
        self.comfort_variation = comfort_variation
        self.placement_attempts = placement_attempts
        self.make_agents()
        self.running = True

    def make_agents(self):
        for i in range(self.population):
            pos = place_individual() # TODO: make place_individual return a np.array((x, y)) instead of printing
        
