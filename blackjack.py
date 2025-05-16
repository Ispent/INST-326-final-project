import random
import sys
import itertools
"""
notes for order of game:

1. Dealing order goes as follows:
    -Player gets first card
    -Dealer gets second card with value showing
    -Player gets third card
    -Dealer gets forth card without value showing
2. Values added for player
    -if dealer is showing ace, check for blackjack and if it is the hand ends if player doesn't also have blackjack.

3. Player has options: Stand, Hit, Double, or Split if applicable
    - on stand game continues to dealers show
   
    -With hit a third card to players hand is added
        -if total is over 21 player busts
        -player can hit as many times as possible until total is over or at 21
   
    -Double allows player to double bet but only one card is added to total
   
    -Split is available if given two cards of the same value
        -two hands are essentially given to player
        -initial bet is added to the second hand
        -one card is added to each split card
        -player is able to then play each hand as normal
4. Dealer turn to show total
    -Dealer stands on totals 17-21
    -if under 17, dealer hits and stand rules apply
    
5. Determine winner
    -compare totals and says whether player or dealer wins
    -also calculates total won by player if they win"""

#deck of cards for the hands
import random

class Deck: 
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
            "J", "Q", "K", "A"] * 4
    
    def __init__(self):
        self.cards = []
        
    def __len__(self):
        return len(self.cards)
        
    def fill(self, decks):
        for _ in range(decks):
            for value in Deck.values:
                self.cards.append(Card(value))
                
    def clear(self):
        self.cards = []
        
    def shuffle(self):
        random.shuffle(self.cards)

# Pulls a card for hands                
class Card:
    def __init__(self, value):
        self.value = value 
        
    def __str__(self):
        return f"{self.value}"
    
    def score(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 11
        else:
            return int(self.value)
        
# Defines the players (user and dealer)        
class Player:
    def __init__(self):
        self.hand = []
        self.split_hands = []
        self.current_hand = 0
    
    # Stores split hand if possible and contains index of hands being played     
    def getHand(self, hand_index=0):
        if hand_index == 0 or (hand_index > 0 and len(self.split_hands) >= hand_index):
            hand = self.hand if hand_index == 0 else self.split_hands[hand_index - 1]
            hand_label = "Player's hand:" if hand_index == 0 else f"Player's split hand {hand_index}"
            print(hand_label)
            for card in hand:  # Fixed: was printing self.hand instead of hand
                print(card)
            print(f"Total: {self.calculate_score(hand)}")
            print()
        
    def resetHand(self):
        self.hand = []
        self.split_hands = []
        self.current_hand = 0
       
    def aces(self):
        return len([card for card in self.hand if card.value == "A"])
    
    def calculate_score(self, hand):
        total = sum(card.score() for card in hand)  # Fixed: was using self.hand instead of hand
        aces = sum(1 for card in hand if card.value == "A")
        # Adjust aces from 11 to 1 if total is over 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
    
    def score(self):
        return self.calculate_score(self.hand)
    
    def all_hands(self):
        return [self.hand] + self.split_hands
     
    def bust(self, hand_index=0):
        hand = self.hand if hand_index == 0 else self.split_hands[hand_index - 1]
        return self.calculate_score(hand) > 21  # Fixed: was missing hand parameter

# Initial bet for player
class Gambler(Player):
    def __init__(self, chips, name):
        super().__init__()
        self.chips = chips
        self.name = name
    
    def bet(self):
        while True:
            stake = input(f"Total: ${self.chips}. Enter the total bet: ")
            try:
                stake = int(stake)
                if stake > self.chips:
                    print("Bet exceeds total.")
                else:
                    self.chips -= stake
                    return stake
            except ValueError:
                print("Enter a number.")
 
# Text for dealer hand           
class Dealer(Player):
    def show(self, all=False):
        print("The dealer has: ")
        if all:
            for card in self.hand:
                print(card)
            print(f"Total: {self.score()}")
        else:
            print(self.hand[0])
            print("Face down card")
        print()
            
# Deals player and dealer hands
class Blackjack:
    def __init__(self, player):
        self.players = [player, Dealer()]
        self.deck = Deck()
        self.player_bet = 0
        self.players_turn = True
        self.split_bets = []  # Initialize split_bets
        
    def deal(self):
        if len(self.deck) < 52:
            print("Shuffling...")
            self.deck.fill(6)
            self.deck.shuffle()
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.cards.pop())
                
    def hit(self, player, hand_index=0):
        if hand_index == 0:
            player.hand.append(self.deck.cards.pop())
        else:
            player.split_hands[hand_index-1].append(self.deck.cards.pop())
    
        if isinstance(player, Dealer):
            player.show(True)
        else:
            player.getHand(hand_index)
        if player.bust(hand_index):
            self.handle_bust(player, hand_index)
        print(f"Total: {player.calculate_score(player.hand if hand_index == 0 else player.split_hands[hand_index-1])}")
   
    # Criterion for player options   
    def player_choice(self, player, hand_index=0):
        hand = player.hand if hand_index == 0 else player.split_hands[hand_index - 1]
        while True:
            options = ["H: Hit", "S: Stand"]
            can_double = len(hand) == 2 and player.chips >= (self.player_bet if hand_index == 0 else self.split_bets[hand_index-1])
            
            can_split = (len(hand) == 2 and 
                        hand[0].value == hand[1].value and 
                        player.chips >= (self.player_bet if hand_index == 0 else self.split_bets[hand_index - 1]) and 
                        len(player.split_hands) < 3)
            
            if can_double:
                options.append("D: Double")
            if can_split:
                options.append("P: Split")
                
            player.getHand(hand_index)
            
            choice = input(f"{', '.join(options)}: ").lower()
            if choice == 'h':
                self.hit(player, hand_index)
                if player.bust(hand_index):
                    break
            elif choice == 's':
                print(f"Stand at {player.calculate_score(hand)}")
                if hand_index < len(player.split_hands):
                    player.current_hand = hand_index + 1
                    self.player_choice(player, hand_index + 1)
                else:
                    self.players_turn = False
                break
            elif choice == 'd' and can_double:
                bet = self.player_bet if hand_index == 0 else self.split_bets[hand_index - 1]
                player.chips -= bet
                if hand_index == 0:
                    self.player_bet *= 2
                else:
                    self.split_bets[hand_index - 1] *= 2
                self.hit(player, hand_index)
                
                if hand_index < len(player.split_hands):
                    player.current_hand = hand_index + 1
                    self.player_choice(player, hand_index + 1)
                else:
                    self.players_turn = False
                break
            elif choice == 'p' and can_split:
                self.split_hand(player, hand_index)
                break
            else:
                print("Invalid choice.")
    
    # Splits players hand and gives them two hands and bets 
    def split_hand(self, player, hand_index=0):
        bet = self.player_bet if hand_index == 0 else self.split_bets[hand_index-1]
        player.chips -= bet
        self.split_bets.append(bet)
    
        if hand_index == 0:
            split_card = player.hand.pop()
            player.split_hands.append([split_card])
            player.hand.append(self.deck.cards.pop())
            player.split_hands[0].append(self.deck.cards.pop())
        else:
            split_card = player.split_hands[hand_index-1].pop()
            player.split_hands.insert(hand_index, [split_card])
            player.split_hands[hand_index-1].append(self.deck.cards.pop())
            player.split_hands[hand_index].append(self.deck.cards.pop())
    
        print("Hand split. Now playing hand 1 and hand 2.")
        player.getHand(0)
        player.getHand(1)

    # Player gets 2:1 payout on dealer bust     
    def handle_bust(self, player, hand_index=0):
        if isinstance(player, Gambler):
            if hand_index == 0 and not player.split_hands:
                print("Bust! You lose.")
                self.players_turn = False
            else:
                print(f"Hand {hand_index + 1} busts!")
                if hand_index < len(player.split_hands):
                    player.current_hand = hand_index + 1
                    self.player_choice(player, hand_index + 1)
                else:
                    self.players_turn = False
        else:
            print("Dealer busts! You win.")
            self.players[0].chips += 2 * (self.player_bet + sum(self.split_bets))
        
    def push(self, player):
        print(f"It is a push. You get your initial bet of {self.player_bet} back.")
        player.chips += self.player_bet
        
    def compare(self):
        dealer = self.players[1]
        player = self.players[0]
        
        if dealer.bust():
            print("Dealer busts. You Win!")
            total_bet = self.player_bet + sum(self.split_bets)
            player.chips += 2 * total_bet
            return
        dealer_score = dealer.score()
        print(f"Dealer's total: {dealer_score}")
        
        player_score = player.calculate_score(player.hand)
        bet = self.player_bet
        self._compare_hand_result(player_score, dealer_score, bet, "Hand 1")
            
        for i, hand in enumerate(player.split_hands, 1):
            if len(hand) > 0:
                player_score = player.calculate_score(hand)
                bet = self.split_bets[i-1]
                self._compare_hand_result(player_score, dealer_score, bet, f"Hand {i+1}")
         
    def _compare_hand_result(self, player_score, dealer_score, bet, hand_name):
        if player_score > 21:
            print(f"{hand_name} busted - lose ${bet}")
        elif player_score == dealer_score:
            print(f"{hand_name} pushes - bet ${bet} returned")
            self.players[0].chips += bet
        elif player_score > dealer_score:
            print(f"{hand_name} wins! - win ${bet}")
            self.players[0].chips += 2 * bet
        else:
            print(f"{hand_name} loses - lose ${bet}")
    
    def reset(self):
        for player in self.players:
            player.resetHand()
        self.player_bet = 0
        self.split_bets = []
    
    def replay(self, player):
        again = None
        while again != "y" and again != "n":  # Fixed: changed 'or' to 'and'
            again = input("Play again? Y/N: ").lower()
            if again == "y":
                return True
            elif again == "n":
                print(f"You walk away with {player.chips}.")
                return False
            else:
                print("Invalid input. Try again.")
                
    # Initiates blackjack game
    def play(self):
        player = self.players[0] #gambler
        dealer = self.players[1]

        print(f"Hi {player.name}! Welcome to Blackjack.")
        self.deck.fill(6)
        self.deck.shuffle()
        
        while True:
            if player.chips <= 0:
                print("Out of chips.")
                break
                
            player.resetHand()
            dealer.resetHand()
            self.split_bets = []
            self.player_bet = player.bet()
            
            self.deal()

            player_blackjack = player.score() == 21 and len(player.hand) == 2
            dealer_blackjack = dealer.score() == 21 and len(dealer.hand) == 2
            
            if player_blackjack:
                dealer.show(all=True)
                if dealer_blackjack:
                    print("Both have blackjack! Push.")
                    player.chips += self.player_bet
                else:
                    print("Blackjack! You win 3:2 payout!")
                    payout = self.player_bet + (self.player_bet * 3 // 2)
                    player.chips += payout
                
                if len(self.deck) < 52:
                    self.deck.clear()
                    self.deck.fill(6)
                    self.deck.shuffle()
                    
                again = input("Play again? (y/n): ").lower()
                if again != 'y':
                    print(f"Exit with {player.chips} chips.")
                else:
                    continue
            dealer.show()
            player.getHand()
            self.players_turn = True
            
            # Player turn
            while self.players_turn:
                self.player_choice(player)
            
            # Dealer turn
            if not all(player.bust(i) for i in range(len(player.all_hands()))):
                dealer.show(all=True)
                while dealer.score() < 17:
                    print("Dealer hits.")
                    self.hit(dealer)
                self.compare()
            
            if len(self.deck) < 52:
                self.deck.clear()
                self.deck.fill(6)
                self.deck.shuffle()
            
            if not self.replay(player):
                print(f"Exit with ${player.chips}.")
                break

def main():
    player = Gambler(500, "test")
    player.name = 'test'
    game = Blackjack(player)
    game.play()
    
if __name__ == "__main__":
    main()
    