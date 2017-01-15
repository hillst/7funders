import State
class Action():
    def __init__(self, state):
        self.state = state

    def take_action(self):
        raise Exception("do not instantiate Action base class")

class MockAction(Action):
    def __init__(self, state=None):
        Action.__init__(self, state)
  
    def take_action(self):
        pass

class PayMockAction(Action):
    def __init__(self, state, pay=[0,0], player_idx=None):
        Action.__init__(self, state)
        self.pay = pay
        self.player_idx = player_idx
  
    def take_action(self):
        player, west, east = self.state.get_player_west_east(self.player_idx)
        #assert the action is legal
        if sum(self.pay) > player.resources[0]:
          print "illegal payment action"
        player.resources[0] -= sum(self.pay)
        west.resources[0] += self.pay[0]
        east.resources[0] += self.pay[1]
  

class BuildPayMockAction(Action):
    def __init__(self, state, pay=[0,0], player_idx=None, card_idx=None):
        Action.__init__(self, state)
        self.pay = pay
        self.player_idx = player_idx
        self.card_idx = card_idx
        self.player, self.west, self.east = self.state.get_player_west_east(self.player_idx)
        self.card = self.player.current_hand[self.card_idx]
  
    def take_action(self):
        player, west, east = self.state.get_player_west_east(self.player_idx)
        #assert the action is legal
        if sum(self.pay) > player.resources[0]:
          print "illegal payment action"
        player.resources[0] -= sum(self.pay)
        west.resources[0] += self.pay[0]
        east.resources[0] += self.pay[1]
        #get the card index
        card = player.current_hand[self.card_idx]
        player.structures.append(card)
        card.on_build(player)
        del player.current_hand[self.card_idx]

    def get_card_type(self):
        return self.card.cardtype

    def __str__(self):
        _str = "=======BUILD ACTION======="  + "\n"
        _str += self.player.current_hand[self.card_idx].__str__() + "\n"
        _str += "Player" + str(self.player_idx) + "\n"
        _str += "Purchases: " +  "-".join(map(str,self.pay))  + "\n"
        return _str



class TrashMockAction(Action):
    def __init__(self, state, player_idx=None, card_idx=None):
        Action.__init__(self, state)
        self.player_idx = player_idx
        self.card_idx = card_idx
        self.player, self.west, self.east = self.state.get_player_west_east(self.player_idx)
  
    def take_action(self):
        player, _, _ = self.state.get_player_west_east(self.player_idx)
        player.resources[0] += 2
        #get the card index
        card = player.current_hand[self.card_idx]
        self.state.discard.append(card)
        del player.current_hand[self.card_idx]

    def __str__(self):
        _str = "=======TRASH ACTION======="  + "\n"
        _str += self.player.current_hand[self.card_idx].__str__() + "\n"
        _str += "Player" + str(self.player_idx) + "\n"
        return _str
  
