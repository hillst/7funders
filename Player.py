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
        self.wonders = None # not implemented yet
        if current_hand == None:
          self.current_hand = None
        else:
          self.current_hand = current_hand #I dont know if we need this
        self.starting_gold = starting_gold

        if discounted_resources == None:
          self.discounted_resources = [[],[]] #list of west,both,east -- may not hold up because there arent really "both" cards.
        else:
          self.discounted_resources = discounted_resources

        if xor_resources == None:
          self.xor_resources = []
        else:
          self.xor_resources = xor_resources

        if resources == "rand":
          self._rand_resources()
        else: 
          self.resources = np.asarray(resources, dtype='int32') #7,1 vector, i feel like this should be computable too.
        self.resources[0] = self.starting_gold
        self.xor_resources=[np.asarray(r, dtype='int32') for r in self.xor_resources]
  
    
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
        discounted_resources = deepcopy(self.discounted_resources)
        return Player(self.name, res, xor, current_hand, structures, discounted_resources = discounted_resources)

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __str__(self):
        return (self.name + "\nGold:" + str(self.resources[0]) + 
                            "\nResources:" + "\t".join(names) + 
                            "\n\t" + "\t".join( map(str,self.resources[1:])))

