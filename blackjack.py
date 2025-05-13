import random
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

#deck of cards/ hands
class Deck: 
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
              "2", "3", "4", "5", "6", "7", "8", "9", "10", 
              "2", "3", "4", "5", "6", "7", "8", "9", "10", 
              "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "J", "Q", "K", "A", "J", "Q", "K", "A", "J", "Q", "K", "A", "J", "Q", "K", "A"]
    
    def __init__(self):
        self.cards = []
        
    def __len__(self):
        return len(self.cards)
        
    def fill(self, decks):
        for i in range(decks):
            for value in (self.values):
                self.cards.append(Card(value))
                
    def clear(self):
        self.cards = []
        
    def shuffle(self):
        random.shuffle(self.cards)

#pulls a card for hands                
class Card:
    def __init__(self, value):
        self.value = value 
        
    def __str__(self):
        return f"{self.value}"
    
    def score(self):
        if self.value in ["J", "Q", "K"]:
            return 10
        if self.value == "A":
            return 1
        else:
            return int(self.value)
        
#defines the players (user and dealer)        
class Player:
    def __init__(self):
        self.hand = []
        
    def getHand(self):
        print("Player's hand:\n")
        for card in self.hand:
            print(card)
            print("")
        print("")
        
    def resetHand(self):
        self.hand = []
    @property   
    def aces(self):
        return len([card for card in self.hand if card.value == "A"])
    @property
    def score(self):
        return sum([card.score for card in self.hand])
    @property
    def score_aces(self):
        for ace in range(self.aces):
            if self.score < 12:
                self.score += 10
        return self.score
        
    def bust(self):
        if self.score_aces > 21:
            return True
        return False       

#Initial bet for player
class Gambler(Player):
    def __init__(self,chips):
        super().__init__()
        self.chips = chips
    
    def bet(self):
        stake = input(f"Total chips: {self.chips}. Enter the total bet:")
        try:
            if int(stake) > self.chips:
                print("Your bet ammount is invalid")
                self.bet()
            else:
                self.chips -= int(stake)
                return int(stake)
        except ValueError:
            print ("Please enter a valid integer.")
            self.bet()
 
#Text for dealer hand           
class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []
        
    def show (self, all = False):
        print("The dealer has: \n")
        if all:
            for card in self.hand:
                print(card)
        else:
            print(self.hand[0])
            print("Face down card")
            
#deals player and dealer hands
class Blackjack:
    def __init__(self):
        self.players = []
        self.deck = []
        self.player_bet = 0
        self.player_turn = True
        
    def deal(self):
        if len(self.deck) < 104:
            print ("shuffling...")
            self.deck.clear()
            self.deck.fill(6)
            self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.hand.append(self.deck.cards.pop())
                
    def hit(self, player):
        player.hand.append(self.deck.cards.pop())
        if isinstance(player, Dealer):
            player.show(True)
        else:
            player.getHand()
        self.checkBust(player)
        print(f"Player total: {player.score_aces}")
        
    def player_choice(self, player):
        answer = input("Hit or Stand? (H/S):")
        if answer.lower() == "h":
            self.hit(player)
        if answer.lower() == "s":
            print(f"You choose to stand on {player.score_aces}")
        
    def checkBust(self, player):
        if player.bust():
            if(isinstance(player, Gambler)):
                print("Bust")
                self.players_turn = False
                self.playerlost()
            if(isinstance(player, Dealer)):
                print("Dealer bust")
    def playerlost(self):
        print("You Lose")
        
    def push(self, player):
        print(f"It is a push. You get your initial bet of {self.player_bet} back.")
        player.chips += self.player_bet
        
    def compare(self, player, dealer):
        if player.score_aces > dealer.score_aces:
            self.playerwon(player)
        elif player.score_aces == dealer.score_aces:
            self.push(player)
        else:
            self.playerlost(player)
            
    def reset(self):
        for player in self.players:
            player.reset()
        self.player_bet = 0
    
    def replay(self, player):
        again = None
        while again != "y" or again != "n":
            again = input ("Play again? Y/N:")
            if again.lower == "y":
                return True
            elif again.lower == "n":
                print(f"You walk away with {player.chips}.")
            else:
                print("Invalid input. Try again.")
                
    #initiates blackjack game
    def play(self):
        print("Welcome to Blackjack")
        self.deck = Deck()
        player = Gambler(500)
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill(6)
        self.deck.shuffle()
        running = True
        
        while running:
            if self.players[0].chips == 0:
                print("The casino took all your money. Get out.")
                break
        self.player_bet = player.bet()
        self.deal()
        dealer.show()
        player.getHand()
        while self.players_turn:
            self.player_choice(player)
        if not player.bust:
            dealer.show()
            while not self.players_turn:
                if dealer.score_aces < 17:
                   print("Dealer hit")
                   self.hit(dealer)
                elif dealer.score_aces >= 17 and not dealer.bust():
                    print(f"Dealer stands with {dealer.score_aces}")
                    break
                elif dealer.bust:
                    self.playerwon(player)
                    break
            if not dealer.bust:
                self.compare(player, dealer)
        again = self.replay()
        if not again:
            running = False
        self.players_turn = False
        self.reset()
        
def main():
    bj = Blackjack()
    bj.play()
    
if __name__ == "__main__":
    main()