from blackjack import Blackjack
from slots import SlotMachine
from poker import PokerGame, initialize_player

def display_menu():
    print("\n=== Casino Games ===")
    print("1. Poker")
    print("2. Blackjack")
    print("3. Slots")
    print("4. Exit")
    return input("\nSelect a game (1-4): ")

def main():
    player1 = initialize_player()
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            pokergame = PokerGame(player1)
            while True:
                print("\n=== Poker ===")
                print(f"Your balance: ${player1.balance}")
                pokergame.round()
                if input("\nPlay another round? (y/n): ").lower() != 'y':
                    break
                    
        elif choice == '2':
            blackjack = Blackjack()
            blackjack.play(player1.balance)
            player1.balance = blackjack.players[0].chips
            
        elif choice == '3':
            slots = SlotMachine(player1.balance)
            slots.play()
            # Update player's balance after slots
            player1.balance = slots.points
            
        elif choice == '4':
            print(f"\nThanks for playing! Final balance: ${player1.balance}")
            break
            
        else:
            print("\nInvalid choice. Please select 1-4.")
            
if __name__ == '__main__':
    main()