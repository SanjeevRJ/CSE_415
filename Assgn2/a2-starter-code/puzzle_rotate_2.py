'''puzzle3.py
An instance of the Eight Puzzle.
'''

from EightPuzzle import *

# We simply redefine the initial state.

init_state_list = [[3, 1, 2], 
                   [6, 8, 7], 
                   [5, 4, 0]]

CREATE_INITIAL_STATE = lambda: State(init_state_list)


