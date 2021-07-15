from mesa.visualization.ModularVisualization import ModularServer

from .agent_based import HerdModel
from .SimpleContinuous import SimpleCanvas

def draw_agent(agent, color):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": color}


herd_canvas = SimpleCanvas(draw_agent, 500, 500)

model_params = read_config(herd

server = ModularServer(HerdModel, [herd_canvas], "Herds", model_params)
