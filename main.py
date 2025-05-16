import json
import time
import os
from blackjack import Blackjack, Gambler
from slots import SlotMachine
from poker import PokerGame, initialize_player

BALANCES_FILE = "player_balances.json" 

def load_balance():
    """Loads JSON file if it exists  
    
    Returns:
        dict: A dictionary mapping player names to their saved balances.
    """
    if os.path.exists(BALANCES_FILE):
        with open(BALANCES_FILE, "r") as f: #opening as read file
            return json.load(f)
    return {} #returning as empty dictionary

def save_balance(balances):
    """Saves the updated player balances to the JSON file.

    Args:
        balances (dict): Dictionary of player names and their current balances.
    """
    with open(BALANCES_FILE, "w") as f:
        json.dump(balances, f, indent=4) #updating json file

def display_menu():
    """Displays the main game menu.

    Returns:
        str: The player's game selection input.
    """
    print("\n=== Casino Games ===")
    print("1. Poker")
    print("2. Blackjack")
    print("3. Slots")
    print("4. Exit")
    return input("\nSelect a game (1-4): ")

def main():
    balances = load_balance() #calling load balance function
    
    player1 = initialize_player()
    
    player1.name = player1.name.strip().lower()
    #adding player name to file if not already in it
    if player1.name not in balances: 
        balances[player1.name] = 500
    else:
        #printing return message
        player1.balance = balances[player1.name]
        time.sleep(1)
        print(f"Welcome back, {player1.name}! Your saved balance is ${player1.balance}")
        time.sleep(2)
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            pokergame = PokerGame(player1)
            while True:
                print("\n=== Poker ===")
                print(f"Your balance: ${player1.balance}")
                pokergame.round()
                if input("\nPlay another round? (y/n): ").lower() != 'y':
                    balances[player1.name] = player1.balance #updating balance
                    save_balance(balances)
                    break
                    
        elif choice == '2':
            gambler_player = Gambler(player1.balance, player1.name)
            blackjack = Blackjack(gambler_player)
            blackjack.play()
            player1.balance = gambler_player.chips
            
            balances[player1.name] = player1.balance
            save_balance(balances) #saving balance after each game
            
        elif choice == '3':
            slots = SlotMachine(player1.balance, player1.name)
            slots.play()
            
            player1.balance = slots.points
            #update player's balance 
            balances[player1.name] = player1.balance
            save_balance(balances) #saving balance after each game
            
        elif choice == '4':
            print(f"\nThanks for playing {player1.name}! Final balance: ${player1.balance}")
            
            balances[player1.name] = player1.balance
            save_balance(balances) #saving final balance
            break
            
        else:
            print("\nInvalid choice. Please select 1-4.")
            
if __name__ == '__main__':
    main()