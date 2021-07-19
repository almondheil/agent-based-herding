# agent-based-herding
Ray Heil's project for the 2021 Institute for Computing in
Research. Licensed under the GNU General Public License 3.0.

## Installation and running
To start off, simply clone the github repository with

```
git clone https://github.com/raymondheil/agent-based-herding.git
```

Then, cd into the cloned repository and attempt to run the main
file:
```
cd agent-based-herding
```
```
python3 run.py
```
Currently, this throws an error after a few seconds of running. See
below for more info.

## ModularVisualization error

With run.py, the program currently throws an error while trying to
place the agents in the agent-based model. Here's the traceback I got,
and what I'm under the impression of for its meaning.

```
Traceback (most recent call last):
  File "/home/ray/Nextcloud/agent-based-herding/run.py", line 141, in <module>
    main()
  File "/home/ray/Nextcloud/agent-based-herding/run.py", line 87, in main
    server.launch_server(model)
  File "/home/ray/Nextcloud/agent-based-herding/agent_based/server.py", line 43, in launch_server
    server = ModularServer(HerdModel, # this does not work. why though?
  File "/home/ray/.local/lib/python3.9/site-packages/mesa/visualization/ModularVisualization.py", line 286, in __init__
    self.reset_model()
  File "/home/ray/.local/lib/python3.9/site-packages/mesa/visualization/ModularVisualization.py", line 314, in reset_model
    self.model = self.model_cls(**model_params)
TypeError: __init__() got an unexpected keyword argument 'num_prey'
```

The argument num_prey is the first parameter I'm trying to pass into
this visualization of the model. In all the tutorials and examples
I've been able to follow there is only one population of agents,
rahter than the two populations of predators and prey that I have.  In
those examples, I also noticed that the parameters they passed into
ModularVisualization had the same names as when they defined the
model. This might mean that I need to pass in all the properties my
model has, so I'll try this as well and update my GitHub if it
magically works.

## Configuration settings

To edit the settings the program runs with, edit the file
`prey_distribution.conf` to change the model settings. The file
should have only one `setting: value` pair per line, and full-line
comments starting with `#` will be ignored.

If the file is in a different format than described above, the program
will not correctly handle the errors and you'll get a bunch of ugly
issues later on. If they come from `run.read_config`, you likely
encountered one. Descriptions of the config settings are visible
below, but may be moved elsewhere in a future update.

## So what do all those variables mean?
Environmental
* `width` and `height`: Dimensions of the field the agents are in

Herd Placement
* `herd-number`: Number of herds to generate
* `herd-size`: Average number of prey in a herd
* `herd-spacing-stdev`: Standard deviation of placement from the
center of a herd
* `herd-lone-prey-chance`: Percentage chance of a herd consisting
of one lone prey member
* `herd-placement-attempts`: Number of points which are checked
when placing an individual to find the most valuable ones
* `herd-preferred-spacing`: The optimal distance between members
the herd, used to calculate the value of any possible point

Predator Attributes
* `predator-number`: Number of predators in the simualtion
* `predator-run-speed`: Speed that predators run when they
are pursuing a prey
* `predator-idle-speed`: Speed that predators move before
noticing any prey
* `predator-stamina`: The maximum distance that a predator
can run at its top speed
* `predator-kill-radius`: The distance a predator must be
from its prey before it can attempt to kill it
* `predator-vision`: The radius a predator can see in

Prey Attributes
* `prey-run-speed`: The speed prey run at when they
notice a predator
* `prey-stamina`: How far prey can run at their top
speed before stopping
* `prey-escape-distance`: The distance at which
a prey has successfully escaped an encounter with a predator
* `prey-vision`: The radius a prey looks for predators, as
well as other fleeing prey

## Planned additions

* Agent-based movement modeling
  * Prey run from predators as a herd,
  following basic selfish herd principles
* Batch data collection of populations
* Checking and cross-checking of config values to ensure they make
sense and do not contradict each other Configuration settings for
other aspects of the simulation Movement forces

