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
from mesa.visualization.modules import ChartModule

from agent_based.herd_model import HerdModel
from agent_based.SimpleContinuousModule import SimpleCanvas

import matplotlib.pyplot as plt

def draw_agent(agent):
    # print("AGENT TYPE PLEASE NOTICE ME %s -> %s" % (str(type(agent)), str(type(agent))[-11:-2]))
    portrayal = {"Shape": "circle",
                 "r": 1.5,
                 "Filled": "true"}
    if str(type(agent))[-11:-2] == "PreyAgent":
        portrayal["Color"] = "MidnightBlue"
        
    else:
        portrayal["Color"] = "MediumVioletRed"
        portrayal["r"] = 3
    return portrayal

herd_canvas = SimpleCanvas(draw_agent, 500, 500)

chart = ChartModule([{"Label": "Alive",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

def launch_server(params, config, prey_data):
    model_params = {"params": params,
                    "config": config,
                    "prey_data": prey_data}
    
    server = ModularServer(HerdModel,
                           [herd_canvas],
                           "Herding Model",
                           model_params)
    if config['total-steps'] > 0:
        model = HerdModel(**model_params)
        print("Simulating %i steps of the model."
              % config['total-steps'])
        for i in range(int(config['total-steps'])):
            model.step()
            
        seed = int(config['seed'])
        if config['herd-lone-prey-chance'] == 1:
            mode = "solo"
        else:
            mode = "herd"
            
        alive = model.datacollector.get_model_vars_dataframe()
        alive.to_csv(path_or_buf= f"./Output/{mode}_{seed}.csv", 
                     sep=',',
                     index=False,
                     header=[f"{mode} prey"])
        # alive.plot()
        # plt.show()
    else:
        print("Starting interactive server of the model.")
        server.launch()

