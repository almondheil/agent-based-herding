# agent-based-herding 
Ray Heil's project for the 2021 Institute for Computing 
in Research. Licensed under the GNU General Public License
3.0.

## Installation and running
Before you start, make sure you have all the required Python 
packages installed with pip:

```
pip install mesa pandas scipy
```

Then, simply clone the github repository with

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
This will open a Tornado web server where you can control the model 
with the "Start/Stop," "Step," and "Reset" buttons at the top of 
the page.

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

