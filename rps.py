"""A template for a python script deliverable for INST326.

Driver: Brenda Ngaba
Navigator: Abdoullah Sankoh, and Ibrahim Sesay
Assignment: Template INST326
Date: 1_24_25

Challenges Encountered: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import sys
import argparse
import os

def determine_winner(p1, p2):
    
    """ Determines which hand sign wins the round of rock, paper, scissors.
    Args:
        p1: Player 1's choice between rock, paper and scissors.
        p2: Player 2's choice between rock, paper and scissors.
    Returns: 
        Either the player who wins the round a tie if there is one.

    """
    #insert code and docstrings here
    p1_choice = input("Player 1, please choose rock, paper or scissors (r,p,s).")
    p2_choice = input("Player 2, please choose rock, paper or scissors (r,p,s).")
   
    r = 'rock'
    p = 'paper'
    s = 'scissors'
    
    p1_choice1 = p1_choice
    p2_choice1 = p2_choice

    
    if p1_choice1 == 's' and p2_choice1 == 'r':
        return 'player2'
    elif p1_choice1 == 'p' and p2_choice1 == 's':
        return 'player2'
    elif p1_choice1 == 's' and p2_choice1 == 'p':
        return 'player1'
    elif p1_choice1 == 'p' and p2_choice1 == 'r':
        return 'player1'
    elif p1_choice1 == 'r' and p2_choice1 == 'p':
        return 'player2'
    else:
        print("There is a tie.")
        return 'tie'
    
    pass
    '''
def main(player1_name, player2_name):
    #insert code and docstrings here
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
    '''