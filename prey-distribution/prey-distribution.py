#! /usr/bin/env python3

import math
import random
import re
import sqlite3

verbose = False

def main():
    fname = 'prey-distribution.cfg'
    config = read_file(fname)
    if verbose: print("# Placing %i prey individuals on a %ix%i field\n" % (config['prey-number'], config['field-width'], config['field-height']))
    connection = sqlite3.connect("../database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE * FROM prey_data") # attempt to clear previous entries from table
    except sqlite3.OperationalError: # is this correct form?
        cursor.execute("CREATE TABLE prey_data (x FLOAT, y FLOAT, comfort_min FLOAT, comfort_max FLOAT)") # if one doesn't already exist create it
    # print('x_pos;y_pos') # might screw everything up if IDK how to work around it
    for i in range(config['prey-number'] + 1): # do I need this? I may have the wrong number of prey coming out rn
        place_individual(config, cursor)
def read_file(fname):
    config = {}
    f = open(fname, 'r')
    for line in f.readlines():
        terms = re.split(':|\s', line) # split along empty space and colons
        terms_cleaned = [x for x in terms if x] # remove empty strings by keeping only terms with a value
        # convert value into float only if applicable and add to dictionary with string identifier
        try:
            int(terms_cleaned[1])
            config[terms_cleaned[0]] = int(terms_cleaned[1]) # use dictionary syntax to add terms_cleaned key and value
        except ValueError:
            config[terms_cleaned[0]] = terms_cleaned[1]
    f.close()
    return config

def place_individual(config, cursor):
    ## generate random test values to evaluate
    (test_x, test_y) = (random.random() * config['field-width'], random.random() * config['field-height'])
    test_comfort_max = config['comfort-average'] + random.random() * config['comfort-max-variation']
    test_comfort_min = config['comfort-average'] - random.random() * config['comfort-max-variation']
    if verbose: print('# Testing at (%.2f, %.2f) with comfort_min %.2f and comfort_max %.2f' % (test_x, test_y, test_comfort_min, test_comfort_max))
    prey_data = cursor.execute("SELECT x, y, comfort_min, comfort_max FROM prey_data").fetchall()
    successful_points = {}
    if len(prey_data) == 0: # you're the first to be placed, don't check against anything
        cursor.execute("INSERT INTO prey_data(x, y, comfort_min, comfort_max) VALUES (?, ?, ?, ?)", (test_x, test_y, test_comfort_min, test_comfort_max))
    else: # you're not the first to be placed, time to find out what the best spot is
        for i in range(config['placement-attempts']): # number of times to test each coordinate
            for position in range(len(prey_data)): # number of existing coordinates we have to test against
                # collect x, y, comfort_min, and comfort_max for the other individual
                other_x = prey_data[position][0]
                other_y = prey_data[position][1]
                other_comfort_min = prey_data[position][2]
                other_comfort_max = prey_data[position][3]
                distance = math.sqrt((test_x - other_x)**2 + (test_y - other_y)**2) # calculate distance between points
                if test_comfort_min < distance < test_comfort_max or other_comfort_min < distance < other_comfort_max:
                    try:
                        successful_points[(test_x, test_y)] += 1 # add to dictionary entry if possible
                    except KeyError:
                        successful_points[(test_x, test_y)] = 1 # create dictionary entry if there isn't one already
            # generate new coordinates, but not a new comfort distance. we don't want to "optimize" comfort distance
            (test_x, test_y) = (random.random() * config['field-width'], random.random() * config['field-height'])
        max_value = max(list(successful_points.values()), default=0)
        most_valuable_points = []
        for term in list(successful_points.items()):
            if term[1] == max_value: # only allow into the running if it's one of the highest answers
                most_valuable_points.append(term)
        try:
            final_point = random.choice(most_valuable_points)[0] # choose the point tuple and leave the value behind
        except IndexError:
            final_point = (test_x, test_y) # only if there are no items in most_valuable_points, just use the most recent test point
        final_x, final_y = final_point
        if verbose: print('# Placing at (%.2f, %.2f) with comfort_min %.2f and comfort_max %.2f\n# Value of point %i' % (final_x, final_y, test_comfort_min, test_comfort_max, max_value))
        print('%f;%f' % (final_x, final_y))
        cursor.execute("INSERT INTO prey_data(x, y, comfort_min, comfort_max) VALUES (?, ?, ?, ?)", (final_x, final_y, test_comfort_min, test_comfort_max))


main()
