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


def main():
    """Doesn't do anything, this just holds some useful functions for
herd placement"""
    print("%s does not support running standalone. \nInstead, it should be used as a part of run.py." % (sys.argv[0]))

def place_herds(config, params):
    """Place a given number of herds randomly around the canvas."""
    prey_data = pd.DataFrame(columns = ['x', 'y', 'herd_x', 'herd_y'])
    herd_positions = {} # [(pos_x, pos_y): num_members]
    herd_variation = math.sqrt(config['herd-size'])
    for i in range(int(config['herd-number'])): # generate completely random herd positions
        if random.random() <= config['herd-lone-prey-chance']:
            member_number = 1
        else:
            member_number = int(random.gauss(config['herd-size'], herd_variation))
        herd_x = random.randint(0, config['width'])
        herd_y = random.randint(0, config['height'])
        herd_positions[(herd_x, herd_y)] = member_number
        if params['verbose']: print('Herd %i to be placed at (%i, %i) with %i member(s)' % (i+1, herd_x, herd_y, member_number))
    if params['verbose']: print('\nIn total, %i prey individuals will be placed in %i herds...\n' %
                                (sum(herd_positions.values()), config['herd-number']))
    return(herd_positions)


def place_herd_members(config, params, herd_position, member_number):
    """Place a full herd of individuals, based around a centerpoint."""
    herd_x = herd_position[0]
    herd_y = herd_position[1]
    member_positions = []
    for member in range(member_number):
        # REVIEW: will using the distribution and wieghting together bias the placement at all? how?
        if member_positions:
            distance_value = {}
            value_distribution = stats.norm(config['herd-preferred-spacing'], math.sqrt(config['herd-preferred-spacing']))
            for i in range(int(config['herd-placement-attempts'])):
                (test_x, test_y) = new_random_position(herd_position, config['herd-spacing-stdev'])
                point_value = 0
                for other_position in member_positions:
                    other_x, other_y = other_position
                    distance_to_other = math.sqrt((test_x - other_x)**2 + (test_y - other_y)**2)
                    point_value += value_distribution.pdf(distance_to_other) # the weight of this term in the final selection
                    # print('point_value %.4f for other_position %s test_position (%s, %s) and i %s'
                          # % (point_value, other_position, test_x, test_y, i))
            distance_value[(test_x, test_y)] = point_value
            distance_value_stripped = {key:val for key, val in distance_value.items() if val != 0} # remove any values that are just zero, which trips up random.choices()
            if distance_value_stripped: # only use choices() if there ARE any items in the stripped version, as an eptry array from the 0 removal would confuse it
                member_x, member_y = random.choices(list(distance_value_stripped.keys()), list(distance_value_stripped.values()), k=1)[0]
                # print("choices %s" % random.choices(list(distance_value_stripped.keys()), list(distance_value_stripped.values()), k=1))
            else:
                member_x, member_y = random.choice(list(distance_value.keys()))
            # print(list(distance_value.keys()))
            # print(list(distance_value.values()))
            # only do this if there IS anything in distance_value. if not, just randomly choose.
            # 1. don't delete the items if every item in the list is 0
            # 2. instead, if EVERY ITEM is 0 go ahead and just choose entirely randomly among the points
            # print('x:%s\ty:%s' % (member_x, member_y))
        else: # if there aren't already entries, just place yourself at a random point point
            member_x, member_y = new_random_position(herd_position, config['herd-spacing-stdev'])
        # wrap around values outside the limits of the model, creating a toroidal space
        if 0 > member_x or member_x > config['width']:
            member_x = int(member_x % config['width'])
        if 0 > member_y or member_y > config['height']:
            member_y = int(member_y % config['height'])
        # print('rotation: %s distance: %s x: %s y: %s' % (rotation, distance, member_x, member_y))
        # if params['verbose']: print('# Individual placed at (%i, %i) belonging to herd at (%i, %i)' % (member_x, member_y, herd_x, herd_y))
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
