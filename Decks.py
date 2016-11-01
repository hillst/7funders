import Card

class Deck():
    """
    Deck -- Base deck class, responsible for building decks and packs for each age.

    This is a really simple wrapper class for shuffling and dealing essentially. It's not clear if the ages should be separate. Age three is the only age with "special" things going on.
    """
    
    def __init__(self, n_players=7):
        self.cards = Card.card_parser()
         
    def __len__(self):
        return len(self.cards)

    def __getitem__(self, i):
        return self.cards[i]

    def __setitem__(self, a, b):
        self.cards[a] = b

class Age1Deck(Deck):
    def __init__(self, n_players=7):
        Deck.__init__(self, n_players)
        new_cards = []
        for card in self.cards:
            if int(card.age) == 1: #i am your list comprehension now
                #in all seriousness this just adds the appropriate number of instances of cards
                [new_cards.append(card.deepcopy()) for i in range(card.n_instances(n_players))]
        self.cards = new_cards

            

class Age2Deck(Deck):
    """
    Deck corresonding to the second age.
    """
    def __init__(self, n_players=7):
        Deck.__init__(self, n_players)
        new_cards = []
        for card in self.cards:
            if int(card.age) == 2: 
                [new_cards.append(card.deepcopy()) for i in range(card.n_instances(n_players))]
        self.cards = new_cards

class Age3Deck(Deck):
    """
    Guild logic is all here, makes more sense to belong to the deck class
    """
    def __init__(self, n_players=7):
        from random import sample
        Deck.__init__(self, n_players)
        new_cards = []
        guilds = []
        for card in self.cards:
            if int(card.age) == 3: 
                if card.cardtype == "Guild":
                    guilds.append(card)
                else:
                    [new_cards.append(card.deepcopy()) for i in range(card.n_instances(n_players))]
            
        n_guilds = n_players+2 
        new_cards += sample(guilds, n_guilds) 
        self.cards = new_cards


def tests():
    """
    The test passees if all decks divide by zero for n players
    """
    for i in range(3, 8):
        for age, d in enumerate((Age1Deck(n_players=i), Age2Deck(n_players=i), Age3Deck(n_players=i))):
            test_pass=len(d.cards) % float(i) == 0
            print "AGE", "I"*(age+1), "PLAYERS", i, "TEST:", test_pass

if __name__ == "__main__":
    tests()
