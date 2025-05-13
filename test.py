import pytest
from cards import Card
from deck import Deck
from player import Player

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
    
    def test_add_to_deck(self):
        # tests functionality to add a card
        deck = Deck()
        card = Card('Hearts', '8')
        deck.add_to_deck(card)

        assert len(deck) == 1
        assert deck.cards[0] == card

    def test_peek_deck(self):
        # tests peek functionarlity of deck
        deck = Deck()
        card = Card("Diamonds", "Jack")

        deck.add_to_deck(card)

        assert deck.peek() == card

    def test_peek_empty_deck(self):
        # ensures Error is raised when deck is empty
        deck = Deck()

        with pytest.raises(IndexError):
            deck.peek()
    
    def test_initalize_deck(self):
        # ensures the length of deck is in line with request amount of decks
        # could/should lowkey flesh this out more
        deck = Deck()
        deck.initialize_deck(1)

        assert len(deck) == 52
        
    def test_shuffle_deck(self):
        # tests shuffling of the deck by comparing two deck objects against each other
        deck1 = Deck()
        deck2 = Deck()

        deck1.initialize_deck()
        deck2.initialize_deck()

        assert deck1 == deck2
        deck2.shuffle_deck()
        assert deck1 != deck2


class TestPlayer:
    
    def test_init(self):
        player = Player('patty')

        assert player.name == 'patty'
        assert player.balance == 500
        assert player.hand == []

    def test_bet(self):
        player = Player('patty')

        p_bet = player.bet(50)

        assert p_bet == 50 
        assert player.balance == 500 - p_bet

    def test_bet_edge(self):
        player = Player('patty')

        with pytest.raises(ValueError):
            player.bet(501)

    def test_fold(self):
        # this seems so cursed for no reason
        player = Player('patty')

        card1 = Card('Diamonds', 'Jack')
        card2 = Card('Clubs', '4')
        player.hand = [card1, card2]

        player.fold()

        assert player.hand == []

    # this one feels ridiculous
    """
    def test_check(self):
        # ???? 
        pass
    """

    def test_call(self):
        # again this just feels like a repeat of the bet function
        player = Player('patty')

        p_bet = player.call(50)

        assert p_bet == 50 
        assert player.balance == 500 - p_bet

    def test_raise(self):
        player = Player('patty')

        p_bet = player.raise_bet(100, 100)

        assert p_bet == 200
        assert player.balance == 500 - p_bet


class TestGame:
    pass

