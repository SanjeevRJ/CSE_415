'''Farmer_Fox.py
by Sanjeev Janarthanan
UWNetID: sanjrj
Student number: 0751196

Assignment 2, in CSE 415, Winter 2020.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain. 
'''

SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Janarthanan']

LEFT = 0
RIGHT = 1
abbreviations = {"F":"Farmer", "f":"fox", "c":"chicken", "g":"grain"}
class State:
    def __init__(self, d = None):
        if d == None:
            #Each string contains a letter representation of which objects
            #are on which side of the river. (LEFT = 0, RIGHT = 1)
            d = {'Ffcg':["Ffcg", ""]}
            
        self.d = d
        
    def __eq__(self, s2):
        for prop in ['Ffcg']:
            if self.d[prop] != s2.d[prop]: return False
        return True
    
    def __str__(self):
        #.join will concat the two strings with everything in the list
        txt = "\n Left side: " + ", ".join([abbreviations[i] for i in self.d["Ffcg"][LEFT]]) + "\n"
        txt += "Right side: " + ", ".join([abbreviations[i] for i in self.d["Ffcg"][RIGHT]]) + "\n"
        return txt
    
    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        news = State({})
        news.d['Ffcg'] = [self.d['Ffcg'][L_or_R] for L_or_R in [LEFT,RIGHT]]
        return news

    #items: the items to be moved
    #move: the side (LEFT = 0, RIGHT =1) the items are to be moved to
    def can_move(self, items, move):
        for item in items:
            if item not in self.d['Ffcg'][move]:
                return False
        #Handles our two constraints with the fox, chicken, and grain
        else:  
            if "g" in self.d['Ffcg'][move] and "c" in self.d['Ffcg'][move] and not ("g" in items or "c" in items):
                return False 
            if "f" in self.d['Ffcg'][move] and "c" in self.d['Ffcg'][move] and not ("f" in items or "c" in items):
                return False 
            return True
        
    def move(self, items, move):
        copy = self.copy()
        
        copy.d['Ffcg'][move] = "".join(sorted([i for i in self.d['Ffcg'][move] if i not in items]))
        copy.d['Ffcg'][1-move] = "".join(sorted(self.d['Ffcg'][1-move] + items))
        return copy
    
def goal_test(s):
    return len(s.d['Ffcg'][LEFT]) == 0

def goal_message(s):
    return "You have succesfully moved you fox, grain, and chicken across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf
    
    def is_applicable(self, s):
        return self.precond(s)
    
    def apply(self, s):
        return self.state_transf(s)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

CREATE_INITIAL_STATE = lambda : State(d={'Ffcg':["Ffcg", ""]})   

Ffcg_combinations = ["F", "Ff", "Fc", "Fg"]

OPERATORS = [Operator(
        "Move " + " and ".join([abbreviations[i] for i in comb]) + " from the " + moves[0] + " to the " + moves[1] + " bank of the river.\n",
        lambda s, c=comb, m=int(moves[0] == "right") : s.can_move(c,m),
        lambda s, c=comb, m=int(moves[0] == "right") : s.move(c,m) )
        for comb in Ffcg_combinations for moves in [("left","right"), ("right","left")] ]    

GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
    