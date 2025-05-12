import random
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
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self.cards = []
        
    def fill(self, decks):
        for i in range(decks):
            for value in (self.values):
                self.cards.append(Card(value))
                
class Card:
    def __init__(self, value):
        
playerHand = []
dealerHand = []

#deals player and dealer hands
def dealCard(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)
    
#calculate total of player and dealer hands
def total(turn):
    total = 0
    face = ['J', 'Q', 'K']
    for card in turn:
        if card in range(1,11):
            total += card
        elif card in face:
            total +=10 
        else:
            if total > 11:
                total += 1
            else:
                total += 11
    return total