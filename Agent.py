from random import choice
import numpy as np
from util import names
from Action import BuildPayMockAction
class Agent():
    def __init__(self):
        raise Exception("Cannot instantiate base Agent class")
    
    def select_action(self, state, legal_actions=[]):
        raise Exception("Cannot use base class alone")

class PlayerAgent(Agent):
    def __init__(self):
        pass
    
    def select_action(self, state, legal_actions=[]):
        self.clear_screen()
        player_idx = legal_actions[0].player_idx
        player, west, east = state.get_player_idx_west_east(player_idx)
        print "Your structures"
        self.draw_board(state, player )
        print
        print "West resources"
        self.draw_resources(state, west)
        print "East resources"
        self.draw_resources(state, east)
        print "Your resources"
        self.draw_resources(state, player)
        print "Your gold"
        self.draw_gold(state, player)
        print "Your hand"
        self.draw_hand(state, player, legal_actions)

        action = -1 
        while int(action) >= len(legal_actions) or int(action) < 0:
          action = raw_input("Select an action (0 -" + str(len(legal_actions)-1) +")")
        return legal_actions[int(action)]
    
    def draw_gold(self, state, player_idx):
        player = state.players[player_idx]
        print player.resources[0]
     
    
    def draw_board(self, state, player_idx):
        player = state.players[player_idx]
        for s in sorted(player.structures, key=lambda x : x.cardtype , reverse=True): #cards
            print s 

    def draw_hand(self, state, player_idx, legal_actions):
        player = state.players[player_idx]
        for s in player.current_hand:
            print s
        for action in legal_actions:
            print action
  
    def draw_resources(self, state, player_idx):
        print state
        print state.players
        print state.players[player_idx]
        print state.players[player_idx].resources[1:]
        for i, resource in enumerate(state.players[player_idx].resources[1:]):
            print names[i], resource,
        print ""
        print "XOR resources:"
        for i, resource in enumerate(state.players[player_idx].xor_resources):
            print resource[1:],
        print ""

    def clear_screen(self):
        print " " * 200 + "\n"

    

    
class BuildFirstAgent(Agent):
    def __init__(self):
        pass
        
    def select_action(self, state, legal_actions=[]):
        scores = self.weigh_actions(legal_actions)
        return legal_actions[np.argmax(scores)]
    
    def __str__(self):
        return "BuildFirstAgent"

    def weigh_actions(self, actions):
        scores = []
        for action in actions:
          score = 0
          if action.__class__ == BuildPayMockAction:
            score += 1
            if action.card.cardtype == "Natural resource":
              score += 1
          scores.append(score) 
        return np.asarray(scores)

class RandomAgent(Agent):
    def __init__(self):
        pass
        
    def select_action(self, state, legal_actions=[]):
        return choice(legal_actions)
    
    def __str__(self):
        return "RandomAgent"

    
def test():
    print RandomAgent()

if __name__ == "__main__":
    test()
         
