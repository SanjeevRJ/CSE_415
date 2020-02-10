'''EightPuzzleWithManhattan.py
by Sanjeev Janarthanan
UWNetID: sanjrj
Student number: 0751196

Assignment 2, in CSE 415, Winter 2020.
 
This file contains a formula for heuristics based on Manhattan distances. 
'''
from EightPuzzle import *

def h(s):
    total_dist = 0
    for r, row in enumerate(s.b):
        for t, tile in enumerate(row):
            tile = int(tile)
            if tile == 0:
                continue
            
            #adjusts the row and column values to their appropriate value
            adj_row = tile / 3
            adj_col = tile % 3
            
            total_dist += abs(r - adj_row) + abs(t - adj_col)
            
    return total_dist