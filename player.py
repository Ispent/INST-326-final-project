
class Player:
    def __init__(self, name, blind='small'):
        # i guess 500 bucks is enough to start off with
        self.name = name
        self.balance = 500
        self.hand = []
        self.blind = blind
        self.current_bet = 0

    def __repr__(self):
        return (f"{'player name:':<15} {self.name:}\n" 
                f"{'player balance:':<15} ${self.balance:.2f}\n")


    def bet(self, amount):
        if self.balance < amount:
            raise ValueError('too broke')
        
        self.balance -= amount
        self.current_bet += amount
        return amount
    
    def fold(self):
        self.hand = []
        self.current_bet = 0
        return 'fold'

    def check(self):
        # i dont think i even need this ??
        return 'check'
    
    def call(self, amount_to_call):
        return self.bet(amount_to_call)
    
    def raise_bet(self, current_bet, raise_amount):
        new_bet = current_bet + raise_amount
        if self.balance < new_bet - self.current_bet:
            raise ValueError('broke')
        
        return self.bet(new_bet - self.current_bet)



    
    
    

        
