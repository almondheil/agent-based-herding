from mesa import Agent
import math

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
        self.desired_heading = None
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
                print("prey_pos: (%.2f, %.2f) for predator %s"
                      % (prey.pos[0], prey.pos[1], self.unique_id))
                heading = self.model.space.get_heading(self.pos, prey.pos)
                if not self.params['verbose']:
                    print(heading)
                # FIXME: if 2+ prey are in the same position,
                # the first ones we check get overwritten.
            if self.params['verbose']:
                print("distances_to_prey %s" % distances_to_prey)
                print("predvis %s: %s currently visible"
                      % (self.unique_id, len(prey_visible)))
    
    def move_idle(self):
        """Do a random walk or initiate a chase after
        any prey you notice"""
        # print("Predator %s moves" % (self.unique_id))
        if self.desired_heading:
            if self.pos == self.desired_heading:
                # Find a new spot to go and start moving
                self.find_desired_heading()
                self.move_idle()
            else:
                # Move a small amount towards your goal spot
                pass
        else:
            # First time moving, find a spot and move towards it
            self.find_desired_heading()
            self.move_idle()
            
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
         
    def attack_prey(self, target):
        if self.params['verbose']:
            print("attack: Predator %s (%.2f, %.2f) attacks prey at (%.2f, %.2f)"
                  % (self.unique_id, self.pos[0], self.pos[1],
                     target.pos[0], target.pos[1]))

    def find_desired_heading(self):
        rotation = self.random.random() * 2 * math.pi
        steps_away = self.random.randint(0, 15)
        self.desired_heading = {"rotation": rotation,
                                # can we decrment steps each turn?
                                "steps": steps_away}
        
    def step(self):
        self.move_idle()
        self.look()
