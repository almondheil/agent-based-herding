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
