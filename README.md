# agent-based-herding
Ray Heil's project for the 2021 Institute for Computing in Research. Licensed under the GNU General Public License 3.0.

## Installation and running
To start off, simply clone the github repository with 

```
git clone https://github.com/raymondheil/agent-based-herding.git
```

Then, edit the file `prey_distribution.conf` to change settings for prey placement.
The file should have its information stored in `setting: value` pairs, and empty lines or
comments starting with # will be ignored.

If the file is in a different format than described above, the program will not correctly 
handle the errors and you'll get a bunch of ugly issues later on. If they come from 
`run.py`'s `read_config` function, you likely encountered one.

### Configuration settings

* `width` and `height`: Dimensions of the field the agents are in

* `herd-number`: Number of herds to generate
* `herd-size`: Average number of prey in a herd
* `herd-spacing-stdev`: Standard deviation of placement from the center of a herd
* `herd-lone-prey-chance`: Percentage chance of a herd consisting of one lone prey member
* `herd-placement-attempts`: Number of points which are checked when placing an individual to find the most valuable ones

* `predator-number`: Number of predators in the simualtion
* `predator-run-speed`: Speed that predators run when they are pursuing a prey
* `predator-idle-speed`: Speed that predators move without seeing any prey
* `predator-stamina`: The maximum distance that a predator can run at its top speed
* `predator-kill-radius`: The distance a predator must be from its prey before it can attempt to kill it
* `predator-vision`: The radius a predator can see in

* `prey-run-speed`: The speed prey run at when they notice a predator
* `prey-stamina`: How far prey can run at their top speed before stopping
* `prey-escape-distance`: The distance at which a prey has successfully escaped an encounter with a predator
* `prey-vision`: The radius a prey can see predators in

These will be used for the agent-based modeling part of the project.

Once the config file is finished, run the code with `python3 run.py`. It will run the prey distribution
code and use this to place prey and predators in the agent-based model.

By default, the program will print the placement of each prey individual. This behavior can be
disabled with the `-q` or `--quiet` parameter on the command line.


## Planned additions

* Agent-based movement modeling
  * Predators follow random walks
  * Prey run from predators as a herd
* Batch data collection of populations
* Checking and cross-checking of config values to ensure they make sense and do not contradict each other
* Configuration settings for other aspects of the simulation
  * Movement forces
