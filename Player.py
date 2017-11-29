"""
Players.py

"""
from copy import deepcopy
import numpy as np
from util import names

class Player():
    def __init__(self, name="Player", resources=[0,0,0,0,0,0,0,0], xor_resources=None,\
                 current_hand=None, structures=None, starting_gold=3, discounted_resources=None):
        """
        We may want these in state.
        """
        if structures != None:
          self.structures = structures # by type? Should we have a structure type? 
        else:
          self.structures = []
       
        self.name = name
        self.wonders = None 
        player.west_natural= False
        player.west_manufactured = False
        player.east_natural= False
        player.east_manufactured= False

        if current_hand == None:
          self.current_hand = None
        else:
          self.current_hand = current_hand #I dont know if we need this
        self.starting_gold = starting_gold
    
    def __copy__(self):
        current_hand = deepcopy(self.current_hand)
        structures = deepcopy(self.structures)
        return Player(self.name, ,  current_hand, structures)

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __str__(self):
        #this could be much prettier.
        return (self.name + "\nGold:" + str(self.resources[0]) )
    

