# agent-based-herding
Ray Heil's project for the 2021 Institute for Computing in Research. Licensed under the GNU General Public License 3.0.

## Installation and running
To start off, simply clone the github repository with 

`git clone https://github.com/raymondheil/agent-based-herding.git`

Then, edit the file `prey_distribution.conf` to change settings for prey placement.
The file will only be correctly encoded with one `setting: value` pair per line.
If this format is broken, the file may read incorrectly. Currently, the program doesn't
know how to recognize this error or prompt the user to correct it.

### Configuration settings

* `width` and `height`: Dimensions of the field the agents are in
* `herd-number`: Number of herds to generate
* `average-herd-size`: Average number of prey in a herd
* `lone-prey-chance`: Percentage chance of a herd consisting of one lone prey member
* `herd-spacing-stdev`: Standard deviation of placement from the center of a herd
* `individual-placement-attempts`: Number of points which are checked when placing an 
individual to find the most valuable ones


Once the config file is correct, run the code with `python3 prey_distribution_montecarlo.py`
by default, the program will print the placement of each prey individual. This behavior can be
disabled with the `-q` or `--quiet` parameter on the command line.

When the program has finished running, it will output the positions of each prey member to a
`.csv` file. At this point this file is the only output, but the prey placement script will also be used
to generate prey positions for the agent-based part of the project.

## Planned additions

* Agent-based movement modeling
  * Predators follow random walks
  * Prey follow Hamiltonian selfish herd movement rules
* Batch data collection of populations
* Checking and cross-checking of config values to ensure they make sense and do not contradict each other
* Configuration settings for other aspects of the simulation
  * Predator placement
  * Movement forces
