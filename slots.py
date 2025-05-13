import random
import time
import sys

class SlotMachine:
    """
    """
    def __init__(self, starting_points): #will replace starting points with player
        self.symbols = ['🍒', '🍋', '🔔', '💎', '🍀']
        self.symbol_value = {
            '🍒' : 20,
            '🍋' : 10,
            '🔔' : 30, 
            '💎' : 50, 
            '🍀' : 25
            }
        #self.player = player
        self.points = starting_points
        self.spin_cost = 10 #can change but for now
        print(f"🎰 Welcome to Slots 🎰")
    
    def can_play(self):
        #checks if user has enough points to play
        #if self.player.balance >= self.spin_cost:
        if self.points >= self.spin_cost:
            return True
        else:
            #short_points = self.spin_cost - self.player.balance
            short_points = self.spin_cost - self.points
            print(f"Sorry, you need {short_points} more points to play this game.")
            sys.exit() #will return to main when there is a main

    def spin_reels(self):
        self.points -= self.spin_cost
        play = input(f"Would you like to play slots for $10? (y/n): \n")
        if play not in ['y' or 'yes']:
            print("Returning to main menu...")
            time.sleep(.5)
            sys.exit()
            #will replace w return to main 

        print(f"You now have {self.points} points.")
        time.sleep(1)
        
        print("Spinning...")
        time.sleep(3)
        
        for _ in range(15):  #number of animation frames
            spin_animation = [random.choice(self.symbols) for _ in range(3)]
            print("\r" + " | ".join(spin_animation), end="", flush=True)
            time.sleep(0.1)
        
        self.spin = [random.choice(self.symbols) for _ in range(3)]
        print("\r" + " | ".join(self.spin))  # overwrite animation with real result
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
    
    def play(self):
        while self.can_play():
            spins = self.spin_reels()
            print(self.results(spins))
            print(f"Current points: {self.points}\n")
            
            play_again =  input("Play again? (y/n): \n").strip().lower()
            if play_again not in ['y', 'yes']:
                print(f"Thanks for playing! You have {self.points} remaining.")
                break
    
if __name__ == "__main__":
    game = SlotMachine(starting_points=100) #test will be equal to the player's global points
    game.play()