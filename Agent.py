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
        return choice(legal_actions)
    
    def __str__(self):
        return "RandomAgent"

def test():
    print RandomAgent()

if __name__ == "__main__":
    test()
         
