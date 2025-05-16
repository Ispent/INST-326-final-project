from cards import Card
import itertools
import random 

class Deck:
    """ 
    Creates a deck object that will hold a number of card objects during the game

    Args:
        cards: list object that will hold each card object
    """

    def __init__(self):
        self.cards = []
        self.suitList = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        self.valueList = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
        
    def __len__(self):
        return len(self.cards)
    
    def __eq__(self, other):
        if not isinstance(other, Deck):
            return NotImplemented
        
        return self.cards == other.cards

    def add_to_deck(self, card):
        """
        Adds provided card object into the Deck object in place

        Args:
            card(obj): card object to be appended onto self.cards 
        """

        self.cards.append(card)

    def peek(self):
        """
        Checks the top card in the deck and returns it, unless the deck is empty, which will raise an error
        
        returns:
            the topmost card of the deck (obj)
        
        raises:
            IndexError - given an empty deck
        """

        if self.cards:
            return self.cards[-1]
        else:
            raise IndexError('Cannot peek empty deck')
        
    def initialize_deck(self, deck_count=1):
        """Initialize the deck with the specified number of standard 52-card decks.
        
        Args:
            deck_count (int): Number of decks to use (must be positive)
            
        Raises:
            ValueError: If deck_count is less than 1
        """
        if not isinstance(deck_count, int) or deck_count < 1:
            raise ValueError("Deck count must be a positive integer")
            
        for suit, value in itertools.product(self.suitList, self.valueList):
            for i in range(0, deck_count):
                self.cards.append(Card(suit, value))
    
    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        """Remove and return the top card from the deck.
        
        Returns:
            Card: The top card from the deck
            
        Raises:
            IndexError: If the deck is empty
        """
        if not self.cards:
            raise IndexError("Cannot deal from an empty deck")
        return self.cards.pop()
