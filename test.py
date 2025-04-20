import pytest
from cards import Card

class TestCard:

    def test_card_init(self):
        # tests the initialization of a card
        card = Card('Hearts', 'King')
        assert card.suit == 'Hearts'
        assert card.value == 'King'

    def test_card_value(self):
        # tests the get_value functions with numerical values
        card = Card('Clubs', '7')
        assert card.get_value() == 7

    def test_card_ace(self):
        # tests get_value function with the Ace
        card = Card('Hearts', 'Ace')
        assert card.get_value() == 11

    def test_card_string(self):
        # tests the string representation of cards
        card = Card('Diamonds', '2')
        assert str(card) == '2 of Diamonds'

class TestDeck:
    
    def test_addToDeck(self):
        pass


