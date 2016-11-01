
class Action():
    def __init__(self, player):
        self.player = player

    def take_action(self):
        raise Exception("do not instantiate Action base class")

class PickAction(Action):
    """
    PickAction - Generic pick action. accepts a card index and player object. Removes that card from the players pack and puts it in their structures.
    """
    def __init__(self, player, card_idx):
        Action.__init__(self, player)
        self.card_idx = card_idx

    def take_action(self):
        self.player.structures.append(self.player.current_hand.pop(self.card_idx))
        print ""

