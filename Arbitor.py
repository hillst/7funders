from Simulator import *
from Agent import PlayerAgent, RandomAgent

def setup_game():
    N_PLAYERS = int(raw_input("How many player(3-7)?"))
    if N_PLAYERS < 3:
      print "Not enough players."
      return -1

    
    player_agent = PlayerAgent()
    game = Simulator(agents=[player_agent]+[BuildFirstAgent() for _ in range(1,N_PLAYERS)]) 
    
  
    
    for i in game.get_state().age_generator(): 
        print "Age: ", "I" * i
        raw_input("any key to continue..")
        for j in game.get_state().pick_generator():
            print "Card selection", j
            
            legal_actions = game.get_legal_actions(game.get_state()) #get all legal actions for this player
            action_queue = []
            for i, agent in enumerate(game.agents):
                action = agent.select_action(game.get_state(), legal_actions[i])
                action_queue.append(action)
                print "Player {}".format(i)
                print "Takes action"
                print action

            for action in action_queue: 
                action.take_action()

            game.pass_packs()
            print "=========ENDING PICK " , j
            a = raw_input("any key to continue..")
        print "At end of age", i + 1
        for player in game.get_state().players:
            print player
            print "Structures:"
            for s in sorted(player.structures, key=lambda x : x.cardtype , reverse=True): #cards
                print s 

        game.get_state().next_age() #TODO hmmm
        game._deal_pass_packs()

def main():
    print "setting up game..."
    game = Simulator(agents=[BuildFirstAgent() for _ in range(N_PLAYERS)]) 
        
    print "starting age loop"

    for i in game.get_state().age_generator(): 
        print "Age: ", "I" * i
        for j in game.get_state().pick_generator():
            print "Card selection", j
            
            legal_actions = game.get_legal_actions(game.get_state()) #get all legal actions for this player
            action_queue = []
            for i, agent in enumerate(game.agents):
                action = agent.select_action(game.get_state(), legal_actions[i])
                action_queue.append(action)
                print "Player {}".format(i)
                print "Takes action"
                print action

            for action in action_queue: 
                action.take_action()
          
            game.pass_packs()
        print "At end of age", i + 1
        for player in game.get_state().players:
            print player
            print "Structures:"
            for s in sorted(player.structures, key=lambda x : x.cardtype , reverse=True): #cards
                print s 

        game.get_state().next_age()
        game._deal_pass_packs()

setup_game()
