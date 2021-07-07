#! /usr/bin/env python3

## IMPORTS ##

import math
import random
import re
import sqlite3 as sql
import sys
import numpy as np
import scipy.stats as stats
import pandas as pd

## ARGUMENT READING ##

for term in sys.argv:
    if term == "--quiet" or term == "-q": # verbose output is on by default
        verbose = False
    else:
        verbose = True
    if term == "--yes" or term == "-y": # accept all inputs
        accept_all = True
    else:
        accept_all = False


def main():
    fname = 'prey-distribution.conf'
    config = read_file(fname)
    if verbose: # interactive prompt to confirm config info, prompting user to change config if info is incorrect
        print('Preparing to place %i herds of average size %i on a %ix%i field.' % (config['herd-number'], config['average-herd-size'], config['width'], config['height']))
        if not accept_all:
            correct = input("Is this information correct? [Y/n]: ").lower()
            if correct == "n" or correct == "no": # abort if user answered n or no, continue otherwise
                print('You can update the configuration and correct this information in prey-distribution.cfg.')
                return # return rather than sys.exit(0), because that would quit a python live environment
            print() # adds a line break retroactively after "Is this information correct?"
    connection = sql.connect('../database.db') # this might be a bootleg way to do this. IDK anymore
    cursor = connection.cursor()
    try: # drop the table if it already exists
        cursor.execute("DROP TABLE prey_data")
    except sql.OperationalError: # triggers if the table does not already exist
        pass
    cursor.execute("CREATE TABLE prey_data (x INTEGER, y INTEGER, herd_x INTEGER, herd_y integer)") # if one doesn't already exist create it
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
        member_positions = place_herd_individuals(herd_position, member_number, config)
        # print(herd_position)
        for position in member_positions:
            x = position[0]
            y = position[1]
            herd_x = herd_position[0]
            herd_y = herd_position[1]
            cursor.execute("INSERT INTO prey_data(x, y, herd_x, herd_y) VALUES (?, ?, ?, ?)", (x, y, herd_x, herd_y)) # FIXME: this is calling at the wrong time, herd_x is always the same LAST VALUE
        # print(cursor.execute("SELECT x, y, herd_x, herd_y FROM prey_data").fetchall())
        sql_query = cursor.execute("SELECT x, y FROM prey_data").fetchall()
        df = pd.DataFrame(sql_query)
        df.to_csv('out.csv', index = False, header = False)

def read_file(fname):
    config = {}
    f = open(fname, 'r')
    for line in f.readlines():
        terms = re.split(':|\s', line) # split along empty space and colons
        terms_cleaned = [x for x in terms if x] # remove empty strings by keeping only terms with a value
        try: # convert value into integer only if applicable and add to dictionary with string identifier
            value = float(terms_cleaned[1])
            config[terms_cleaned[0]] = value # use dictionary syntax to add terms_cleaned key and value
        except ValueError:
            config[terms_cleaned[0]] = terms_cleaned[1]
        # TODO: add cross-checking of values, like I discussed with Ed 7/6. For instance, did they input both width and height?
    f.close()
    return config


def place_herd_individuals(herd_position, member_number, config):
    member_positions = []
    for member in range(member_number):
        rotation = (random.random() * 2 * math.pi) # rotation stored in radians
        distance = abs(random.gauss(0, config['herd-spacing-stdev'])) # absolute value of gaussian distribution means we have everything over the mean, so 66% of members are within 1 stdev of the center.
        herd_x = herd_position[0]
        herd_y = herd_position[1]
        member_x = int((math.sin(rotation) * distance) + herd_x) # REVIEW: should I be using floats or ints? this does ints right now but I could change it easily enough
        member_y = int((math.cos(rotation) * distance) + herd_y)
        # REVIEW: does a toroidal space help with the model, or am I better off just cutting off the values?
        if 0 > member_x or member_x > config['width']:
            member_x = member_x % config['width'] # wrap around values if they exceed the limits of the model as defined by the user
        if 0 > member_y or member_y > config['height']:
            member_y = member_y % config['height']
        # print('rotation: %s distance: %s x: %s y: %s' % (rotation, distance, member_x, member_y))
        if verbose: print('# Individual placed at (%i, %i) belonging to herd at (%i, %i)' % (member_x, member_y, herd_x, herd_y))
        # print('%i\t%i' % (member_x, member_y)) # bootleg way of getting this to work out of the box with gnuplot
        member_positions.append((member_x, member_y))
    # print(member_positions)
    return (member_positions) # to be fed back into a dictionary or sql database


main()
