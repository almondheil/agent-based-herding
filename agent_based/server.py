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

def draw_agent(agent):
    # print("AGENT TYPE PLEASE NOTICE ME %s -> %s" % (str(type(agent)), str(type(agent))[-11:-2]))
    portrayal = {"Shape": "circle",
                 "r": 2,
                 "Filled": "true",
                 "Color": "red"}
    if str(type(agent))[-11:-2] == "PreyAgent":
        portrayal["Color"] = "blue"
    else:
        portrayal["Color"] = "red"
    return portrayal

herd_canvas = SimpleCanvas(draw_agent, 500, 500)

def launch_server(params, config, prey_data):
    model_params = {"params": params,
                    "config": config,
                    "prey_data": prey_data}
    
    server = ModularServer(HerdModel,
                           [herd_canvas],
                           "Herding Model",
                           model_params)
    server.launch()

