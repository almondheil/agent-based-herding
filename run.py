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

from prey_distribution.prey_distribution_montecarlo import *
from agent_based.herd_model import *
import agent_based.server as server
# from agent_based.server import server

import sys
import re
import pandas as pd

params = {}
for term in sys.argv:
    """Read in arguments given in the command line in order to customize 
`program. Expandable to other options, including the possibility of specific 
file input for configuration or other uses."""
    if term == "--quiet" or term == "-q": # verbose output is on by default
        params['verbose'] = False
    else:
        params['verbose'] = True
    if term == "--interactive" or term == "-i":
        # TODO: add stopping points at other parts of the  process if -i is True
        # also in this case I need to 
        params['interactive'] = True
    else:
        params['interactive'] = False
        
def main():
    # interactive prompt to confirm config info, prompting user to
    # change config if info is lincorrect
    config = read_config('herding_setup.conf')
    if params['verbose']:
        print('Placing %i herds of average size %i on a %ix%i field.'
              % (config['herd-number'], config['herd-size'],
                 config['width'], config['height']))
        if params['interactive']: # just skip this section if the
                                  # user specified -y
            while True: # catch unknown input and ask again
                correct = input("Is this information correct? [Y/n]: ").lower()
                if correct == "n" or correct == "no": # abort if user answered n or no, continue otherwise
                    print('You can update the configuration and correct this information in herding_setup.conf.')
                    return # return rather than sys.exit(0), because
                           # that would quit a python live environment
                elif correct == "y" or correct == "yes" or correct == '':
                    print() # adds a line break retroactively after
                            # "Is this information correct?"
                    break
                else:
                    continue

    prey_data = pd.DataFrame(columns = ['x', 'y', 'herd_x', 'herd_y'])
    herd_positions = place_herds(config, params)
    # print(herd_positions)
    for herd in herd_positions.items():
        herd_position = herd[0]
        member_number = herd[1]
        member_positions = place_herd_members(config, params, herd_position, member_number)
        herd_x = herd_position[0]
        herd_y = herd_position[1]
        for position in member_positions:
            member_x = position[0]
            member_y = position[1]
            prey_data.loc[len(prey_data.index)] = [member_x, member_y, herd_x, herd_y]
    if params['verbose']:
        print("All placement values have been generated. Adding agents to model")
    server.launch_server(params, config, prey_data)
    # TODO: check if predators are chasing the correct number of prey

    
def read_config(fname):
    """Read a config file into the program, separating terms and their
    values and adding them to a dictionary that can be referenced
    later.

    In the future, read_file will also perform checks and cross-checks
    that values are logical and point the user in the direction of any
    errors."""
    config = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            # ignore lines that are fully comments or are
            # blank. cannot detect lines with ' \n' yet
            if line[:1] == '#' or line[:1] == "\n":
            # TODO: this only works with Unix \n newlines, as do other
            # parts of the code. that prolly means Windows \r\n won't
            # work
                continue
            terms = re.split(':|\s', line) # split along empty space
                                           # and colons
            # remove empty strings by keeping only terms with a value
            terms_cleaned = [] # [x for x in terms if x]
            for term in terms:
                if term:
                    terms_cleaned.append(term)
                
            # print(terms_cleaned)
            try: # convert value into integer only if applicable and
                 # add to dictionary with string identifier
                value = float(terms_cleaned[1])
                # use dictionary syntax to add terms_cleaned key & value
                config[terms_cleaned[0]] = value 
            except ValueError:
                config[terms_cleaned[0]] = terms_cleaned[1]
            # TODO: add cross-checking of values, like I discussed
            # with Ed 7/6. For instance, did they input both
            # width and height?

            # print(config)
    return(config)


def write_output(prey_data, path_to_csv=None, csv_name=None):
    if csv_name: # output to either a specified CSV or to a file with
                 # the current time
        csv_out = str(csv_name) + ".csv"
    else:
        csv_out = datetime.now().strftime("Output %d-%m-%Y %H:%M:%S.csv")
    if verbose: print("\nSaving to '%s'" % csv_out)
    prey_data.to_csv(csv_out, index=False)



if __name__ == "__main__":
    main()
