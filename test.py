import pytest
from cards import Card
from deck import Deck
from player import Player
from poker import PokerGame
from handEval import HandEvaluator

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


class TestPoker:
    def test_initialize_round(self):
        """Test round initialization."""
        poker_game = PokerGame(Player("test_player"))
        poker_game.initialize_round()
        assert poker_game.pot == poker_game.SMALL_BLIND + poker_game.BIG_BLIND
        assert len(poker_game.community_cards) == 0
        
    def test_get_min_raise(self):
        """Test minimum raise amounts for different stages."""
        poker_game = PokerGame(Player("test_player"))
        
        # Pre-flop
        poker_game.current_stage = 'pre-flop'
        assert poker_game.get_min_raise() == poker_game.SMALL_BLIND
        
        # Flop
        poker_game.current_stage = 'flop'
        assert poker_game.get_min_raise() == poker_game.SMALL_BLIND
        
        # Turn
        poker_game.current_stage = 'turn'
        assert poker_game.get_min_raise() == poker_game.BIG_BLIND
        
        # River
        poker_game.current_stage = 'river'
        assert poker_game.get_min_raise() == poker_game.BIG_BLIND
        
    def test_is_raise_valid(self):
        """Test raise validation."""
        poker_game = PokerGame(Player("test_player"))
        
        # Test valid raise
        poker_game.current_stage = 'pre-flop'
        is_valid, _ = poker_game.is_raise_valid(2)
        assert is_valid is True
        
        # Test invalid raise (not multiple of min raise)
        is_valid, msg = poker_game.is_raise_valid(3)
        assert is_valid is False
        assert "multiple" in msg
        
        # Test max raises limit
        poker_game.raises_this_round = poker_game.MAX_RAISES
        is_valid, msg = poker_game.is_raise_valid(2)
        assert is_valid is False
        assert "Maximum number of raises" in msg
        
    def test_initial_deal(self):
        """Test initial card dealing."""
        poker_game = PokerGame(Player("test_player"))
        poker_game.inital_deal()
        assert len(poker_game.player.hand) == 2
        assert len(poker_game.other_player.hand) == 2
        
    def test_assign_blinds(self):
        """Test blind rotation."""
        poker_game = PokerGame(Player("test_player"))
        initial_player_blind = poker_game.player.blind
        initial_dealer_blind = poker_game.other_player.blind
        
        poker_game.assign_blinds()
        assert poker_game.player.blind != initial_player_blind
        assert poker_game.other_player.blind != initial_dealer_blind
        
        # Test second rotation returns to original positions
        poker_game.assign_blinds()
        assert poker_game.player.blind == initial_player_blind
        assert poker_game.other_player.blind == initial_dealer_blind


class TestHandEvaluator:
    def test_royal_flush(self):
        """Test royal flush detection."""
        evaluator = HandEvaluator()
        royal_flush = [
            Card('Hearts', 'Ace'),
            Card('Hearts', 'King'),
            Card('Hearts', 'Queen'),
            Card('Hearts', 'Jack'),
            Card('Hearts', '10')
        ]
        rank = evaluator.check_hand(royal_flush)
        assert rank == evaluator.HAND_RANKS['ROYAL_FLUSH'][0]
        
    def test_straight_flush(self):
        """Test straight flush detection."""
        evaluator = HandEvaluator()
        straight_flush = [
            Card('Clubs', '9'),
            Card('Clubs', '8'),
            Card('Clubs', '7'),
            Card('Clubs', '6'),
            Card('Clubs', '5')
        ]
        rank = evaluator.check_hand(straight_flush)
        assert rank == evaluator.HAND_RANKS['STRAIGHT_FLUSH'][0]
        
    def test_four_of_kind(self):
        """Test four of a kind detection."""
        evaluator = HandEvaluator()
        four_kind = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'King'),
            Card('Clubs', 'King'),
            Card('Spades', 'King'),
            Card('Hearts', '2')
        ]
        rank = evaluator.check_hand(four_kind)
        assert rank == evaluator.HAND_RANKS['FOUR_KIND'][0]
        
    def test_full_house(self):
        """Test full house detection."""
        evaluator = HandEvaluator()
        full_house = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'King'),
            Card('Clubs', 'King'),
            Card('Spades', '2'),
            Card('Hearts', '2')
        ]
        rank = evaluator.check_hand(full_house)
        assert rank == evaluator.HAND_RANKS['FULL_HOUSE'][0]
        
    def test_flush(self):
        """Test flush detection."""
        evaluator = HandEvaluator()
        flush = [
            Card('Hearts', '2'),
            Card('Hearts', '5'),
            Card('Hearts', '7'),
            Card('Hearts', '9'),
            Card('Hearts', 'Jack')
        ]
        rank = evaluator.check_hand(flush)
        assert rank == evaluator.HAND_RANKS['FLUSH'][0]
        
    def test_straight(self):
        """Test straight detection."""
        evaluator = HandEvaluator()
        straight = [
            Card('Hearts', '5'),
            Card('Clubs', '6'),
            Card('Diamonds', '7'),
            Card('Spades', '8'),
            Card('Hearts', '9')
        ]
        rank = evaluator.check_hand(straight)
        assert rank == evaluator.HAND_RANKS['STRAIGHT'][0]
        
    def test_three_of_kind(self):
        """Test three of a kind detection."""
        evaluator = HandEvaluator()
        three_kind = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'King'),
            Card('Clubs', 'King'),
            Card('Spades', '2'),
            Card('Hearts', '3')
        ]
        rank = evaluator.check_hand(three_kind)
        assert rank == evaluator.HAND_RANKS['THREE_KIND'][0]
        
    def test_two_pair(self):
        """Test two pair detection."""
        evaluator = HandEvaluator()
        two_pair = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'King'),
            Card('Clubs', '2'),
            Card('Spades', '2'),
            Card('Hearts', '3')
        ]
        rank = evaluator.check_hand(two_pair)
        assert rank == evaluator.HAND_RANKS['TWO_PAIR'][0]
        
    def test_one_pair(self):
        """Test one pair detection."""
        evaluator = HandEvaluator()
        one_pair = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'King'),
            Card('Clubs', '2'),
            Card('Spades', '3'),
            Card('Hearts', '4')
        ]
        rank = evaluator.check_hand(one_pair)
        assert rank == evaluator.HAND_RANKS['PAIR'][0]
        
    def test_high_card(self):
        """Test high card detection."""
        evaluator = HandEvaluator()
        high_card = [
            Card('Hearts', 'King'),
            Card('Diamonds', '2'),
            Card('Clubs', '4'),
            Card('Spades', '6'),
            Card('Hearts', '8')
        ]
        rank = evaluator.check_hand(high_card)
        assert rank == evaluator.HAND_RANKS['HIGH_CARD'][0]
        
    def test_ace_low_straight(self):
        """Test ace-low straight detection."""
        evaluator = HandEvaluator()
        ace_low = [
            Card('Hearts', 'Ace'),
            Card('Diamonds', '2'),
            Card('Clubs', '3'),
            Card('Spades', '4'),
            Card('Hearts', '5')
        ]
        assert evaluator.straight_check(ace_low) is True
        
    def test_compare_high_cards(self):
        """Test high card comparison."""
        evaluator = HandEvaluator()
        higher = [
            Card('Hearts', 'Ace'),
            Card('Diamonds', 'King'),
            Card('Clubs', 'Queen'),
            Card('Spades', 'Jack'),
            Card('Hearts', '10')
        ]
        lower = [
            Card('Hearts', 'King'),
            Card('Diamonds', 'Queen'),
            Card('Clubs', 'Jack'),
            Card('Spades', '10'),
            Card('Hearts', '9')
        ]
        assert evaluator._compare_high_cards(higher, lower) is True
        assert evaluator._compare_high_cards(lower, higher) is False


class TestPokerPlayer:
    """Test poker-specific player functionality."""
    
    def test_raise_bet(self):
        player = Player('test')
        initial_balance = player.balance
        current_bet = 50
        raise_amount = 50
        
        bet_made = player.raise_bet(current_bet, raise_amount)
        assert bet_made == current_bet + raise_amount
        assert player.balance == initial_balance - bet_made
        
    def test_raise_bet_insufficient_funds(self):
        player = Player('test')
        with pytest.raises(ValueError):
            player.raise_bet(player.balance, 100)  # Try to raise more than balance
            
    def test_win_pot(self):
        player = Player('test')
        initial_balance = player.balance
        pot_amount = 200
        
        player.win_pot(pot_amount)
        assert player.balance == initial_balance + pot_amount

