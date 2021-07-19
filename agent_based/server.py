'''
Copyright 2021 Core Mesa Team and contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from mesa.visualization.ModularVisualization import ModularServer

from agent_based.herd_model import HerdModel # AHA! paths are relative to top-level run.py
from agent_based.SimpleContinuousModule import SimpleCanvas


def agent_portayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 2}
    if str(type(agent))[-15:-2] == "PreyAgent":
        portrayal["Color"] = "green"
    else:
        portrayal["Color"] = "red"
    return portrayal

herd_canvas = SimpleCanvas(agent_portayal, 500, 500)

def launch_server(model): #  server.launch_server(model, config, total_agents)
    model_params = {"num_prey": model.num_prey,
                    "num_predator": model.num_predator,
                    "width": model.space.width,   # what exactly does model_params get used for?
                    "height": model.space.height} # OMG might be it: self.model = self.model_cls(**model_params)
    
    server = ModularServer(HerdModel, # this does not work. why though?
                           [herd_canvas],
                           "Herding Model",
                           model_params)
    server.launch()

