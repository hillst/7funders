from random import choice
class Agent():
    def __init__(self):
        raise Exception("Cannot instantiate base Agent class")
    
    def select_action(self, state, legal_actions=[]):
        raise Exception("Cannot use base class alone")

    
class RandomAgent(Agent):
    def __init__(self):
        pass
        
    def select_action(self, state, legal_actions=[]):
        if len(legal_actions) > 1:
          return choice(legal_actions[1:])
        else:
          return legal_actions[0]
    
    def __str__(self):
        return "RandomAgent"

def test():
    print RandomAgent()

if __name__ == "__main__":
    test()
         
