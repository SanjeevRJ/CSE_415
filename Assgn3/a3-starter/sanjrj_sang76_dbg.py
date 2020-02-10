# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:29:18 2020

@author: sanje
"""

from backgState import *

class dbgAgent:
    
    NUM_POINTS = 24
    BAR_PT= 0
    BEARED_OFF = -1
    SPECIAL_FUNC = False

    def __init__(self):
        self.maxPly = -1
        self.plyLeft = self.maxPly
        self.prune = False
        self.cutoffs = 0
        self.states = 0      
        
    def move(self, state, die1, die2):
        who = state.whose_move
        move = minimax(state, who, 4, die1, die2)
        return move[1]
    
    def useAlphaBetaPruning(self, prune=False):
        self.prune = prune
        
    def statesAndCutoffsCounts(self):
        return (cutoffs, states)
        
    def setMaxPly(self, maxply=-1):
        self.maxply = maxply
        
    def useSpecialStaticEvalFunction(self, func):
        return func
        
    def getLocations(self, state):
        locations = {}
        for i, row in enumerate(state.pointLists):
            curCheckers = []
            for j, checker in enumerate(row):
                if checker == W:
                    curCheckers.append(W)
                else:
                    curCheckers.append(R)
            locations[i] = curCheckers
        
        return locations
    
    def possibleMoves(self, state, die1, die2):
        moves = []
        bearOff = True
        locations = getLocations(state)
        who = state.whose_move
        
        barLoc1 = None
        barLoc2 = None
        if who == W:
            barLoc1 = die1
            barLoc2 = die2
        else:
            barLoc1 = NUM_POINTS-die1+1
            barLoc2 = NUM_POINTS-die2+1
        if who in state.bar:
            if locations[barLoc1].count(1-who) <= 1:
                moves.append([BAR_PT, barLoc1])
                locations[barLoc1].append(who)
            if locations[barLoc2].count(1-who) <= 1:
                moves.append([BAR_PT, barLoc2])
                locations[barLoc2].append(who)
        homeLim = None
        if who == W:
            homeLim = NUM_POINTS - 5
        else:
            homeLim = 6
        for loc, checkers in locations.items():
            nextLoc1 = None
            nextLoc2 = None
            if who == W:
                if who in checkers:
                    if loc < homeLim:
                        if who in locations[loc]: 
                            bearOff = False
                    else:
                        if who in locations[loc] and bearOff: 
                            moves.append([loc, -1])
                        
                    nextLoc1 = loc+die1
                    nextLoc2 = loc+die2
                    if nextLoc1 > NUM_POINTS:
                        continue
                    elif nextLoc2 > NUM_POINTS:
                        continue
                    
            else:
                if who in checkers:
                    if loc > homeLim:
                        if who in locations[loc]: 
                            bearOff = False
                    else:
                        if who in locations[loc] and bearOff: 
                            moves.append([loc, -1])       
                    nextLoc1 = loc-die1
                    nextLoc2 = loc-die2
                    if nextLoc1 < 1:
                        continue
                    elif nextLoc2 < 1:
                        continue

            if locations[nextLoc1].count(1-who) <= 1:
                moves.append([loc,nextLoc1])
            elif locations[nextLoc2].count(1-who) <= 1:
                moves.append([loc,nextLoc2])
        
        return moves
        
    def staticEval(self, state): 
        val = 0
        for i, row in enumerate(state.pointLists):
            for j, checker in enumerate(row):
                if checker == W:
                    val += (NUM_POINTS - i)
                else:
                    val -= (i-1)
               
        for i in state.white_off:
            val += NUM_POINTS
        for i in state.red_off:
            val -= NUM_POINTS
        
        return val
                
    def minimax(self, state, who, plyLeft, die1, die2):
        if self.plyLeft == 0:
            return self.staticEval()
        
        bestVal = None
        if who == W:
            bestVal = -10000
        else: 
            bestVal = 10000
        
        poss_moves = possibleMoves(state, die1, die2)
        best_move = None
        for move in poss_moves:
            new_state = bgstate(old = state)
            self.states += 1
            newPts = new_state.pointLists
            if move[0] == BEARED_OFF:
                if who == W:
                    new_state.white_off.append(who)
                else: 
                    new_state.red_off.append(who)
            else:
                newPts[moves[0]].remove(who)
                newPts[moves[1]].append(who)
            new_state.pointLists = newPts
            new_val = (new_state, 1-who, plyLeft -1)
            
            if who == W:
                if new_val > bestVal:
                    bestVal = new_val
                    best_move = move
            else:
                if new_val < bestVal:
                    bestVal = new_val
                    best_move = move
                    
        return best_move 



        
        
    
    
        
    
        