from cards import Card

class Deck:
    """ Creates a deck object that will hold a number of card objects during the game

    Args:
        cards: list object that will hold each card object
    """

    def __init__(self):
        self.cards = []