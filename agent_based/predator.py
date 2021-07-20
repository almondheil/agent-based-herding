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
        self.current_stamina = self.stamina
        self.wait_timer = 0
        self.kill_radius = self.random.gauss(
            self.config['predator-kill-radius'],
            math.sqrt(self.config['predator-kill-radius']))
        self.vision = self.random.gauss(
            self.config['predator-vision'],
            math.sqrt(self.config['predator-vision']))
        # desired_heading placeholder that will later be reset
        self.desired_heading = {"rotation": 0,
                                "steps": 0}

        
    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        prey_visible = []
        for neighbor in neighbors:
            if str(type(neighbor))[-11:-2] == "PreyAgent":
                prey_visible.append(neighbor)
                if self.params['verbose']:
                    print("see: predator %s (%.2f, %.2f) sees prey at %s"
                          % (self.unique_id, self.pos[0], self.pos[1],
                             neighbor.pos))
        return(prey_visible)
                
    def move_idle(self):
        """Do a random walk or initiate a chase after
        any prey you notice"""
        if self.desired_heading["steps"] <= 0:
            # it IS possible for it to be under 0, so this should
            # serve as a catch-all
            rotation = self.random.random() * 2 * math.pi
            steps_away = self.random.randint(1, 15)
            # TODO: make 0, 15 configurable with pred_min_steps
            # and pred_max_steps
            self.desired_heading = {"rotation": rotation,
                                    "steps": steps_away}
        current_x, current_y = self.pos
        new_x = current_x + (math.cos(self.desired_heading["rotation"]) * self.idle_speed)
        new_y = current_y + (math.sin(self.desired_heading["rotation"]) * self.idle_speed)
        # new_x, new_y = self.check_position(new_x, new_y)
        self.pos = (new_x, new_y)
        self.model.space.move_agent(self, (new_x, new_y))
        # this should take care of the issue with the torus
        self.desired_heading["steps"] -= 1
        # print("Predator %s moves" % (self.unique_id))

        
    def chase_prey(self, target):
        """After noticing a prey, chase it down. 
        Possible outcomes include: 
            Catch up, secure kill; 
            Catch up, miss kill; 
            Don't catch up :(
        
        Difference between prey initiated chase and predator initiated
        is that prey gets a full (or maybe percentage) movement before
        alerting predator"""
        dx, dy = self.model.space.get_heading(self.pos, target.pos)
        dt = math.sqrt(dx**2 + dy**2)
        rotation = math.atan(dx / dy)
        # REVEIW: is my trig correct?
        if dt <= self.run_speed:
            self.model.space.move_agent(self, target.pos)
            self.attack_prey(target)
            if self.params['verbose']:
                print("chase: predator %s caught up with prey %s and is attacking" % (self.unique_id, target.unique_id))
        else:
            new_x = self.pos[0] + (self.run_speed * math.sin(rotation))
            new_y = self.pos[1] + (self.run_speed * math.cos(rotation))
            self.model.space.move_agent(self, (new_x, new_y))

            
    def attack_prey(self, target):
        if self.params['verbose']:
            print("attack: Predator %s (%.2f, %.2f) attacks prey at (%.2f, %.2f)"
                  % (self.unique_id, self.pos[0], self.pos[1],
                     target.pos[0], target.pos[1]))

            
    def step(self):
        prey_visible = self.look()
        if self.current_stamina <= 0:
            self.wait_timer = 10
            # TODO: make this configurable
            self.current_stamina = self.stamina
            
        if self.wait_timer > 0:
            self.wait_timer -= 1
        else:
            if len(prey_visible) > 0:
                distances_to_prey = {}
                for prey in prey_visible:
                    dt = self.model.space.get_distance(self.pos, prey.pos)
                    distances_to_prey[prey] = dt
                print(list(distances_to_prey.items())[0])
                target = max(distances_to_prey.items(), key=lambda x : x[1])[0]
                
                # target = max(list(distances_to_prey.items()))
                # chase the closest target
                self.chase_prey(target)
                self.current_stamina -= self.run_speed
            else:
                self.move_idle()
        
