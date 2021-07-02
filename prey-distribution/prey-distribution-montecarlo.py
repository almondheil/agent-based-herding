#! /usr/bin/env python3

import math
import random
import re
import sqlite3 as sql
import sys

for term in sys.argv:
    if term == "--quiet" or term == "-q": # verbose output is on by default
        verbose = False
    else: verbose = True

def main():
    fname = 'prey-distribution.cfg'
    config = read_file(fname)
    if verbose:
        # interactive prompt to confirm config info, prompting user to change config if info is incorrect
        print('Preparing to place %i herds of average size %i on a %ix%i field.' % (config['herd-number'], config['average-herd-size'], config['width'], config['height']))
        correct = input("Is this information correct? [Y/n]: ").lower()
        if correct == "n" or correct == "no": # abort if user answered n or no, continue otherwise
            print('You can update the configuration and correct this information in prey-distribution.cfg.')
            return # rather than sys.exit(0), because that would quit a python live environment
        else:
            print('\n')
    connection = sql.connect('../database.db') # this might be a bootleg way to do this. IDK anymore
    cursor = connection.cursor()
    try: # drop table and create a new one. I tried using DELETE to clear it but it didn't work
        cursor.execute("DROP TABLE prey_data")
    except sql.OperationalError:
        pass
    cursor.execute("CREATE TABLE prey_data (x INTEGER, y INTEGER, herd INTEGER)") # if one doesn't already exist create it
    herd_positions = {} # [(pos_x, pos_y): num_members]
    herd_variation = math.sqrt(config['average-herd-size'])
    for i in range(config['herd-number']): # generate completely random herd positions
        # TODO: switch random.gauss() out for my own function that accounts for lone deer and/or other stuff
        member_number = int(random.gauss(config['average-herd-size'], herd_variation))
        x = int(random.random() * config['width'])  # TODO: is herds overlapping going to be a big issue?
        y = int(random.random() * config['height']) # if so I need to proof against that, but it may lend itself to bias.
        herd_positions[(x, y)] = member_number
        if verbose:
            print('Herd %i to be placed at (%i, %i) with %i members' % (i+1, x, y, member_number))
    if verbose:
        print('\nIn total, %i prey individuals will be placed in %i herds' % (sum(herd_positions.values()), config['herd-number']))
    for herd_position in herd_positions.keys():
        member_number = herd_positions[herd_position]
        print('member_number %i    herd_position %s' % (member_number, herd_position))
        for i in range(member_number):
            individual_position = place_individual(herd_position)
        # TODO: almost entirely rewrite individual_position, then make it return the position of the individual
        # cursor.execute("INSERT INTO prey_data(x, y, comfort_min, comfort_max) VALUES (?, ?, ?, ?)", ())


    # print(herd_positions)
    # print(herd_positions.values())
    # print(sum(herd_positions.values()))


def read_file(fname):
    config = {}
    f = open(fname, 'r')
    for line in f.readlines():
        terms = re.split(':|\s', line) # split along empty space and colons
        terms_cleaned = [x for x in terms if x] # remove empty strings by keeping only terms with a value
        try: # convert value into float only if applicable and add to dictionary with string identifier
            int(terms_cleaned[1])
            config[terms_cleaned[0]] = int(terms_cleaned[1]) # use dictionary syntax to add terms_cleaned key and value
        except ValueError:
            config[terms_cleaned[0]] = terms_cleaned[1]
    f.close()
    return config


def place_individual(herd_position):
    """
    Place an individual prey, based on the center of its herd. Another thing I
    don't really have the energy for at the moment, and will have to wait
    until I'm inspired on the weekend or until Monday. No later though.
    """
    pass


def altered_gaussian():
    """
    This is a placeholder for later. I need to create an altered version of a Gaussian,
    but I don't have the energy to put towards it at the moment. Making approximations
    of complex functions like this is central to the kind of Monte Carlo modeling that I
    am doing, and I need to put a lot more work into understanding it-- on a base level as
    well as how to do it in code.

    In the future, this function will produce an integral of a gaussian, but the
    probability of a lone animal will be based on config['lone-prey-chance'].
    At the moment, I can't think how exactly that affects the integral.

    Ed's drawings from July 1 were torn out, but I'll keep them folded in the black notebook.
    """
    pass



main()
