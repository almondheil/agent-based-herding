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

from .agent_based import HerdModel
from .SimpleContinuousModule import SimpleCanvas
# I need to import run.read_config but it sucks the most ever to exist
from run import read_config
'''
Current problem diagram for later--I can't deal with this right now

Code
  agent_based
    agent_based.py
    server.py ** import into here
    simple_continuous_canvas.js
    SimpleContinuousModule.py
  prey_distribution
    prey_distribution_montecarlo.py
    some output files
  run.py ** import from here. 
            this IS the top-level file, but it 
            tells me I'm importing from above it.
  README.md
  LICENSE
  herding_setup.conf 
'''

def draw_agent(agent, color):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": color}

herd_canvas = SimpleCanvas(draw_agent, 500, 500)

model_params = read_config('herding_setup.conf')

server = ModularServer(HerdModel, [herd_canvas], "Herds", model_params)
