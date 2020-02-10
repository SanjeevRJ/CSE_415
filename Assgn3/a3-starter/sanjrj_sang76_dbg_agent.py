'''sanjrj_sang76_dbg_agent.py
by Sanjeev Janarthanan and Andrew Sang
UWNetIDs: sanjrj and sang76

This file was created from scratch.

Assignment 3, in CSE 415, Winter 2020.
 
This file implements an agent which can play a deterministic version of backgammon
where the dice roll always results in 1,6. This agent uses minimax search with
alpha-beta pruning to determine its move.
'''

from backgState import *

global NUM_POINTS
global BAR_PT
global BEARED_OFF
global SPECIAL_FUNC   

global prune
global cutoffs
global states
global cutoffs
global maxPly
global func

#Class variables 
NUM_POINTS = 24
BAR_PT= 0
BEARED_OFF = -1

#Equivalent of instance variables
func = None
prune = True
cutoffs = 0
states = 0
maxPly = 3

#Takes in the current state of the game and the current dice roll and outputs
#the best move.
def move(state, die1, die2):
    global states
    global maxPly
    
    #The first iteration of minimax search is started here.
    best_val1 = None
    best_val2 = None
    who = state.whose_move
    if who == W:
        best_val1 = -100000
        best_val2 = -100000
    else: 
        best_val1 = 100000
        best_val2 = 100000 
    who = state.whose_move
    poss_moves = possibleMoves(state, die1, die2)
    best_moves = {}
    states = 0
    for move in poss_moves:
        new_state = bgstate(old = state)
        mod_new_state(new_state, who, move)
        new_state.whose_move = 1-who
        new_val = minimax(new_state, maxPly, die1, die2, -100000, 100000)
        best_moves[(move[0], move[1])] = new_val

    move_str =  bestMove(best_moves, who, die1, die2, best_val1, best_val2)       
    return move_str

#Takes in a dictionary of best_moves and their associated state values and determines
#the best possible move.
def bestMove(best_moves, who, die1, die2, best_val1, best_val2):
    move1 = "p"
    move2 ="p"
    for move, val in best_moves.items():
        if who == W:
            #Accounts for the case where the move is from the bar.
            if move[0] == 0 and move[1] == die1:
                move1 = move
            if move[0] == 0 and move[1] == die2:
                move2 = move
            #Make sure the move increases the value, doesn't move the same checker
            #as the other move, and that moves from the bar take priority.
            if move[1]-move[0] == die1 and val > best_val1 and not (move2 != "p" and
                   move[0] == move2[0]) and not (move1 != "p" and move1[0] == 0):
                move1 = move
                best_val1 = val
            if move[1]- move[0] == die2 and val > best_val2 and not (move1 != "p" and
                   move[0] == move1[0]) and not (move2 != "p" and move2[0] == 0):
                move2 = move
                best_val2 = val
        else:
            if move[0] == 0 and move[1] == NUM_POINTS-die1+1:
                move1 = move
            if move[0] == 0 and move[1] == NUM_POINTS-die2+1:
                move2 = move
            if move[0]-move[1] == die1 and val < best_val1 and not (move2 != "p" and
                   move[0] == move2[0]) and not (move1 != "p" and move1[0] == 0):
                move1 = move
                best_val1 = val
            if move[0]- move[1] == die2 and val < best_val2 and not (move1 != "p" and
                   move[0] == move1[0]) and not (move2 != "p" and move2[0] == 0):
                move2 = move
                best_val2 = val
                
    move_str = str(move1[0]) + "," + str(move2[0])
    #Since die1 always goes fist, pass if the second move involves moving a checker
    #from the bar
    if move2[0] == 0 and move1 != "p":
        move1 = move2
        move2 = "p"
        move_str = str(move1[0]) + "," + str(move2[0]) + "," + "R"
    #Bug in game master--if the first move is a pass the game crashes.
    if move1 == "p" and move2 != "p":
        move_str = str(move2[0]) + "," + str(move1[0]) + "," + "R"
    if move1 == "p" and move2 == "p":
        move_str = "p"
    
    return move_str

#Changes whether or not alpha-beta pruning is used based on the boolean parameter.
def useAlphaBetaPruning(prune1):
    global prune
    prune = prune1

#Returns the current amount of cutoffs and states.
def statesAndCutoffsCounts():
    global cutoffs
    global states
    return (cutoffs, states)

#Sets the max depth minimax will go to. If -1, the furthest possible depth.    
def setMaxPly(maxply=-1):
    global maxPly
    maxPly = maxply

#If a function is passed it is used for static evaluation.
def useSpecialStaticEvalFunction(func1):
    global func
    if func1 != None:
        func = func1

#Returns a dictionary of all the checkers at occupied locations. Basically translates
#pointsList to a dicionary.
def getLocations(state):
    locations = {}
    for i, row in enumerate(state.pointLists):
        curCheckers = []
        for j, checker in enumerate(row):
            if checker == W:
                curCheckers.append(W)
            if checker == R:
                curCheckers.append(R)
        locations[i+1] = curCheckers
    
    return locations

#Returns a list of the possible moves of form [x,y] given the current roll. 
def possibleMoves(state, die1, die2):
    moves = []
    bearOff = True
    locations = getLocations(state)
    who = state.whose_move
    die_on_bar = False
    
    #Handles the case of a checker being on the bar.
    if who in state.bar:
        barLoc1 = None
        barLoc2 = None
        die_on_bar = True
        if who == W:
            barLoc1 = die1
            barLoc2 = die2
        else:
            barLoc1 = NUM_POINTS-die1+1
            barLoc2 = NUM_POINTS-die2+1
        if locations[barLoc1].count(1-who) <= 1:
            moves.append([BAR_PT, barLoc1])
            locations[barLoc1].append(who)
        elif locations[barLoc2].count(1-who) <= 1:
            moves.append([BAR_PT, barLoc2])
            locations[barLoc2].append(who)
            
    homeLim = None
    if who == W:
        homeLim = NUM_POINTS - 5
    else:
        homeLim = 6
    furthest_white = NUM_POINTS
    furthest_red = 1
    for loc, checkers in locations.items():
        if who == W:
            if loc == 0:
                continue
            if loc <= furthest_white:
                furthest_white = loc
            if who in checkers:
                nextLoc1 = loc+die1
                nextLoc2 = loc+die2
                if loc < homeLim:
                    if who in locations[loc]: 
                        bearOff = False
                else:
                    #Handles bearing off
                    if who in locations[loc] and bearOff:
                        if nextLoc1 == NUM_POINTS + 1 or (loc == furthest_white and
                                       nextLoc1 == NUM_POINTS + 2):
                            moves.append([loc, nextLoc1])
                        if nextLoc2 == NUM_POINTS + 1 or (loc == furthest_white and
                                       nextLoc2 == NUM_POINTS + 2):
                            moves.append([loc, nextLoc2])
                    
                if not nextLoc1 > NUM_POINTS and not die_on_bar:
                    if locations[nextLoc1].count(1-who) <= 1:
                        moves.append([loc,nextLoc1])
                if not nextLoc2 > NUM_POINTS and not die_on_bar:
                    if locations[nextLoc2].count(1-who) <= 1:
                        moves.append([loc,nextLoc2])
                
        else:
            #Loc is essentially reversed to (24,0) so that it's easier to keep
            #track of if checkers are outside red's home board.
            loc = NUM_POINTS-loc+1
            if loc == 0:
                continue
            checkers = locations[loc]
            if who in checkers:
                if loc >= furthest_red:
                    furthest_red = loc
                furthest_white ==loc
                nextLoc1 = loc-die1
                nextLoc2 = loc-die2
                if loc > homeLim:
                    if who in locations[loc]: 
                        bearOff = False
                else:
                    if who in locations[loc] and bearOff:
                        if nextLoc1 == 0 or (loc == furthest_red and
                                       nextLoc1 == -1):
                            moves.append([loc, nextLoc1])
                        if nextLoc2 == 0 or (loc == furthest_red and
                                       nextLoc2 == -1):
                            moves.append([loc, nextLoc2])
                        
                if not nextLoc1 < 1 and not die_on_bar:
                    if locations[nextLoc1].count(1-who) <= 1:
                        moves.append([loc,nextLoc1])
                if not nextLoc2 < 1 and not die_on_bar:
                    if locations[nextLoc2].count(1-who) <= 1:
                        moves.append([loc,nextLoc2])        
    return moves

#Returns a numeric evaluation of the current state. The evaluation is higher if it
#benefits the maximizing player, white, and same vice versa.
def staticEval(state): 
    val = 0
    for i in range(0,len(state.pointLists)):
        for j in range(0,len(state.pointLists[i])):
            checker = state.pointLists[i][j]
            if checker == W:
                val += i
            if checker == R:
                val -= (NUM_POINTS-i)
           
    for i in state.white_off:
        val += NUM_POINTS*10
    for i in state.red_off:
        val -= NUM_POINTS*10
    
    for i in state.bar:
        if i == W:
            val -= 3
        if i == R:
            val += 3

    return val

#Modifies the current bgstate() object so it reflects the result of the move
#parameter.
def mod_new_state(new_state, who, move):
    newPts = new_state.pointLists
    if move[1] > NUM_POINTS or move[1] < 1:
        if who == W:
            newPts[move[0]-1].remove(who)
            new_state.white_off.append(who)
            new_state.pointLists = newPts
        else: 
            newPts[move[0]-1].remove(who)
            new_state.red_off.append(who)
            new_state.pointLists = newPts
    elif move[0] == BAR_PT:
        new_state.bar.remove(who)
        newPts[move[1]-1].append(who)
        new_state.pointLists = newPts
    else:
        newPts[move[0]-1].remove(who)
        newPts[move[1]-1].append(who)
        new_state.pointLists = newPts
           
def minimax(state, plyLeft, die1, die2, alpha, beta):
    global cutoffs
    global prune
    global func
    global states

    who = state.whose_move
    if plyLeft == 0:
        if func != None:
            return func(state)
        else:
            return staticEval(state)
    
    best_val = None
    if who == W:
        best_val = -10000
    else: 
        best_val = 10000
    poss_moves = possibleMoves(state, die1, die2)
    for move in poss_moves:
        states += 1
        new_state = bgstate(old = state)
        mod_new_state(new_state, who, move)
        new_state.whose_move = 1-who
        new_val = minimax(new_state, plyLeft -1, die1, die2, alpha, beta)
        
        if who == R:
            if new_val < best_val:
                best_val = new_val
            if best_val < beta and prune:
                beta = best_val
                if alpha >= beta:
                    cutoffs += 1
                    break
        else:
            if new_val > best_val:
                best_val = new_val  
            if best_val > alpha and prune:
                alpha = best_val
                if alpha >= beta:
                    cutoffs += 1
                    break
                
    return best_val

    
        