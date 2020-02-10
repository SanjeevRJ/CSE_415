'''EightPuzzleWithHamming.py
by Sanjeev Janarthanan
UWNetID: sanjrj
Student number: 0751196

Assignment 2, in CSE 415, Winter 2020.
 
This file contains a formula for heuristics based on Hamming distances. 
'''

from EightPuzzle import *

def h(s):
    goal = [[0,1,2], [3,4,5], [6,7,8]]
    out = 0
    for r, row in enumerate(s.b):
        for t, tile in enumerate(row):
            
            if tile != 0 and goal[r][t] != tile:
                out += 1
                
            
        return out