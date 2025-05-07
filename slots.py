import random
import time

class SlotMachine:
    """
    """
    def __init__(self, starting_points):
        self.symbols = ['🍒', '🍋', '🔔', '💎', '🍀']
        self.points = starting_points
        self.spin_cost = 10
        

    def spin_reels(self):
        self.spin = [random.choice(self.symbols) for _ in range(3)]
        return self.spin

    def results(self, spins):
        if spins[0] == spins[1 == spins[3]]:
            self.points += 100
            return "🎉 JACKPOT! +100 points"
        elif spins[0] == spins[1] or spins[2] or spins[0] == spins[2]:
            self.points += 20
            return "Two matching symbols! +20 points"
        else:
            return "No match. Try again!"