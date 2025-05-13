""" Script that tests rps program.
"""

from rps1 import rps

def test_tie():
    """Testing if the rock, paper, scissors games tie function works."""
    assert rps("rock", "rock") == 0
    assert rps("scissors", "scissors") == 0
    assert rps("paper", "paper") == 0
    
def test_item_1():
    """Testing if item 1 defeats item 2."""
    assert rps("rock", "scissors") == 1
    assert rps("paper", "rock") == 1
    assert rps("scissors", "paper") == 1

def test_item_2():
    """Testing if item 2 defeats item 1."""
    assert rps("scissors", "rock") == 2
    assert rps("rock", "paper") == 2
    assert rps("paper", "scissors") == 2