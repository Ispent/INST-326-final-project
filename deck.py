from cards import Card

class Deck:
    """ Creates a deck object that will hold a number of card objects during the game

    Args:
        cards: list object that will hold each card object
    """

    def __init__(self):
        self.cards = []

    def __str__(self):
        for card in self.cards:
            return card
        
    def __len__(self):
        return len(self.cards)

    def add_to_deck(self, card):
        self.cards.append(card)

    def peek(self):
        if self.cards:
            return self.cards[-1]
        else:
            raise IndexError('Cannot peek empty deck')