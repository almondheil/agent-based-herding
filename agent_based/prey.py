from mesa import Agent
import math

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
        self.alive = True

    def look(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision)
        # print(len(visible))
        predators_visible = []
        prey_visible = []
        for neighbor in neighbors:
            if str(type(neighbor))[-15:-2] == "PredatorAgent": 
                predators_visible.append(neighbor)
            if str(type(neighbor))[-11:-2] == "PreyAgent":
                if neighbor.alive:
                    prey_visible.append(neighbor)
        return(predators_visible, prey_visible)

    def flee_predator(self, predator, originator):
        dx, dy = self.model.space.get_heading(originator.pos, predator.pos)
        
        angle = math.atan(dx / dy) # but if it's a nan, should I just randomize it? or maybe something else
        print("positions (%.2f, %.2f) and (%.2f, %.2f)"
              % (originator.pos[0], originator.pos[1], predator.pos[0], predator.pos[1]))
        print("angle.dx: %.2f" % dx)
        print("angle.dy: %.2f" % dy)
        print("angle: %.2f" % angle)
        new_x = self.pos[0] + (math.cos(angle) * self.run_speed)
        new_y = self.pos[1] + (math.sin(angle) * self.run_speed)
        self.model.space.move_agent(self, (new_x, new_y))
        if self.params['verbose']:
            print("chase: Prey %s (%.2f, %.2f) is fleeing predator (%.2f, %.2f)"
                  % (self.unique_id, self.pos[0], self.pos[1],
                     predator.pos[0], predator.pos[1]))
            
    def step(self):
        if self.alive:
            predators_visible, prey_visible = self.look()
            if len(predators_visible) > 0:
                predator = predators_visible[0]
                # TODO: have a more sophisticated way to choose who to run from
                for other_prey in prey_visible:
                    other_prey.flee_predator(predator, self)
                self.flee_predator(predator, self)
        # else:
            # print("agent %s removing self" % self.unique_id, flush=True) # 
            # self.model.space.remove_agent(self)
            # print(type(self), flush=True)
            
        
