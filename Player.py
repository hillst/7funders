"""
Players.py

"""

class Player():
    def __init__(self, name="Player"):
        """
        We may want these in state.
        """
        self.structures = [] # by type? Should we have a structure type? 
        self.name = name
                             #It would make sense but its kind of defined in card
        self.wonders = None
        self.current_hand = [] #???
        self.active_leaders = []
        self.inactive_leaders = []
        self.resources = {"resource_name": 0}

    #getters and setters

    def __str__(self):
        return self.name

