"""
essentially

receive a combo of 7 cards
    user itertools to split up 7 cards into a list of all possivle 5 card combos

    from there
        count all the unique values of cards - returns dictionary of value combos
            checks for
                pair
                two pair
                three of a kind
                four of a kind
                full house
            
        count all the unique suits of all cards - returns dictionary of combination of suits 
            checks for flush

functions

evalute
    loop throgh each combo
    check hand
    keep track of best hand

value counts
    collect values

suit counts
    colect suits

straight check
    checks if straight exists

flush check
    checks if flush exists

chcek hand
    based off the data from the above functions, will evalaute out hands to their respective ranks

    royal flush - needs flush, straight and highest card is ace
    straight flush - needs flush ad straight
    4 of kind - value counts
    full house - value counts
    flush - flush check
    straight - value checks in sequecne
    3 of kind - value counts
    2 paur - value counts
    pair - value counts
    high card - highest value



"""
from itertools import combinations


class HandEvaluator:
    HAND_RANKS = {
        'HIGH_CARD': (1, "High Card"),
        'PAIR': (2, "One Pair"),
        'TWO_PAIR': (3, "Two Pair"),
        'THREE_KIND': (4, "Three of a Kind"),
        'STRAIGHT': (5, "Straight"),
        'FLUSH': (6, "Flush"),
        'FULL_HOUSE': (7, "Full House"),
        'FOUR_KIND': (8, "Four of a Kind"),
        'STRAIGHT_FLUSH': (9, "Straight Flush"),
        'ROYAL_FLUSH': (10, "Royal Flush")
    }

    VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14 
    }

    def __init__(self):
        """Initialize the HandEvaluator without cards. Cards will be provided to evaluate method."""
        self.best_hand = None

    def evaluate(self, cards):
        """
        Evaluate all possible 5-card combinations from the given cards
        and return the rank of the best hand.
        
        Args:
            cards (list): A list of 7 Card objects
            
        Returns:
            int: The rank of the best possible hand
        """
        best_rank = self.HAND_RANKS["HIGH_CARD"][0]  # Start with lowest possible rank (just the number)
        
        # Generate 5-card combinations if more than 5 cards provided
        if len(cards) > 5:
            hands = combinations(cards, 5)
        else:
            hands = [cards]  # Just use the 5 cards as is
            
        # Find best possible hand
        for hand in hands:
            rank = self.check_hand(list(hand))
            best_rank = max(best_rank, rank)  # Higher rank number is better
            
        return best_rank

    def value_counts(self, hand):
        counts = {}
        for card in hand:
            counts[card.value] = counts.get(card.value, 0) + 1
        return counts

    def suit_counts(self, hand):
        counts = {}
        for card in hand:
            counts[card.suit] = counts.get(card.suit, 0) + 1
        return counts

    def straight_check(self, hand):
        values = sorted([self.VALUES[card.value] for card in hand])

        if values == [2, 3, 4, 5, 14]:
            return True
        
        return values == list(range(values[0], values[0] + 5))
    
    def flush_check(self, hand):
        return len(set(card.suit for card in hand)) == 1

    def check_hand(self, hand):
        values = [self.VALUES[card.value] for card in hand]  # Convert to numeric values
        value_counts = self.value_counts(hand)
        is_flush = self.flush_check(hand)
        is_straight = self.straight_check(hand)
        
        # Royal Flush
        if is_straight and is_flush and max(values) == 14:
            return self.HAND_RANKS["ROYAL_FLUSH"][0]
            
        # Straight Flush
        if is_straight and is_flush:
            return self.HAND_RANKS["STRAIGHT_FLUSH"][0]
            
        # Four of a Kind
        if 4 in value_counts.values():
            return self.HAND_RANKS["FOUR_KIND"][0]
            
        # Full House
        if 3 in value_counts.values() and 2 in value_counts.values():
            return self.HAND_RANKS["FULL_HOUSE"][0]
            
        # Flush
        if is_flush:
            return self.HAND_RANKS["FLUSH"][0]
            
        # Straight
        if is_straight:
            return self.HAND_RANKS["STRAIGHT"][0]
            
        # Three of a Kind
        if 3 in value_counts.values():
            return self.HAND_RANKS["THREE_KIND"][0]
            
        # Two Pair
        if list(value_counts.values()).count(2) == 2:
            return self.HAND_RANKS["TWO_PAIR"][0]
            
        # One Pair
        if 2 in value_counts.values():
            return self.HAND_RANKS["PAIR"][0]
            
        # High Card
        return self.HAND_RANKS["HIGH_CARD"][0]

    @classmethod
    def get_hand_name(cls, rank):
        """Convert numeric rank to readable name."""
        for hand_type, (value, name) in cls.HAND_RANKS.items():
            if value == rank:
                return name
        return "Unknown"


