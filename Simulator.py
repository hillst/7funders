import Player, State
from Action import PickAction
from Agent import RandomAgent


def test():
    """
    This test should run through a full game phase.

    Right now there is no player stuff going on
    """

    N_PLAYER = 3
    print "setting up game..."
    game = Simulator(agents=[RandomAgent() for _ in range(N_PLAYER)]) 
    
        
    #print len(game.agents), " players."

    print "starting age loop"

    #for age_deck in game.ages:
    for i in game.get_state().age_generator(): 
        print "Age: ", "I" * i
        for j in game.get_state().pick_generator():
            print "Card selection", j
            legal_actions = game.get_legal_actions()
            action_queue = []
            for i, agent in enumerate(game.agents):
                action = agent.select_action(game.get_state(), legal_actions[i])
                action_queue.append(action)

            for action in action_queue: action.take_action()

            game.pass_packs()

        game.get_state().next_age()
        game._deal_pass_packs()

   

        
    for player in game.get_state().players:
        print player, "structures:"
        for s in sorted(player.structures, key=lambda x : x.cardtype , reverse=True): #cards
            print s 
        



 
    """
    Some notes
            #state.execute_action_queue
            #now we need to send a list of actions to agents to select from -- essentially select_action should be called on every player
            # thats trivial though because our agents work!
    """
   
    print "game over"

class Simulator():
    def __init__(self, agents = [None, None, None]):
        """
        should act as a surrogate between agents, actions, and states 

    
        players should probably be a part of the game state.

        finally we should have an arbiter (main) run the simulation

        """
        self.agents = agents
        self._set_initial_state(n_players=len(agents))

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state.copy() # should this be a copy? probably, that or the passed object should be a copy.

    def get_agents(self):
        # returns a list of players/agents
        pass
        
    def get_rewards(self):
        # Compute full score with the game as-is? that or set to zero unless game is over. might be useful to do both.
        pass 
    
    def is_terminal_state(self):
        # is the game over?
        pass
    
    def take_action(self, action, agent):
        #take action a and agent p
        # we havent defined actions yet so chill out
        pass 

    def pass_packs(self):
        for player, pack in zip(self.get_state().players, self.get_state().rotate_hands()):
            player.current_pack = pack

    def _set_initial_state(self, n_players=7):
        """
        What does this entail? -- get the number of players, build the card decks
        """
        self.state = State.State(players=[Player.Player("Player" + str(i+1)) for i in range(n_players)])
        self._deal_pass_packs()

    def _deal_pass_packs(self):
        self.state.deal()
        #build decks
        
        for i,  p in enumerate(self.state.players):
            p.current_hand = self.state.packs[i]
    
    def get_legal_actions(self):
        """
        get_legal_actions - returns a 2d list of legal actions. The list is:
            (n_player x var), we have a list of legal actions for each player!
        """
        legal_actions = []
        for player in self.get_state().players:
            player_actions = []
            for idx, card in enumerate(player.current_hand):
                player_actions.append(PickAction(player, idx))
            legal_actions.append(player_actions)
        return legal_actions
                
                

    def copy():
        #important that we make a deep copy
        pass


    #why am i writing this in python this shit is  gon be too slow to do anything.... write it in a way that is easy to translate to c++


    


if __name__ == "__main__":
    test()
