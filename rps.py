""" Program that performs rock, paper, scissors and determines the winner.
"""

import sys
import argparse
import os

def determine_winner(p1, p2):
    #insert code and docstrings here
    """ Determines which player wins rock, paper, scissors.
    Args:
        p1 (str): Player 1's choice between rock, paper and scissors, represented as (r,p,s).
        p2 (str): Player 2's choice between rock, paper and scissors, represented as (r,p,s).
    Returns: 
        Either 'Player1', 'Player2 or 'tie' if there is one.
    """

    #determining which player wins based on their chosen hand sign
    if p1 == p2:
        return 'tie'
    elif (p1 == 'r' or p1 == 'rock') and (p2 == 's' or p2 == 'scissors'): #ensuring both spelt out an shorthand versions are valid input
        return 'player1'
    elif (p1 == 's' or p1 == 'scissors') and (p2 == 'p' or p2 == 'paper'):
        return 'player1'
    elif (p1 == 'p' or p1 == 'paper') and (p2 == 'r' or p2 == 'rock'):
        return 'player1'
    else:
        return 'player2'
        
    
def main(player1_name, player2_name):
    #insert code and docstrings here
    """ Handles main game logic for rock, paper, scissors.

    Asks the user to input both player's hand shape, clears the screen
    after each input, and calls the determine_winner function to revealsthe winner.

    Args:
        player1_name (str): The name of player 1, inserted at command line.
        player2_name (str): The name of Player 2, inserted at command line.

    Returns:
        None
    """

     #asking user to input both player's hand sign
    p1_choice = input(f"Enter {player1_name}'s hand shape (r,p,s).\n")
    
    #validating input
    while p1_choice not in ['r', 'rock', 'p', 'paper', 's', 'scissors']:
        print("That response was not understood. Please enter rock, paper, or scissors (r, p, s).")
        p1_choice = input(f"Enter {player1_name}'s hand shape (r,p,s).\n")
        os.system('cls||clear')
        
    
    p2_choice = input(f"Enter {player2_name}'s hand shape (r,p,s).\n")
    
        #validating input
    while p2_choice not in ['r', 'rock', 'p', 'paper', 's', 'scissors']:
        print("That response was not understood. Please enter rock, paper, or scissors (r, p, s).")
        p2_choice = input(f"Enter {player2_name}'s hand shape (r,p,s).\n")
        
        os.system('cls||clear')
        
    #assigning player's choices to variables p1 and p2 for consistency 
    p1 = p1_choice
    p2 = p2_choice 
    
    
    result = determine_winner(p1, p2) #calling on determine winner module
    
    #printing the game's results
    if result == 'tie':
        print("There is a tie.")
    elif result == 'player1':
        print(f"{player1_name} wins!")
    elif result == 'player2':
        print(f"{player2_name} wins!")
    
    pass


def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
    args_list (list) : the list of strings from the command prompt
    Returns:
    args (ArgumentParser)
    """
    #For the sake of readability it is important to insert comments all throughout.
    #Complicated operations get a few lines of comments before the operations commence.
    #Non-obvious ones get comments at the end of the line.
    #For example:
    #This function uses the argparse module in order to parse command line arguments.
    
    parser = argparse.ArgumentParser() #Create an ArgumentParser object.
    
    #Then we will add arguments to this parser object.
    #In this case, we have a required positional argument.
    #Followed by an optional keyword argument which contains a default value.
    
    parser.add_argument('p1_name', type=str, help="Please enter Player1's Name")
    parser.add_argument('p2_name', type=str, help="Please enter Player2's Name")
    
    args = parser.parse_args(args_list) #We need to parse the list of command line arguments using this object.
    
    return args

if __name__ == "__main__":
    
    #If name == main statements are statements that basically ask:
    #Is the current script being run natively or as a module?

    #It the script is being run as a module, the block of code under this will not beexecuted.
    #If the script is being run natively, the block of code below this will be executed.

    arguments = parse_args(sys.argv[1:]) #Pass in the list of command line arguments to the parse_args function.
    
    #The returned object is an object with those command line arguments as attributes of an object.
    #We will pass both of these arguments into the main function.
    #Note that you do not need a main function, but you might find it helpfull.
    #You do want to make sure to have minimal code under the 'if __name__ == "__main__":' statement.

    main(arguments.p1_name, arguments.p2_name)
