'''BackMan.py
This Backgammon player simply asks the user to decide how
to move.  It can be used either to test another agent in
a competition, or to test the game master itself.

'''

from backgState import *

def move(state, die1, die2):
  w = state.whose_move
  print("I'm playing "+get_color(w))
  print("Tell me which checkers to move, with point numbers, e.g., 19,7")
  print("Use 0 to move from the bar.")
  print("If you want your first (or only) checker to move according")
  print("to the 2nd die, add a 3rd argument R: e.g., 19,7,R to reverse the dice.")
  print("For only 1 checker to move with both dice, give as 2nd argument the point number")
  print("where the checker will be after the move is half done.")
  ans = input("or enter Q to quit: ")
  return ans
  #return "Q" # quit

