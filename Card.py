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
import numpy as np
int_to_resource =  dict(zip(range(8), ("gold", "clay",  "stone", "ore", "wood", "glass", "paper", "silk")))

resource_to_int = dict( zip(("gold", "clay",  "stone", "ore", "wood", "glass", "paper", "silk"), range(8)))


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

    def on_build(self, player):
        """
        All cards require a player argument so we know who to apply the effect to :)
        """
        print "ahhh base class\r",

    def score(self):
        print "ahh base class\r",

    def deepcopy(self):
        copy_costs = deepcopy(self.costs)
        new_obj = (Card(name=self.name, cardtype=self.cardtype, age=self.age, 
                               costs=copy_costs, card_text=self.card_text, 
                               upgrades=self.upgrades, players=self.players, meta=self.meta))
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

    def __eq__(self, other):
        return self.name == other.name
          

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
    
    def deepcopy(self):
        copy_costs = deepcopy(self.costs)
        new_obj = (CivilianCard(name=self.name, cardtype=self.cardtype, age=self.age, 
                               costs=copy_costs, card_text=self.card_text, 
                               upgrades=self.upgrades, players=self.players, meta=self.meta))
        return new_obj
        

    def on_build(self, player):
        print "building Civilian Card"

class CommerceCard(Card):
    def __init__(self, **kwargs):
       Card.__init__(self, **kwargs)

    def on_build(self, player):
      print "CommerceCard class"
    
    def deepcopy(self):
        copy_costs = deepcopy(self.costs)
        new_obj = (CommerceCard(name=self.name, cardtype=self.cardtype, age=self.age, 
                               costs=copy_costs, card_text=self.card_text, 
                               upgrades=self.upgrades, players=self.players, meta=self.meta))
        return new_obj

    

class CommerceMarketCard(CommerceCard):
    """
    What about the case where it is a fixed bonus? the level 2 markets are like this.
    I think we can just have another class nbd

    Tavern,Commerce,1,0,0,0,0,0,0,0,0,5G,,4-5-7,
    East Trading Post,Commerce,1,0,0,0,0,0,0,0,0,PurchaseNatural-R,,3-7,
    West Trading Post,Commerce,1,0,0,0,0,0,0,0,0,PurchaseNatural-L,,3-7,
    Marketplace,Commerce,1,0,0,0,0,0,0,0,0,PurchaseManufactured-LR,,3-6,
    """
    def __init__(self, **kwargs):
      CommerceCard.__init__(self, **kwargs)
      self.purchase_from = self.card_text.split("-")[1]
      self.purchase_what = self.card_text.split("-")[0].strip("Purchase")
       

    def on_build(self, player):

        zeroes = [0,0,0,0, 0,0,0,0] 
        if self.purchase_what == "Natural":
          to_add = [0,1,1,1, 1,0,0,0]
        elif self.purchase_what == "Manufactured":
          to_add = [0,0,0,0, 0,1,1,1]
        else:
          raise Exception("Trying to build invalid market type. This should not happen so please dont")
        #so there is a case where we have both
        if "L" == self.purchase_from:
          player.discounted_resources[0].append(to_add) 
          player.discounted_resources[0].append(zeroes)
        elif "R" == self.purchase_from:
          player.discounted_resources[1].append(to_add)
          player.discounted_resources[1].append(zeroes)
        elif "LR" == self.purchase_from:
          player.discounted_resources[0].append(to_add)
          player.discounted_resources[1].append(to_add)

    def deepcopy(self):
        copy_costs = deepcopy(self.costs)
        new_obj = (CommerceMarketCard(name=self.name, cardtype=self.cardtype, age=self.age, 
                               costs=copy_costs, card_text=self.card_text, 
                               upgrades=self.upgrades, players=self.players, meta=self.meta))
        return new_obj
            


class MilitaryCard(Card):
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        pass

class GuildCard(Card):
    # We really have two types of guild cards, scoring cards and board effect cards,
    #     an open question is how to capture this properly, such that its easy to extend
    #     python sippets would be intersting as card text
    #    Commerce-1VP-LR
    def __init__(self, **kwargs):
        Card.__init__(self, **kwargs)
        #if it is the kind we want it to be, do the following
        if self.name != "Scientists Guild":
            how, what, self.where = self.card_text.split("-")
            self.whats = how.split(";") #one is VP one is MP
            self.hows = what.split("|") #should be card types, wonders, or LossBell
            #where = "LMR" are possible

    def score(self):
        if self.name != "Scientists Guild":
            pass
            #wait how do we score if we dont have player information what the fuck
        #if self.whats:
        
        

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
        parsed = self.card_text.split(" ")

    def on_build(self, player):
        #how do we define that weird or relationship
        """ 
        Stone OR Wood, Stone AND Stone, Stone
        """
        arr = self.card_text.split(" ")
        to_add = [0,0,0,0 ,0,0,0,0]
        if len(arr) > 1:
          boolean = arr[1]
          res = (arr[0].lower(), arr[2].lower())
          to_add[resource_to_int[res[0]]] += 1
          to_add[resource_to_int[res[1]]] += 1
        else:
          boolean = None
          to_add[resource_to_int[arr[0].lower()]] += 1

        to_add = np.asarray(to_add)
        if boolean == "OR":
          player.xor_resources.append(to_add)
        else:
          player.resources += to_add
    
    def deepcopy(self):
        """
        >>>> We were working on this, the bug is we need to put the kewyrods in for it to work.
              after that things should work and we are checking to see that the resources changed for each player<<<<<
        """
        copy_costs = deepcopy(self.costs)
        new_obj = (NaturalCard(name=self.name, cardtype=self.cardtype, age=self.age, 
                               costs=copy_costs, card_text=self.card_text, 
                               upgrades=self.upgrades, players=self.players, meta=self.meta))
        return new_obj


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
        
        card = None
        if cardtype == "Civilian":
            card = CivilianCard(name=name,cardtype=cardtype,age=int(age), costs = costs,   \
                           card_text=c_text, upgrades=upgrades.split(','), meta = meta,    \
                           players=map(int, players.split("-")))
        elif cardtype == "Natural resource":
            card = NaturalCard(name=name,cardtype=cardtype,age=int(age), costs = costs,   \
                           card_text=c_text, upgrades=upgrades.split(','), meta = meta,    \
                           players=map(int, players.split("-")))  
        elif cardtype == "Commerce":
            if "Purchase" in c_text:
              card = CommerceMarketCard(name=name,cardtype=cardtype,age=int(age),costs=costs, \
                             card_text=c_text, upgrades=upgrades.split(','), meta = meta,    \
                             players=map(int, players.split("-")))

            else:
              card = CommerceCard(name=name,cardtype=cardtype,age=int(age),costs=costs,       \
                             card_text=c_text, upgrades=upgrades.split(','), meta = meta,   \
                             players=map(int, players.split("-")))
        else:
            card = Card(name=name, cardtype=cardtype, age=int(age), costs = costs,         \
                           card_text=c_text, upgrades=upgrades.split(','), meta = meta,    \
                           players=map(int, players.split("-"))) 
        cards.append(card)     


        
        #this just setups a set of card objects, not great for data science
    return cards



if __name__ == "__main__":
    import sys
    cards = card_parser(sys.argv[1])
    for card in sorted(cards): 
        print card.deepcopy()


    
