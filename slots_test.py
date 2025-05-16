""" Script that tests slots machine game results"""
import pytest
from slots import SlotMachine
# test_slot_machine.py

def test_can_play_true():
    """Testing if 'y' or 'yes' returns True."""
    
    game = SlotMachine(100)
    assert game.can_play() is True

def test_can_play_false():
    """Testing input that is not 'y' or 'yes' returns False."""
    
    game = SlotMachine(5)
    with pytest.raises(SystemExit):
        game.can_play()
        
def test_jackpot():
    """Testing Jackpot result. """
    
    game = SlotMachine(100)
    game.points -= game.spin_cost  #simulating spin deduction
    result = game.results(['🍋', '🍋', '🍋'])
    expected_reward = (10 * 3) + 50
    assert "JACKPOT" in result
    assert game.points == 100 - game.spin_cost + expected_reward

def test_two_match_start():
    """Testing two matching symbols at the start of the result. """
    
    game = SlotMachine(100)
    game.points -= game.spin_cost 
    result = game.results(['🔔', '🔔', '🍀'])
    expected_reward = (30 * 2)
    assert "Two matching" in result
    assert game.points == 100 - game.spin_cost + expected_reward

def test_two_match_end():
    """Testing two matching symbols at the end of the result. """
    
    game = SlotMachine(100)
    game.points -= game.spin_cost 
    result = game.results(['🍀', '🍒', '🍒'])
    expected_reward = (20 * 2)
    assert "Two matching" in result
    assert game.points == 100 - game.spin_cost + expected_reward

def test_no_match_result():
    """Testing no matching symbols. """
    
    game = SlotMachine(100)
    game.points -= game.spin_cost 
    result = game.results(['🍒', '💎', '🍋'])
    assert result == "No match. Try again!"
    assert game.points == 100 - game.spin_cost 

def test_spin_cost():
    """Testing spin cost calculation."""
    game = SlotMachine(100)
    starting_points = game.points
    game.points -= game.spin_cost  #simulating a spin
    assert game.spin_cost == 10
    assert game.points == starting_points - 10