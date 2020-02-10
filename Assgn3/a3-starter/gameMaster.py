'''gameMasterV03.py

A simple game master program for Simplified Backgammon.

To use this program, edit the import statements below to import your
preferred playing agents, and set the time limit per move.

Then run the program under Python 3.x from a command line:
python3 gameMaster.py  

The rules of the game are simplified for this version of Backgammon.
A. WHITE always plays first, so there is no initial rolling and
   requirement that the first player use the initial roll.
B. No doubling allowed. "Cube value" is therefore always 1.
C. A player may pass on any turn, in either of two ways:
     -- Pass on the whole turn. 
     -- Pass on moving a second checker.
D. If no move is available to a player on its turn, then it MUST pass
   or forfeit the game.  If it can move only one checker, then it
   should do that and pass for the second checker.
E. If the dice come out doubles (like a pair of sixes), then unlike
   standard backgammon, where the player can move 4 checkers, we
   don't allow any special bonus.
F. Standard backgammon has a rule that if a player can only use one
   of the two dice, the player must use the larger number.  We do not
   follow that rule.  Either number may be used.
G. No special rules are in effect, like the Crawford rule, since
   we don't use the doubling cube.

This game master is very strict, in terms of requiring that the
playing agents describe legal moves.  If the game master detects
anything wrong with a player's move, the game ends and the player
with the questionable move forfeits the game.

Status as of Nov. 20, 2019 (version 02)

Basic move checking and execution is OK.
Bearing off works.
Bringing checkers onto the board from the bar works,
 including to hit an opponent's blot (single checker). ***(as of Nov. 20)***
Win detection is implemented.

Time limits are not implemented so just ignored in this version.

Nov. 27. Bug fixed in line 247. call to hit with target_point-1 was changed
to target_point, as it was pointed out by Xui Xiao on the discussion board
that the subtraction of 1 was performed already in the hit function.
Also added a check for having a checker on the bar, before trying to move
a piece from a point; that's illegal and now ends the game.

Jan 17, 2020. "Deterministic" feature added that forces dice to specific
outcomes.  This is useful in terms of allowing alpha-beta pruning to
make sense.
'''

import BackMan as agent1
#import McGammon as agent2
import BackMan as agent2
TIME_LIMIT=3.0 # 2 seconds.

DETERMINISTIC = True
# for the deterministic version, where the dice are loaded in a way
# that prevents all randomness.

#DETERMINISTIC = False
# for the stochastic version of the game ("SSBG"), so that dice get
# rolled normally.


from backgState import *

DONE = False
def run(agent1, agent2, max_secs_per_move, initial_state=bgstate(), deterministic=False):
  '''Start and monitor a game of Simplified Backgammon.
  The two players are agent1 and agent2, which must be instances of a class
  that implements method named "move".
  max_secs_per_move is the time limit.  If it's 0, then no time limit.
  initial_state is a function that should return a valid state
  from which the game should start.  The default is to start from the
  beginning -- the standard starting board for Backgammon.
  If deterministic is True, then instead of rolling dice randomly,
  fixed values (1, 6) come back.  This allows a variation of the game
  in which alpha-beta pruning makes sense.
  '''
  print("The Simplified Backgammon Game-master (V03) says: Welcome!")
  global DONE
  current_state = initial_state
  while(not DONE):
    print("Current state:")
    print(current_state.prettyPrint())
    whose_move = current_state.whose_move
    new_state = None

    print(get_color(whose_move)+' to play...')
    die1,die2 = toss(deterministic)
    if deterministic: print("The result of the 'heavily biased' dice roll gives "+
           str(die1)+', '+str(die2))
    else: print("The dice roll gives: "+str(die1)+', '+str(die2))
    if whose_move==W: mover=agent1
    else: mover=agent2
    move=mover.move(current_state, die1, die2)
    print(get_color(whose_move), "moves from: ", move)
    if move in ["Q", "q"]:
      print('Agent '+get_color(whose_move)+' resigns. Game OVER!')
      forfeit(whose_move)
      break;
    if move in ["P", "p"]:
      print('Agent '+get_color(whose_move)+' passes.')
      if moves_exist(current_state, whose_move, die1, die2):
        print("Moves exist. Passing is not allowed. You lose.")
        forfeit(whose_move)
        break;
      else:
        print("OK. Pass is accepted for this turn.")
        new_state = bgstate(current_state)
        new_state.whose_move=1-whose_move
        current_state = new_state
        continue
    else:
      try:
        move_list = move.split(',')
        if len(move_list)==3 and move_list[2] in ['R','r']:
          dice_list = [die2, die1]
        else:
          dice_list = [die1, die2]
        checker1, checker2 = move_list[:2]
      except:
        print("Invalid type of move: ", move, " Game over.")
        forfeit(whose_move)
        break
      for i in range(2):
        # Just in case the player wants to pass after the first checker is moved:
        if i==1 and checker2 in ['P','p']:
          print("OK. Pass is accepted for the other die.")
          new_state = bgstate(current_state)
          new_state.whose_move=1-whose_move
          current_state = new_state
          continue

        pt = int([checker1, checker2][i])
        # Check first for a move from the bar:
        if pt==0:
          # Player must have a checker on the bar.
          if not whose_move in current_state.bar:
            print("You don't have any checkers on the bar.")
            forfeit(whose_move)
            break
          new_state = handle_move_from_bar(current_state, whose_move, dice_list[i])
          if not new_state:
            print("Move from bar is illegal.")
            forfeit(whose_move)
            break
          current_state = new_state
          continue
        # Now make sure player does NOT have a checker on the bar.
        if any_on_bar(current_state, whose_move):
          print("Illegal to move a checker from a point, when you have one on the bar.")
          forfeit(whose_move)
          break
        # Is checker available on point pt?
        if pt < 1 or pt > 24:
          print(pt, "is not a valid point number.")
          forfeit(whose_move)
          break
        if not whose_move in current_state.pointLists[pt-1]:
          print("No "+get_color(whose_move)+" checker available at point "+str(pt))
          forfeit(whose_move)
          break
        # Determine whether destination is legal.
        die = dice_list[i]
        if whose_move==W:
          dest_pt = pt + die
        else:
          dest_pt = pt - die
        if dest_pt > 24 or dest_pt < 1:
          born_off_state = bear_off(current_state, pt, dest_pt, whose_move)
          if born_off_state:
            current_state = born_off_state
            continue
          print("Cannot bear off this way.")
          forfeit(whose_move)
          break
       
        dest_pt_list = current_state.pointLists[dest_pt-1]
        if len(dest_pt_list) > 1 and dest_pt_list[0]!=whose_move:
          print("Point "+str(dest_pt)+" is blocked. You can't move there.")
          forfeit(whose_move)
          break
        # So this checker's move is legal. Update the state.
        if not new_state:
          new_state = bgstate(current_state)
        # Remove checker from its starting point.
        new_state.pointLists[pt-1].pop()
        # If the destination point contains a single opponent, it's hit.
        new_state = hit(new_state, dest_pt_list, dest_pt)
        # Now move the checker into the destination point.
        new_state.pointLists[dest_pt-1].append(whose_move)
        current_state = new_state
    current_state.whose_move=1-whose_move
    if win_detected(current_state, whose_move):
      print(current_state.prettyPrint())
      print("\nBIG NEWS: "+get_color(whose_move)+" WON THE GAME.")
      break

def hit(new_state, dest_pt_list, dest_pt):
  opponent = 1-new_state.whose_move
  if len(dest_pt_list)==1 and dest_pt_list[0]==opponent:
    if opponent==W:
      new_state.bar.insert(W, 0) # Whites at front of bar
    else:
      new_state.bar.append(R) # Reds at end of bar
    new_state.pointLists[dest_pt-1]=[]
  return new_state

def bear_off(state, src_pt, dest_pt, who):
  # Return False if 'who' is not allowed to bear off this way.
  # Otherwise, create the new state showing the result of bearing
  # this one checker off, and return the new state.

  # First of all, is bearing off allowed, regardless of the dice roll?
  if not bearing_off_allowed(state, who): return False
  # Direct bear-off, if possible:
  pl = state.pointLists[src_pt-1]
  if pl==[] or pl[0]!=who:
    print("Cannot bear off from point "+src(src_pt))
    return False
  # So there is a checker to possibly bear off.
  # If it does not go exactly off, then there must be
  # no pieces of the same color behind it, and dest
  # can only be one further away.
  good = False
  if who==W:
    if dest_pt==25:
       good = True
    elif dest_pt==26:
       for point in range(18,src_pt-1):
         if W in state.pointLists[point]: return False
       good = True
  elif who==R:
    if dest_pt==0:
       good = True
    elif dest_pt== -1:
       for point in range(src_pt, 6):
         if R in state.pointLists[point]: return False
       good = True
  if not good: return False 
  born_off_state = bgstate(state)
  born_off_state.pointLists[src_pt-1].pop()
  if who==W: born_off_state.white_off.append(W)
  else:  born_off_state.red_off.append(R)
  return born_off_state

def forfeit(who):
  global DONE
  print("Player "+get_color(who)+" forfeits the game and loses.")
  DONE = True

def moves_exist(state, who, die1, die2):
  return False  # placeholder.

def any_on_bar(state, who):
  return who in state.bar

def remove_from_bar(new_state, who):
  #removes a white from start of bar list,
  # or a red from the end of the bar list.
  if who==W:
    del new_state.bar[0]
  else:
    new_state.bar.pop()
  print("After removing a "+get_color(who)+" from the bar,")
  print("  the bar is now: "+str(new_state.bar))

def handle_move_from_bar(state, who, die):
  # We assume there is a piece of this color available on the bar.
  if who==W: target_point=die
  else: target_point=25-die
  pointList = state.pointLists[target_point-1]
  if pointList!=[] and pointList[0]!=who and len(pointList)>1:
     print("Cannot move checker from bar to point "+str(target_point)+" (blocked).")
     return False
  new_state = bgstate(state)
  new_state = hit(new_state, pointList, target_point)
  remove_from_bar(new_state, who)
  new_state.pointLists[target_point-1].append(who)
  return new_state

def bearing_off_allowed(state, who):
  # True provided no checkers of this color on the bar or in
  # first three quadrants.
  if any_on_bar(state, who): return False
  if who==W: point_range=range(0,18)
  else: point_range=range(6,24)
  pl = state.pointLists
  for i in point_range:
    if pl[i]==[]: continue
    if pl[i][0]==who: return False
  return True

def win_detected(state, who):
  if who==W: return len(state.white_off)==15
  else: return len(state.red_off)==15

run(agent1, agent2, TIME_LIMIT, deterministic=DETERMINISTIC)
# For use in testing:
#import testStates
#run(agent1, agent2, TIME_LIMIT, testStates.WHITE_TO_BEAR_OFF, deterministic=DETERMINISTIC)
#run(agent1, agent2, TIME_LIMIT, testStates.RED_TO_BEAR_OFF, deterministic=DETERMINISTIC)
#run(agent1, agent2, TIME_LIMIT, testStates.WHITE_ABOUT_TO_WIN, deterministic=DETERMINISTIC)
#run(agent1, agent2, TIME_LIMIT, testStates.WHITE_HIT_FROM_BAR, deterministic=DETERMINISTIC)
