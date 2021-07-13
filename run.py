#! usr/bin/env python3

'''
    $NAME: Agent-based Monte Carlo modeling of herding dynamics.
    Copyright (C) 2021 Raymond Heil

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from prey_distribution_montecarlo import *
from agent_based import *


def main():
    config = read_config('herd_scenario.conf')
    prey_positions = place_herd(herd_position, member_number)
    # generate prey positions and save them to a pd dataframe, as well as an optional CSV
    # run that dataframe into the agent_based model
    # go from there


def read_config(fname):
    """Read a config file into the program, separating terms and their values
    and adding them to a dictionary that can be referenced later.

    In the future, read_file will also perform checks and cross-checks that values
    are logical and point the user in the direction of any errors."""
    config = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            if line[:1] == '#' or line[:1] == "\n": # ignore lines that are fully comments or are blank. cannot detect lines with ' \n' yet
            # TODO: this only works with Unix \n newlines, as do other parts of the code. that prolly means Windows \r\n won't work
                continue
            terms = re.split(':|\s', line) # split along empty space and colons
            terms_cleaned = [x for x in terms if x] # remove empty strings by keeping only terms with a value
            # print(terms_cleaned)
            try: # convert value into integer only if applicable and add to dictionary with string identifier
                value = float(terms_cleaned[1])
                config[terms_cleaned[0]] = value # use dictionary syntax to add terms_cleaned key and value
            except ValueError:
                config[terms_cleaned[0]] = terms_cleaned[1]
            # TODO: add cross-checking of values, like I discussed with Ed 7/6. For instance, did they input both width and height?
    # print(config)
    return(config)


if __name__ == "__main__":
    main()
