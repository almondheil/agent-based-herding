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

from agent_based.herd_model import HerdModel
from agent_based.SimpleContinuousModule import SimpleCanvas
# from run import read_config
# A-HA! paths are relative to top-level run.py, which is
# why . was necessary without agent_based as part of it

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

"""
model_params = read_config('herding_setup.conf')
# model_params should be three dicts: params, config, prey_data.
# how do we get these in there? I think it makes the most sense from
# run.py, but I had some issues with that (commented out)

server = ModularServer(HerdModel,
                       [herd_canvas],
                       "Herding Model",
                       model_params)
"""

def launch_server(params, config, prey_data): #  server.launch_server(model, config, total_agents)
    #model = HerdModel(params, config, prey_data)
    model_params = {"params": params,
                    "config": config,
                    "prey_data": prey_data}
    # what exactly does model_params get used for?
    
    server = ModularServer(HerdModel,
                           [herd_canvas],
                           "Herding Model",
                           model_params)
    server.launch()

# then how do we get model_params in without a function call?
# and why wouldn't server = ModularServer() work in a function?
    
