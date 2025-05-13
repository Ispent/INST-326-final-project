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


def initialize_player():
    while True:
        # this lowkey seems more annoying than useful but whatever
        name = input("Enter name of player: ")

        if (input(f'Are you sure you want to be named {name}? (y/n): ')).lower() == 'y':
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
    
    def round(self):
        pass

    def initialize_round(self):
        self.deck.initialize_deck()
        self.deck.shuffle_deck()
        self.assign_blinds()
        self.pot = 0
        self.community_cards = []

        # post up da blinds
        small_blind = 2
        big_blind = 4
        if self.player.blind == 'small':
            self.player.bet(small_blind)
            self.other_player.bet(big_blind)
            self.pot += small_blind + big_blind
        else:
            self.player.bet(big_blind)
            self.other_player.bet(small_blind)
            self.pot += small_blind + big_blind



    def assign_blinds(self):
        if self.player.blind == 'small':
            self.player.blind = 'big'
            self.other_player.blind = 'small'
        else:
            self.player.blind = 'small'
            self.other_player.blind = 'big'

    def inital_deal(self):
        self.player.hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.other_player.hand = [self.deck.deal_card(), self.deck.deal_card()]
    

    def bet_round(self):
        highest_bet = 0
        self.player.current_bet = 0
        self.other_player.current_bet = 0

        if self.player.blind == 'small':
            turn_order = [self.player, self.other_player]
        else:
            turn_order = [self.other_player, self.player]
        
        while True:
            for player in turn_order:
                if player == self.player:
                    print(f"Pot: ${self.pot}"
                        f"Your hand: {self.player.hand}"
                        f"Community Cards: {self.community_cards}"
                        f"Current bet to match ${highest_bet}")
                    
                    action = input('what would you like to do (fold/call/check/raise)').lower()

                    if action == 'fold':
                        print('You have folded, dealer wins')
                        return self.player.fold()
                    
                    elif action == 'check':
                        if highest_bet > 0:
                            print(f'You cannot check, you must match the current bet of {highest_bet}')
                        else:
                            print('You check')
                            return self.player.check()
                    
                    elif action == 'call':
                        call_amount = highest_bet - self.player.current_bet
                        self.player.balance -= call_amount
                        self.player.current_bet += call_amount
                        self.pot += call_amount
                        print(f'you called ${call_amount}')

                    elif action == 'raise':
                        raise_amount = int(input('Enter raise amount: '))

                        total_bet = highest_bet + raise_amount
                        self.player.balance -= total_bet - self.player.current_bet
                        self.player.current_bet = total_bet
                        self.pot += total_bet - highest_bet
                        highest_bet = total_bet

                        print(f'You raised to ${total_bet}')
                    
                    else:
                        print('Invalid action. Please choose fold, call, check, or raise.')
                        continue
                else:
                    action, new_bet = self.dealer_ai(highest_bet)
                    if action == 'fold':
                        return
                    if action == 'raise':
                        highest_bet = new_bet

            if (self.player.current_bet == self.other_player.current_bet) and highest_bet > 0:
                print('end of betting')
                break


    def dealer_ai(self, highest_bet):
        # by default, the dealer will only fold if the current bet is too high to be reasonable
        min_raise = 2
        max_raise = min(self.other_player.balance, self.player.balance)
        call_amount = highest_bet - self.other_player.current_bet

        # folding logic, current bet needs to be less than half the dealer's balance
        if call_amount > self.other_player.balance // 2:
            print('dealer folds, you win')
            self.other_player.fold()
            return 'fold', highest_bet
        
        # if fold check passes, the dealer wil raise their bet 30 percent of the time
        if call_amount >= min_raise and max_raise > min_raise and random.random() < 0.3:
            raise_amount = random.randint(min_raise, max_raise)
            total_bet = highest_bet + raise_amount

            self.other_player.raise_bet(highest_bet, raise_amount)
            self.pot += total_bet - highest_bet

            print(f'dealer raises to ${total_bet}')
            return 'raise', total_bet


        # if not raising or folding, will default to calling
        self.other_player.call(call_amount)
        self.pot += call_amount

        print(f'dealer calls ${call_amount}')
        return 'call', highest_bet
            

    
            
def main():
    player1 = initialize_player()
    pokergame = PokerGame(player1)
    print(pokergame.player)
    pokergame.bet_round()

    print(pokergame.pot)


main()

def hand_finder():
    test_list = [1, 2, 3, 4, 5, 6, 7]

    for reply in itertools.combinations(test_list, 5):
        print(reply)



