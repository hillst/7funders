"""
Players.py

"""
from copy import deepcopy
import numpy as np
from util import names

class Player():
    def __init__(self, name="Player", resources=[0,0,0,0,0,0,0,0], xor_resources=[],\
                 current_hand=[], structures=None, starting_gold=3):
        """
        We may want these in state.
        """
        if structures != None:
          self.structures = structures # by type? Should we have a structure type? 
        else:
          self.structures = []
       
        self.name = name
        self.wonders = None # not implemented yet
        self.current_hand = current_hand #I dont know if we need this
        self.starting_gold = starting_gold
        if resources == "rand":
          self._rand_resources()
        else: 
          self.resources = np.asarray(resources, dtype='int32') #7,1 vector, i feel like this should be computable too.
        self.resources[0] = self.starting_gold
        self.xor_resources=[np.asarray(r, dtype='int32') for r in xor_resources]
  
    
    def _rand_resources(self):
        import random
        resources = [self.starting_gold] 
        for i in range(1,8):
            if random.random() > .5:
                resources.append(1)
            else:
                resources.append(0)    
        self.resources = np.asarray(resources , dtype='int32')

    
    def __copy__(self):
        res = deepcopy(self.resources)
        xor = deepcopy(self.xor_resources)
        current_hand = deepcopy(self.current_hand)
        structures = deepcopy(self.structures)
        return Player(self.name, res, xor, current_hand, structures)

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __str__(self):
        return (self.name + "\nGold:" + str(self.resources[0]) + 
                            "\nResources:" + "\t".join(names) + 
                            "\n\t" + "\t".join( map(str,self.resources[1:])))

