"""
Card - Container class for the different card types. At some point we will need to decide 
if we want a single master class or many child classes. (probably child)

Oh and we need a good copy constructor in this case.

What is in a card?

Cost
Bonus (bonus could be resource or skill bonus) -- sometimes bonuses depend on player state
    - resource
        a. manufactured
        b. natural
    - flat gold
    - victory points
    - marketplace
    - science

    classes of cards:
        simple class (gives you "stuff" --  resource/science/fight/points)
        complex class (depends on game state, gives you "stuff")
        
    
    
Type
"""
from termcolor import colored
from copy import copy, deepcopy
int_to_resource =  dict(zip(("gold", "clay",  "stone", "ore", "wood", "glass", "paper", "silk"), range(8)))


class Card():
    """
    Not a very well defined class yet. We will get there when we are implementing rules and stuff.
    """
    def color_lookup(self):
        # wow such functional
        return {"Civilian": "blue", "Military":"red", "Guild":"magenta","Science":"green",\
                  "Natural resource": "white", "Manufactured good": "cyan", \
                  "Commerce":"yellow"}[self.cardtype]


    def __init__(self, name, cardtype, age, costs, card_text, upgrades, players, meta=""):
        self.name = name
        self.cardtype=cardtype
        self.age=age
        self.costs=costs
        self.card_text=card_text
        self.upgrades=upgrades
        self.players = players
        self.meta = meta
        self.__params__ =["name", "cardtype", "age", "cost", "card_text", "upgrades", "players"]

    def on_build(self):
        raise Exception("Not implemented error. Do not instantiate this class")

    def score(self):
        raise Exception("Not implemented error. Do not instantiate this class")

    def deepcopy(self):
        copy_costs = deepcopy(self.costs)
        new_obj = Card(self.name, self.cardtype, self.age, copy_costs, \
                      self.card_text, self.upgrades, self.players, self.meta)
        return new_obj
        
    
    def __str_costs(self):
        return "".join(("Costs:\t", "$" * self.costs[0], "C"*self.costs[1], "S"*self.costs[2],\
                                   "O" * self.costs[3], "W"*self.costs[4], "G"*self.costs[5],\
                                   "P" * self.costs[6], "S" * self.costs[7]))

    def __str__(self):
        to_ret="\t".join( (self.name, str(self.age), self.__str_costs(), \
                            " ,".join(self.upgrades), self.card_text) ) 
        return colored(to_ret, self.color_lookup() )

    def __lt__(self, other):
        """
        what is more functional? age or players? age.
        sorting rules:
            age => cardtype => name
        """ 
        if self.age != other.age:
            return self.age < other.age 
        elif self.cardtype != other.cardtype:
            return self.cardtype < other.cardtype
        else:
            return self.name < other.name

    def __gt__(self, other):
        if self.age != other.age:
            return self.age > other.age 
        elif self.cardtype != other.cardtype:
            return self.cardtype > other.cardtype
        else:
            return self.name > other.name

    def n_instances(self, n_players=3):
        """
        Returns how many of this card there should be in the deck
        Does not handle guilds.
        """
        val=0
        for p in self.players: 
            if p <= n_players: 
                val += 1
        return val

class CivilianCard(Card):
    """
    Score is just VP
    """
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        self.vp = int(self.card_text.strip("VP"))
        #setup parsing rules

    def score(self):
        return self.vp

    def on_build(self): pass

class CommerceCard(Card):
    def __init__(self, **kwargs):
        pass

class MilitaryCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass

class GuildCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass

class ScienceCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass

class ManufacturedCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass

class NaturalCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass


def card_parser(filename="Cards.csv"):
    """
    card_parser - parses the cards.csv file. this should be a configuration parameter. these 
                  docs need production rules.

    returns - list of Card objects.
    """
    #Name,Type,Age,cost_gold,cost_clay,cost_stone,cost_ore,cost_wood,cost_glass,cost_paper,cost_silk,CardText,UpgradesToo,Players,Meta
    cards = []
    for line in open(filename, 'r'):
        if "#" in line[0]: continue
        if line.strip() == "": continue     
        name,cardtype,age,c_gold,c_brick,c_stone,c_ore,c_wood,c_glass,c_paper,c_silk,c_text,\
             upgrades,players,meta = line.strip().split(",")
        costs = map(int, [c_gold, c_brick, c_stone, c_ore, c_wood, c_glass, c_paper, c_silk])
        
        #if cardtype == "Civilian":
            


        cards.append( Card(name=name, cardtype=cardtype, age=int(age), costs = costs,       \
                           card_text=c_text, upgrades=upgrades.split(','), meta = meta,     \
                           players=map(int, players.split("-"))) )
        
        #this just setups a set of card objects, not great for data science
    return cards



if __name__ == "__main__":
    import sys
    cards = card_parser(sys.argv[1])
    for card in sorted(cards): 
        print card.deepcopy()


    