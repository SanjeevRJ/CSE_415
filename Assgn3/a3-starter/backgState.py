'''backgState.py

A state class for the game of Backgammon.
S. Tanimoto, Jan. 17, 2020.

'''

W = 0; R = 1

def get_color(who):
  return ['White', 'Red'][who]

class bgstate:
  def __init__(self, old=None):
    if old:
      self.pointLists = [lst[:] for lst in old.pointLists]
      self.bar = old.bar[:]
      self.white_off = old.white_off[:]
      self.red_off = old.red_off[:]
      self.cube = old.cube
      self.offering_double = old.offering_double
      self.whose_move = old.whose_move
    else:
      self.bar=[]
      self.white_off = []
      self.red_off = []
      self.cube=1
      self.offering_double = False
      self.whose_move = W
      self.pointLists =[
[W,W],
[],
[],
[],
[],
[R,R,R,R,R],
[],
[R,R,R],
[],
[],
[],
[W,W,W,W,W],
[R,R,R,R,R],
[],
[],
[],
[W,W,W],
[],
[W,W,W,W,W],
[],
[],
[],
[],
[R,R] ]

  def __str__(self):
    s = '+----------\n'
    for i in range(len(self.pointLists)):
      point = self.pointLists[i]
      line=str(i+1)+':'
      for c in point:
        if c==W: line += 'W'
        elif c==R: line += 'R'
      line+='\n'
      s += line
    s += '+----------\n'
    line =  'bar:'
    for c in self.bar:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    line =  'white off:'
    for c in self.white_off:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    line =  'red off:'
    for c in self.red_off:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    s += 'cube: '+str(self.cube)+'\n'
    s += 'offering to double: '+str(self.offering_double)+'\n'
    s += '===========\n'
    return s

  def prettyPrint(self):
    top_numbers    = " 131415161718 192021222324\n"
    bottom_numbers = " 121110 9 8 7  6 5 4 3 2 1\n"
    hline = "+------------+------------+\n"
    s = top_numbers + hline
    point_lengths    = [len(l) for l in self.pointLists]
    top_max_checkers = 0
    for i in range(12,24):
      top_max_checkers = max(top_max_checkers, point_lengths[i])
    #print("top_max_checkers = ", top_max_checkers)
    for j in range(top_max_checkers):
      line = '|'
      for i in range(12,24):
        if j < point_lengths[i]:
          if self.pointLists[i][0]==W:
            line += ' W'
          else:
            line += ' R' 
        else:
          line += '  '
        if i==17: line += '|'
      s += line + '|\n'
    bottom_max_checkers = 0
    for i in range(11,-1,-1):
      bottom_max_checkers = max(bottom_max_checkers, point_lengths[i])
    sb = ''
    for j in range(bottom_max_checkers):
      line = '|'
      for i in range(11,-1,-1):
        if j < point_lengths[i]:
          if self.pointLists[i][0]==W:
            line += ' W'
          else:
            line += ' R' 
        else:
          line += '  '
        if i==6: line += '|'
      sb = line + '|\n' + sb
    #print("bottom_max_checkers = ", bottom_max_checkers)
    s += hline + sb + hline + bottom_numbers
    line =  'bar:'
    for c in self.bar:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    line =  'White off:'
    for c in self.white_off:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    line =  'Red off:'
    for c in self.red_off:
      if c==W: line += 'W'
      elif c==R: line += 'R'
    line+='\n'
    s += line
    if self.whose_move==W:
      line2 = "Now it's White's turn.\n"
    else:
      line2 = "Now it's Red's turn.\n"
    s += line2 + '==========================\n'
    return s

import random
def toss(deterministic=False):
  if deterministic: return((1,6))
  die1 = random.choice(range(1,7))
  die2 = random.choice(range(1,7))
  return (die1,die2)

if __name__=='__main__':
  INITIAL_STATE = bgstate()
  print(INITIAL_STATE.prettyPrint())

