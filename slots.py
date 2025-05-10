import random
import time

class SlotMachine:
    """
    """
    def __init__(self, starting_points):
        self.symbols = ['🍒', '🍋', '🔔', '💎', '🍀']
        self.symbol_value = {
            '🍒' : 20,
            '🍋' : 10,
            '🔔' : 30, 
            '💎' : 50, 
            '🍀' : 25
            }
        self.points = starting_points
        self.spin_cost = 10 #can change but for now

    def spin_reels(self):
        self.points -= self.spin_cost
        print(f"You now have {self.points} points.")
        time.sleep(2)
        
        print("Spinning...")
        time.sleep(3)
        
        self.spin = [random.choice(self.symbols) for _ in range(3)]
        return self.spin

    def results(self, spins):
        if spins[0] == spins[1] == spins[2]:
            reward = self.symbol_value[spins[0]] * 3
            self.points += reward
            return f"🎉 JACKPOT! +{reward} points"
        
        elif spins[0] == spins[1]:
            symbol = spins[0]
            
        elif spins[0] == spins [2]:
            symbol = spins[0]
        elif spins[1] == spins [2]:
            symbol = spins[1]
        else:
            return "No match. Try again!"
        
        reward = self.symbol_value[symbol] * 2
        self.points += reward
        return f"Two matching symbols! +{reward} points"
            
        
        