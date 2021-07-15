#! usr/bin/python3

## Imports ##
# general packages
import math
import sys

# mesa-specific components
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation


class PreyAgent(Agent):
    """A prey agent who herds with other prey
    and is attacked by predators"""
    def __init__(self, unique_id, model, config, params):
        super().__init__(unique_id, model)
        self.config = config
        self.params = params
        self.run_speed = self.config['prey-run-speed']
        self.stamina = self.config['prey-stamina']
        self.escape_distance = self.config['prey-escape-distance']
        self.vision = self.config['prey-vision']

    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        # print(len(visible))
        for neighbor in neighbors:
            if str(type(neighbor))[20:-2] == "PredatorAgent":
                # print("!! Prey %s %s sees a predator near it at %s!" % (self.unique_id, self.pos, neighbor.pos))
                pass
            
    def step(self):
        self.look()


class PredatorAgent(Agent):
    """A predator agent who attacks prey."""
    def __init__(self, unique_id, model, config, params):
        super().__init__(unique_id, model)
        self.config = config
        self.params = params
        self.run_speed = self.config['predator-run-speed']
        self.idle_speed = self.config['predator-idle-speed']
        self.stamina = self.config['predator-stamina']
        self.kill_radius = self.config['predator-kill-radius']
        self.vision = self.config['predator-vision']

    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        prey_visible = []
        for neighbor in neighbors:
            if str(type(neighbor))[20:-2] == "PreyAgent": # complicated way of getting a clean value for Prey
                if self.params['verbose']: print("Predator %s (%.2f, %.2f) sees a prey near it %s"
                                                 % (self.unique_id, self.pos[0], self.pos[1], neighbor.pos))
                prey_visible.append(neighbor)
                # print(prey_visible)
        if prey_visible:
            target = self.model.random.choice(prey_visible)
            self.chase_prey(target)
                # where do I go from here? I wanna random.choice() from any that are visible at the end of a look()
        
    def move_idle(self):
        """Do a random walk or move towards any prey you notice"""
        # print("Predator %s moves" % (self.unique_id))
        rotation = self.model.random.random() * 2 * math.pi
        distance = round(self.model.random.gauss(self.idle_speed, math.sqrt(self.idle_speed)), 1)
        for step in range(int(distance * 10)):
            current_x, current_y = self.pos
            new_x = current_x + (math.sin(rotation) * (distance/10))
            new_y = current_y + (math.cos(rotation) * (distance/10))
            new_pos = (new_x, new_y)
            if self.params['verbose']: print('Predator %s moving to (%.2f, %.2f) (step %s)' % (self.unique_id, new_x, new_y, step))
            self.model.space.move_agent(self, new_pos)
            self.look()

    def chase_prey(self, target):
        """After noticing a prey, chase it down. Possible outcomes include: 
            Catch up, secure kill; 
            Catch up, miss kill; 
            Don't catch up :(

        One issue I'm having is that it can randomly chase a different prey if it feels like it, so I may need to
        have a check against that
        
        Difference between prey initiated chase and predaotr initiated is that prey gets a full 
        (or maybe percentage) movement before alerting predator"""
        if self.params['verbose']: print("## Predator %s is chasing prey %s" % (self.unique_id, target.unique_id))
        """distance_to_target = 
        if distance_to_target <= self.run_speed:
            new_x, new_y = target.pos
        else:
            new
        new_pos = (new_x, new_y)"""
        # if self.params['verbose']: print('Predator %s moves to (%.2f, %.2f) in pursuit of prey %s'
                                         # % (self.unique_id, self.new_x, self.new_y, target.unique_id))
            
        # print(self.idle_speed)
        # print((rotation, distance))

    def step(self):
        self.move_idle()


class HerdModel(Model):
    def __init__(self, params, config, prey_data):
        self.config = config
        self.params = params
        self.prey_data = prey_data

        self.num_predator = self.config['predator-number']
        self.num_prey = len(self.prey_data)
        self.width = self.config['width']
        self.height = self.config['height']
                
        self.space = ContinuousSpace(self.width, self.height, True) # create torus space with predefined width and height
        self.schedule = RandomActivation(self)
        # print("MODEL prey data %s" % (self.prey_data))
        self.make_agents(self.config, self.params, self.prey_data)

    def make_agents(self, config, params, prey_data): # this is where I feed in the prey placement code and also add RANDOM predator placement
        # print(self.num_predator + self.num_prey)
        id = 0 # least confusing way I can come up with to have unique ID for each agent regardless of predator or prey
        for i in range(int(self.num_predator)):
            a = PredatorAgent(id, self, config, params)
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            # print('PredatorAgent placed at (%s, %s)' % (x, y)) # slice prints PredatorAgent or PreyAgent from class
            id += 1
        for i in range(int(self.num_prey)):
            a = PreyAgent(id, self, config, params)
            # print("LOCATION \n%s" % prey_data.loc[row])
            # print("LENGTH %s" % (len(prey_data) -1))
            # print("ITER %s" % i)
            x = prey_data.loc[i][0] # locate the x and y in the prey_data DataFrame we generated already
            y = prey_data.loc[i][1]
            self.schedule.add(a)
            self.space.place_agent(a, (x, y))
            # print('PreyAgent placed at (%s, %s)' % (x, y)) # slice prints PredatorAgent or PreyAgent from class
            id += 1
        if params['verbose']: print("Agents successfully added to model!")
        # print(prey_data)

    def step(self):
        self.schedule.step()
            

if __name__ == "__main__":
    main()

