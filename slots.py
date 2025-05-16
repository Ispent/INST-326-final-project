""" Slot machine game"""
import random
import time

class SlotMachine:
    """A class representing a CLI-based slot machine game.
    
    Attributes:
        symbols (list): The emoji symbols available on the reels.
        symbol_value (dict): Point value for each symbol.
        points (int): Current number of points the player has.
        spin_cost (int): Cost in points to play a single spin.
    """
    def __init__(self, starting_points, player_name): 
        """Initializes the SlotMachine with starting points.
        
        Args:
            starting_points (int): The player's initial balance.
        Side effects:
            Prints a welcome message to terminal.
        """
        self.points = starting_points 
        self.player_name = player_name
        
        self.symbols = ['🍒', '🍋', '🔔', '💎', '🍀']
        
        #using dictionary to add values to symbols
        self.symbol_value = {
            '🍒' : 20,
            '🍋' : 10,
            '🔔' : 30, 
            '💎' : 50, 
            '🍀' : 25
            }
        
        self.spin_cost = 10 #cost of each spin
        
        print(f"Hi {player_name}! 🎰 Welcome to Slots 🎰 ")
    
    def can_play(self):
        """ Checks if the player has enough points to play.
    
        Returns:
            Boolean: True if the player has enough points.
        Side effects:
            Returns to the main menu if the player has insufficient points.
        """
        #checks if user has enough points to play
        #if self.player.balance >= self.spin_cost:
        
        #using boolean flag to determine if player has enough points to spin reel
        if self.points >= self.spin_cost:
            return True
        
        else:
            #logic for if player doesn't have enough points
            #short_points = self.spin_cost - self.player.balance
            short_points = self.spin_cost - self.points
            print(f"Sorry, you need {short_points} more points to play this game.")
            return False
    
    def start_game(self):
        """Asks user if they want to play the game.yy
        
        Args:
            None
        Returns:
            Boolean: True if player says 'y' or 'yes'.
        """
        
        play = input(f"Would you like to play slots for $10? (y/n): \n")

        return play in ['y', 'yes']
    
        

    def spin_reels(self):
        """Deducts the spin cost, prompts the player, and simulates reel spinning.
    
        Returns:
            list: A list of three random symbols representing the final spin result.
        Side effects:
            Prints spinning animation and spin result.
        """

        #if user doesnt say yes they return to main menu
        if not self.start_game(): 
            print("Returning to main menu...")
            time.sleep(.5)
            return None
            
        self.points -= self.spin_cost #subtracting spin cost from users balance 
        print(f"You now have ${self.points}.")
        time.sleep(1)
        
        print("Spinning...")
        time.sleep(3)
        
        #reel spin animation 
        for _ in range(15):  #number of animation frames
            spin_animation = [random.choice(self.symbols) for _ in range(3)]
            print("\r" + " | ".join(spin_animation), end="", flush=True) #overwriting each line with a new spin 
            time.sleep(0.1)
        
        self.spin = [random.choice(self.symbols) for _ in range(3)]
        print("\r" + " | ".join(self.spin))  # overwrite animation with final spin result
        return self.spin

    def results(self, spins):
        """Evaluates the spin result and calculates any reward.
    
        Args:
            spins (list): A list of three symbols from the spin.
        Returns:
            str: A message describing the result and points earned.
        Side effects:
            Updates the player's balance based on the result.
        """
        if spins[0] == spins[1] == spins[2]: #all 3 symbols matching
            reward = ((self.symbol_value[spins[0]] * 3) + 50) #adding an extra $50 for jackpot
            self.points += reward
            return f"🎉 JACKPOT! +${reward}"
        
         #logic if only 2 symbols are matching
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
        return f"Two matching symbols! + ${reward}"
    
    def play_again(self):
        """Asks user to play again.
        Args:
            None
        Returns:
            Boolean: True if player says 'y' or 'yes'.
        """
        play_again =  input("Play again? (y/n): \n").strip().lower()
        return play_again in ['y', 'yes']
    
    def play(self):
        """Runs the main game loop that allows the player to spin the reel and play again."""
        
        #gameplay logic
        while self.can_play(): #if can_play returns true
            spins = self.spin_reels() #spinning reel
            
            if spins is None: #returning to main menu
                break
            
            #printing spin results
            print(self.results(spins)) 
            print(f"Current points: {self.points}\n")
            
            #play again logic
            if not self.play_again(): #if user doesn't choose to play again
                print(f"Thanks for playing! You have ${self.points} remaining.")
                break

 
    
if __name__ == "__main__":
    #creating an instance of the SlotMachine class
    game = SlotMachine(starting_points=100, player_name="Test") #test will be equal to the player's global points when ran in main
    game.play()