#! /usr/bin/env python3

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

from datetime import datetime
import math
import pandas as pd
import random
import re
import sys
import scipy.stats as stats


for term in sys.argv:
    """Read in arguments given in the command line in order to customize program.
    Expandable to other options, including the possibility of specific file input
    for configuration or other uses."""

    if term == "--quiet" or term == "-q": # verbose output is on by default
        verbose = False
    else:
        verbose = True
    if term == "--yes" or term == "-y": # accept all inputs
        accept_all = True
    else:
        accept_all = False


def main():
    """Set up other aspects of the program and export."""
    fname = 'prey_distribution.conf'
    config = read_config(fname)
    # interactive prompt to confirm config info, prompting user to change config if info is incorrect
    if verbose:
        print('Preparing to place %i herds of average size %i on a %ix%i field.'
              % (config['herd-number'], config['average-herd-size'], config['width'], config['height']))
        if not accept_all: # just skip this section if the user specified -y
            answered = False
            while answered == False:
                correct = input("Is this information correct? [Y/n]: ").lower()
                if correct == "n" or correct == "no": # abort if user answered n or no, continue otherwise
                    print('You can update the configuration and correct this information in prey-distribution.conf.')
                    return # return rather than sys.exit(0), because that would quit a python live environment
                elif correct == "y" or correct == "yes" or correct == '':
                    answered = True
                    print() # adds a line break retroactively after "Is this information correct?"
                    continue
                else:
                    continue

    prey_data = pd.DataFrame(columns = ['x', 'y', 'herd_x', 'herd_y'])
    herd_positions = {} # [(pos_x, pos_y): num_members]
    herd_variation = math.sqrt(config['average-herd-size'])
    for i in range(int(config['herd-number'])): # generate completely random herd positions
        if random.random() <= config['lone-prey-chance']:
            member_number = 1
        else:
            member_number = int(random.gauss(config['average-herd-size'], herd_variation))
        herd_x = random.randint(0, config['width'])
        herd_y = random.randint(0, config['height'])
        herd_positions[(herd_x, herd_y)] = member_number
        if verbose: print('Herd %i to be placed at (%i, %i) with %i members' % (i+1, herd_x, herd_y, member_number))
    if verbose: print('\nIn total, %i prey individuals will be placed in %i herds\n' % (sum(herd_positions.values()), config['herd-number']))
    for herd_position in herd_positions.keys():
        member_number = herd_positions[herd_position]
        # print('member_number %i    herd_position %s' % (member_number, herd_position))
        member_positions = place_herd(herd_position, member_number, config)
        # print(herd_position)
        herd_x = herd_position[0]
        herd_y = herd_position[1]
        for position in member_positions:
            x = position[0]
            y = position[1]
            prey_data.loc[len(prey_data.index)] = [x, y, herd_x, herd_y]
        # print(prey_data)
    write_output(prey_data)


def write_output(prey_data, path_to_csv=None, csv_name=None):
    if csv_name: # output to either a specified CSV or to a file with the current time
        csv_out = str(csv_name) + ".csv"
    else:
        csv_out = datetime.now().strftime("Output %d-%m-%Y %H:%M:%S.csv")
    if verbose: print("\n# Saving to '%s'" % csv_out)
    prey_data.to_csv(csv_out, index=False)


def read_config(fname):
    """Read a config file into the program, separating terms and their values
    and adding them to a dictionary that can be referenced later.

    In the future, read_file will also perform checks and cross-checks that values
    are logical and point the user in the direction of any errors."""

    config = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            terms = re.split(':|\s', line) # split along empty space and colons
            terms_cleaned = [x for x in terms if x] # remove empty strings by keeping only terms with a value
            try: # convert value into integer only if applicable and add to dictionary with string identifier
                value = float(terms_cleaned[1])
                config[terms_cleaned[0]] = value # use dictionary syntax to add terms_cleaned key and value
            except ValueError:
                config[terms_cleaned[0]] = terms_cleaned[1]
            # TODO: add cross-checking of values, like I discussed with Ed 7/6. For instance, did they input both width and height?
    return config


def place_herd(herd_position, member_number, config):
    """Place a full herd of individuals, based around a centerpoint."""
    herd_x = herd_position[0]
    herd_y = herd_position[1]
    member_positions = []
    for member in range(member_number):
        # REVIEW: will using the distribution and wieghting together bias the placement at all? how?
        if member_positions:
            distance_value = {}
            value_distribution = stats.norm(25, 10) # TODO: make these parameters available in config (25, 3) was old
            for i in range(int(config['individual-placement-attempts'])):
                (test_x, test_y) = new_random_position(herd_position, config['herd-spacing-stdev'])
                point_value = 0
                for other_position in member_positions:
                    other_x, other_y = other_position
                    distance_to_other = math.sqrt((test_x - other_x)**2 + (test_y - other_y)**2)
                    point_value += value_distribution.pdf(distance_to_other) # the weight of this term in the final selection
                    # print('point_value %.4f for other_position %s test_position (%s, %s) and i %s' % (point_value, other_position, test_x, test_y, i))
            distance_value[(test_x, test_y)] = point_value
            distance_value = {key:val for key, val in distance_value.items() if val != 0} # remove any values that are just zero, which trips up random.choices()
            for value in distance_value.items():
                if value == 0:
                    print(value)
            member_x, member_y = random.choices(list(distance_value.keys()), list(distance_value.values()), k=1)[0] # janky but it comes out as a tuple in a list
            # print('x:%s\ty:%s' % (member_x, member_y))
        else: # if there aren't already entries, just place yourself at a random point point
            member_x, member_y = new_random_position(herd_position, config['herd-spacing-stdev'])
        # wrap around values outside the limits of the model, creating a toroidal space
        if 0 > member_x or member_x > config['width']:
            member_x = int(member_x % config['width'])
        if 0 > member_y or member_y > config['height']:
            member_y = int(member_y % config['height'])
        # print('rotation: %s distance: %s x: %s y: %s' % (rotation, distance, member_x, member_y))
        if verbose: print('# Individual placed at (%i, %i) belonging to herd at (%i, %i)' % (member_x, member_y, herd_x, herd_y))
        # print('%i\t%i' % (member_x, member_y)) # bootleg way of getting this to work out of the box with gnuplot
        member_positions.append((member_x, member_y))
    # print(member_positions)
    return(member_positions)


def new_random_position(herd_position, herd_spacing_stdev):
    rotation = (random.random() * 2 * math.pi) # radians, not degrees
    distance = abs(random.gauss(0, herd_spacing_stdev))
    herd_x = herd_position[0]
    herd_y = herd_position[1]
    member_x = int((math.sin(rotation) * distance) + herd_x)
    member_y = int((math.cos(rotation) * distance) + herd_y)
    return((member_x, member_y))


if __name__ == "__main__":
    main()
