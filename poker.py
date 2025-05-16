"""
how do i even start this

notes:
    - only requires 1 deck to play (optional multiple decks feature)
    
    - several different possible hands and needs to compare against each other
        - some kind of hierarchy needs to be in place for every hand
            - each hand needs to be comparable to itself as well

    - possible hands
        - royal flush - (A - K - Q - J - 10) - most value hand, needs to be same suit as well
        - straight flush - (6 - 7 - 8 - 9 - 10) - second highest, needs to be same suit in numerical order
        - four of a kind - (A - A - A - A - (any card)) - four cards of the same rank
        - full house - (A - A - A - K - K) - three cards of one rank with two cards of another rank
        - flush - (2 - 5 - 9 - 10 - 3) - five cards of the same suit, any order
        - straight - (2 - 3 - 4 - 5 - 6) - five cards of numerically increasing value, any suit
        - three of a kind - yk what this is
        - two pair
        - pair
        - high card 

    - tie logic
        - highest value combo of five cards within the seven available cards will win 
            - if the main hand occurs in a tie, kickers are utilized to break ties
            - highest value of unused cards
            - if everything fails and all cards are the valued the same, the pot will be split

    - turn logic
        - within a turn, the player will have the option to
            1. fold - forfeit the hand, give up essentially
            2. check - stand your hand without any bets made
                - only available if other player hasnt bet
            3. bet - first person to money in the pot in this round
            4. call - you match the current bet placed by other player
            5. raise - you increase the current bet, a fixed amount based off the blind

    - betting logic
        - planning on limit hold 'em poker

        1. blinds (reversed ????)
            - small blind - posted by dealer
            - big blind - posted by other player
        
        2. bet size
            - small bet - used in pre-flop and flop rounds
            - big bet - used on turn and river
            - ~ 2/4 or 3/6 structure
        
        3. per round
            - in each round, there is one bet, and upto three raises
        
            pre flop - occurs right after player receives the two cards
                - small bind bets first 
                - in small bet increment
                - available actions: fold, call, raise
            
            flop - first three community cards are shown
                - dealer now goes second 
                - bet size remains at $2 

            turn - when there is four cards present 
                - big bet is possible now 

            river - final card is now dealt
                - last chance to make a bet

            ::essentially
                - round 1/2 can raise by the amount of the small blind
                - round 3/4 can raise/bet by the big blind amount

    - so with this hwat do i even do ???
        - game order
            - 

        - code order
            - initialize deck
                - add appropriate amount of cards to deck

            - initalize player
                - crate player profile and dealer profile
                - assign blind object (?)
                    - create a blind object to keep track of bets (?) -- idk if neccesary
            
            - shuffle deck and deal cards
                - 2 each to player's hand
            
            - bet round
                - enfore blinds
                - player can either fold, call, raise, or check
            
            - repeat until all cards are shown of bet rounds

            - if at least 2 players remaining at the final round, reveal hands
                - compare the strength of cards
                    - compare card structure against like a regex (?) - or utilize a tuple - hell no wtf

            **- deck management
              - ensure after dealing a card to a player/dealer, the card object is properly removed from the top of the deck
                - add a remove top/deal function to deck
                - apparently u burn cards but idk when i have to look into that

        - money logic
            - ideally contain a "stack" of chips
            - each chip will hold a numerical value
            - can be bet/freely exchanged with the dealer for differnet chip valuations

            - but reallistically for now will just hold numerical values

            - side pots (?) for two player 

        - round progression
            - burn - flop ( draw - draw - draw) - bets - burn - turn ( draw ) - bet - burn - river ( draw ) - bet - final 

        - hand evaluation (?????)
            - actually how the fuck
           
"""
from deck import Deck
from cards import Card
from player import Player
import itertools
import random
from handEval import HandEvaluator

def initialize_player():
    while True:
        name = input("Enter name of player: ")
        if input(f'Are you sure you want to be named {name}? (y/n): ').lower() == 'y':
            return Player(name)

class PokerGame:
    def __init__(self, player):
        self.player = player
        self.other_player = Player('dealer', 'big')
        self.deck = Deck()
        self.deck.initialize_deck()
        self.deck.shuffle_deck()
        self.pot = 0
        self.community_cards = []
        # Add betting structure constants
        self.SMALL_BLIND = 2
        self.BIG_BLIND = 4
        self.current_stage = 'pre-flop'
        self.raises_this_round = 0
        self.MAX_RAISES = 3
        
    def get_min_raise(self):
        """Get minimum raise amount based on current stage."""
        if self.current_stage in ['pre-flop', 'flop']:
            return self.SMALL_BLIND
        else:  # turn or river
            return self.BIG_BLIND
            
    def is_raise_valid(self, raise_amount):
        """Check if raise amount is valid for current stage."""
        min_raise = self.get_min_raise()
        if self.raises_this_round >= self.MAX_RAISES:
            return False, f"Maximum number of raises ({self.MAX_RAISES}) reached for this round"
        if raise_amount % min_raise != 0:
            return False, f"Raise amount must be a multiple of ${min_raise}"
        return True, None
        
    def round(self):
        """Play a complete round of poker."""
        # Initialize round
        self.initialize_round()
        self.inital_deal()
        
        # Pre-flop betting
        self.current_stage = 'pre-flop'
        print("\n=== Pre-flop betting ===")
        if self.bet_round() == 'fold':
            return
            
        # Deal flop (3 cards)
        self.current_stage = 'flop'
        self.deck.deal_card()  # Burn card
        self.community_cards.extend([self.deck.deal_card() for _ in range(3)])
        print("\n=== Flop ===")
        if self.bet_round() == 'fold':
            return
            
        # Deal turn (1 card)
        self.current_stage = 'turn'
        self.deck.deal_card()  # Burn card
        self.community_cards.append(self.deck.deal_card())
        print("\n=== Turn ===")
        if self.bet_round() == 'fold':
            return
            
        # Deal river (1 card)
        self.current_stage = 'river'
        self.deck.deal_card()  # Burn card
        self.community_cards.append(self.deck.deal_card())
        print("\n=== River ===")
        if self.bet_round() == 'fold':
            return
            
        # Evaluate hands and determine winner
        self.evaluate_hands()

    def initialize_round(self):
        """Initialize a new round of poker."""
        self.deck = Deck()
        self.deck.initialize_deck()
        self.deck.shuffle_deck()
        self.assign_blinds()
        self.pot = 0
        self.community_cards = []
        
        # Reset bets from previous round
        self.player.reset_bet()
        self.other_player.reset_bet()

        # post up da blinds
        small_blind = 2
        big_blind = 4
        if self.player.blind == 'small':
            self.player.bet(small_blind)
            self.other_player.bet(big_blind)
        else:
            self.player.bet(big_blind)
            self.other_player.bet(small_blind)
        self.pot = small_blind + big_blind

    def assign_blinds(self):
        """Rotate blinds between players."""
        if self.player.blind == 'small':
            self.player.blind = 'big'
            self.other_player.blind = 'small'
        else:
            self.player.blind = 'small'
            self.other_player.blind = 'big'

    def inital_deal(self):
        """Deal two cards to each player."""
        self.player.hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.other_player.hand = [self.deck.deal_card(), self.deck.deal_card()]
    
    def bet_round(self):
        self.raises_this_round = 0
        highest_bet = max(self.player.current_bet, self.other_player.current_bet)
        players_acted = 0
        action_needed = True

        if self.player.blind == 'small':
            turn_order = [self.player, self.other_player]
        else:
            turn_order = [self.other_player, self.player]
        
        while action_needed:
            for player in turn_order:
                if player == self.player:
                    print(f"\nPot: ${self.pot}")
                    print(f"Your hand: {', '.join(str(card) for card in self.player.hand)}")
                    print(f"Community Cards: {', '.join(str(card) for card in self.community_cards)}")
                    print(f"Current bet to match: ${highest_bet}")
                    print(f"Your current bet: ${self.player.current_bet}")
                    print(f"\nCurrent stage: {self.current_stage}")
                    print(f"Minimum raise: ${self.get_min_raise()}")
                    print(f"Raises this round: {self.raises_this_round}/{self.MAX_RAISES}")
                    
                    action = input('\nWhat would you like to do (fold/call/check/raise)? ').lower()

                    if action == 'fold':
                        print('\nYou have folded, dealer wins')
                        self.other_player.win_pot(self.pot)
                        return 'fold'
                    
                    elif action == 'check':
                        if highest_bet > self.player.current_bet:
                            print(f'\nYou cannot check, you must match the current bet of ${highest_bet}')
                            continue
                        else:
                            print('You check')
                            players_acted += 1
                            
                    elif action == 'call':
                        call_amount = highest_bet - self.player.current_bet
                        if call_amount == 0:
                            print('You check')
                            players_acted += 1
                            continue
                        try:
                            self.player.call(call_amount)
                            self.pot += call_amount
                            print(f'You called ${call_amount}')
                            players_acted += 1
                        except ValueError:
                            print('\nNot enough balance to call.')
                            return self.player.fold()
                            
                    elif action == 'raise':
                        if self.raises_this_round >= self.MAX_RAISES:
                            print(f'\nMaximum number of raises ({self.MAX_RAISES}) reached for this round')
                            continue
                            
                        min_raise = self.get_min_raise()
                        while True:  # Keep trying until valid raise or different action
                            print(f'\nMinimum raise amount is ${min_raise}')
                            print(f'Your raise must be a multiple of ${min_raise}')
                            
                            try:
                                raise_amount = int(input('Enter raise amount (or 0 to cancel): '))
                                if raise_amount == 0:
                                    print('\nRaise cancelled. Choose another action.')
                                    break
                                    
                                is_valid, error_message = self.is_raise_valid(raise_amount)
                                if not is_valid:
                                    print(f'\n{error_message}')
                                    continue
                                    
                                total_bet = highest_bet + raise_amount
                                amount_to_add = self.player.raise_bet(highest_bet, raise_amount)
                                self.pot += amount_to_add
                                highest_bet = total_bet
                                print(f'You raised by ${raise_amount}')
                                players_acted = 1
                                self.raises_this_round += 1
                                break
                            except ValueError as e:
                                print('\nInvalid input or not enough balance.')
                                continue
                        if raise_amount == 0:  # If raise was cancelled, let player choose again
                            continue
                    
                    else:
                        print('\nInvalid action. Please choose fold, call, check, or raise.')
                        continue
                else:
                    action, new_bet = self.dealer_ai(highest_bet)
                    if action == 'fold':
                        self.player.win_pot(self.pot)
                        return 'fold'
                    elif action == 'raise':
                        highest_bet = new_bet
                        players_acted = 1
                        self.raises_this_round += 1
                    else:
                        players_acted += 1

            if players_acted >= 2:
                action_needed = False
                print('\nEnd of betting round')

    def dealer_ai(self, highest_bet):
        """AI logic for dealer's betting decisions."""
        # Calculate the amount needed to call
        call_amount = max(0, highest_bet - self.other_player.current_bet)
        
        # Get minimum raise for current stage
        min_raise = self.get_min_raise()
        
        # Folding logic - fold if call amount is too high relative to balance
        if call_amount > self.other_player.balance // 2:
            print('Dealer folds')
            self.other_player.fold()
            return 'fold', highest_bet
        
        # Simple raising logic - 30% chance to raise
        if random.random() < 0.3:
            try:
                amount_to_add = self.other_player.raise_bet(highest_bet, min_raise)
                self.pot += amount_to_add
                new_bet = highest_bet + min_raise
                print(f'Dealer raises by ${min_raise}')
                return 'raise', new_bet
            except ValueError:
                # If raise fails, fall through to call
                pass

        # Call or check
        if call_amount > 0:
            try:
                self.other_player.call(call_amount)
                self.pot += call_amount
                print(f'Dealer calls ${call_amount}')
            except ValueError:
                print('Dealer folds')
                self.other_player.fold()
                return 'fold', highest_bet
        else:
            print('Dealer checks')
            
        return 'call', highest_bet

    def evaluate_hands(self):
        """Evaluate both players' hands and determine the winner."""
        evaluator = HandEvaluator()
        
        # Combine hole cards with community cards for each player
        player_cards = self.player.hand + self.community_cards
        dealer_cards = self.other_player.hand + self.community_cards
        
        # Get the rank and best hand for each player
        player_rank, player_best_hand = evaluator.evaluate(player_cards, return_best_hand=True)
        dealer_rank, dealer_best_hand = evaluator.evaluate(dealer_cards, return_best_hand=True)
        
        # Display both hands
        print(f"\nYour hand: {', '.join(str(card) for card in self.player.hand)}")
        print(f"Dealer's hand: {', '.join(str(card) for card in self.other_player.hand)}")
        print(f"Community cards: {', '.join(str(card) for card in self.community_cards)}")
        print(f"\nYour best hand ({evaluator.get_hand_name(player_rank)}): {', '.join(str(card) for card in player_best_hand)}")
        print(f"Dealer's best hand ({evaluator.get_hand_name(dealer_rank)}): {', '.join(str(card) for card in dealer_best_hand)}\n")
        
        # Determine winner
        if player_rank > dealer_rank:
            print(f"{self.player.name} wins with {evaluator.get_hand_name(player_rank)}")
            self.player.win_pot(self.pot)
        elif dealer_rank > player_rank:
            print(f"Dealer wins with {evaluator.get_hand_name(dealer_rank)}")
            self.other_player.win_pot(self.pot)
        else:
            # Split pot on tie
            print("It's a tie! Splitting the pot")
            split = self.pot // 2
            self.player.win_pot(split)
            self.other_player.win_pot(split)
        
        self.pot = 0

def main():
    player1 = initialize_player()
    pokergame = PokerGame(player1)
    
    while True:
        print("\n=== New Round ===")
        print(f"Your balance: ${player1.balance}")
        pokergame.round()
        
        if input("\nPlay another round? (y/n): ").lower() != 'y':
            break
        
    print(f"\nGame Over! Final balance: ${player1.balance}")

if __name__ == "__main__":
    main()

