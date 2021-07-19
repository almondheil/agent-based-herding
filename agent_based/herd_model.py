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
        self.run_speed = self.random.gauss(
            self.config['prey-run-speed'],
            math.sqrt(self.config['prey-run-speed']))
        self.stamina = self.random.gauss(
            self.config['prey-stamina'],
            math.sqrt(self.config['prey-stamina']))
        self.current_stamina = self.stamina
        self.escape_distance = self.random.gauss(
            self.config['prey-escape-distance'],
            math.sqrt(self.config['prey-escape-distance']))
        self.vision = self.random.gauss(
            self.config['prey-vision'],
            math.sqrt(self.config['prey-vision']))

    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        # print(len(visible))
        for neighbor in neighbors:
            if str(type(neighbor))[-15:-2] == "PredatorAgent": 
                if self.params['verbose']:
                    print("see: prey %s (%.2f, %.2f) sees a predator at (%.2f, %.2f)"
                          % (self.unique_id, self.pos[0], self.pos[1],
                             neighbor.pos[0], neighbor.pos[1]))
                self.flee_predator(neighbor)

    def flee_predator(self, predator):
        if self.params['verbose']:
            print("chase: Prey %s (%.2f, %.2f) is fleeing predator (%.2f, %.2f)"
                  % (self.unique_id, self.pos[0], self.pos[1],
                     predator.pos[0], predator.pos[1]))
            
    def step(self):
        self.look()


class PredatorAgent(Agent):
    """A predator agent who attacks prey."""
    def __init__(self, unique_id, model, config, params):
        super().__init__(unique_id, model)
        self.config = config
        self.params = params
        self.run_speed = self.random.gauss(
            self.config['predator-run-speed'],
            math.sqrt(self.config['predator-run-speed']))
        self.idle_speed = self.random.gauss(
            self.config['predator-idle-speed'],
            math.sqrt(self.config['predator-idle-speed']))
        self.stamina = self.random.gauss(
            self.config['predator-stamina'],

            math.sqrt(self.config['predator-stamina']))
        self.kill_radius = self.random.gauss(
            self.config['predator-kill-radius'],
            math.sqrt(self.config['predator-kill-radius']))
        self.vision = self.random.gauss(
            self.config['predator-vision'],
            math.sqrt(self.config['predator-vision']))
        # print("predvis %s: %s" % (self.unique_id, self.vision))

    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        prey_visible = []
        for neighbor in neighbors:
            if str(type(neighbor))[-11:-2] == "PreyAgent":
                # I tried using a slice of the string to get "PreyAgent"
                # but it broke, it's not that ugly anway
                prey_visible.append(neighbor)
                if self.params['verbose']:
                    print("see: predator %s (%.2f, %.2f) sees prey at %s"
                          % (self.unique_id, self.pos[0], self.pos[1],
                             neighbor.pos))
        if prey_visible: # run only if there are items in the list
            distances_to_prey = {}
            for prey in prey_visible:
                print("prey_pos: (%.2f, %.2f) for predator %s" % (prey.pos[0], prey.pos[1], self.unique_id))
                heading = self.model.space.get_heading(self.pos, prey.pos)
                if not self.params['verbose']:
                    print(heading)
                # distance = self.model.space.get_distance(self, prey_pos)
                # distances_to_prey[prey_pos] = distance # FIXME: if 2+ prey are in the same position,
                                                       # the first ones we check get overwritten.
            if self.params['verbose']:
                print("distances_to_prey %s" % distances_to_prey)
                print("predvis %s: %s currently visible"
                      % (self.unique_id, len(prey_visible)))
            """distances_to_prey = {}
            for prey in prey_visible:
                distance
            target = self.random.choices(prey_visible.keys(),
                                               prey_visible.values(),
                                               k=1)
            self.chase_prey(target)"""
                # where do I go from here? I wanna random.choice() from any that are visible at the end of a look()
        
    def move_idle(self):
        """Do a random walk or move towards any prey you notice"""
        # print("Predator %s moves" % (self.unique_id))
        rotation = self.random.random() * 2 * math.pi
        distance = round(max(self.random.gauss(self.idle_speed, math.sqrt(self.idle_speed)), 1), 0)
        # max() function necessary to make sure we don't go below 0.
        # could come up other places too, but it's much less likely
        for step in range(int(distance * 10)):
            current_x, current_y = self.pos
            new_x = current_x + (math.sin(rotation) * (distance/10))
            new_y = current_y + (math.cos(rotation) * (distance/10))
            new_pos = (new_x, new_y)
            if self.params['verbose']:
                print('move: Predator %s moving to (%.2f, %.2f) (step %s)'
                      % (self.unique_id, new_x, new_y, step))
            self.model.space.move_agent(self, new_pos)
            self.look()

    def chase_prey(self, target):
        """After noticing a prey, chase it down. 
        Possible outcomes include: 
            Catch up, secure kill; 
            Catch up, miss kill; 
            Don't catch up :(
        
        Difference between prey initiated chase and predator initiated
        is that prey gets a full (or maybe percentage) movement before
        alerting predator"""
        if self.params['verbose']:
            print("chase: predator %s is chasing prey %s"
                  % (self.unique_id, target.unique_id))
        dx = abs(self.pos[0] - target.pos[0]) # get distances
        dy = abs(self.pos[1] - target.pos[1])
        dx = min(dx, self.width - dx) # adjust for toroidal space to
        dy = min(dy, self.height - dy)# avoid weird overflows 
        dt = math.sqrt(dx**2 + dy**2)
        heading = math.atan(dx / dy)
        if dt <= self.run_speed:
            self.pos = new_x, new_y
            self.attack_prey(target)
            if self.params['verbose']:
                print("change: it didn't do the thing I'm examining")
        else:
            change_x = self.run_speed * math.sin(heading)
            change_y = self.run_speed * math.cos(heading)
            if self.params['verbose']:
                print("change: %s, %s" % (change_x, change_y))
                print("change: from (%.2f, %.2f)..." % (self.pos[0], self.pos[1]))
            self.pos = (self.pos[0] + change_x, self.pos[1] + change_y)
            print("change: to (%.2f, %.2f)" % (self.pos[0], self.pos[1]))
            
        if self.params['verbose']:
            print('chase: predator %s moves to (%.2f, %.2f) in pursuit of prey %s'
                  % (self.unique_id, self.pos[0], self.pos[1], target.unique_id))
            
        # print(self.idle_speed)
        # print((rotation, distance))
    def attack_prey(self, target):
        if self.params['verbose']:
            print("attack: Predator %s (%.2f, %.2f) attacks at (%.2f, %.2f)"
                  % (self.unique_id, self.pos[0], self.pos[1],
                     target.pos[0], target.pos[1]))
    
    def step(self):
        self.move_idle()
        self.look()


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
        if params['verbose']: print("%i agents successfully added to model"
                                    % (int(self.num_predator + self.num_prey)))
        # print(prey_data)

    def count_agents(self):
        return len(self.schedule.agents)

    def step(self):
        self.schedule.step()

if __name__ == "__main__":
    main()

