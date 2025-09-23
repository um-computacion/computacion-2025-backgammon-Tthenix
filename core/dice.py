"""Dice module for the Backgammon game.

This module contains the Dice class that handles dice rolling
and move calculation for the Backgammon game.
"""

import random


class Dice:
    """Represents a pair of dice for Backgammon game.

    Handles rolling dice and determining available moves based on the roll.
    """

    def __init__(self):
        """Initialize the dice."""

    def roll(self):
        """Roll two dice and return the result.

        Returns:
            tuple: A tuple containing the values of both dice (die1, die2).
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return (die1, die2)

    def is_double(self, roll_result):
        """Check if the roll is a double (both dice show the same value).

        Args:
            roll_result (tuple): The result of a dice roll.

        Returns:
            bool: True if the roll is a double, False otherwise.
        """
        return roll_result[0] == roll_result[1]

    def get_moves(self, roll_result):
        """Get available moves based on the dice roll.

        Args:
            roll_result (tuple): The result of a dice roll.

        Returns:
            list: List of available move distances. For doubles, returns 4 moves
                 of the same value. For non-doubles, returns 2 moves.
        """
        if self.is_double(roll_result):
            return [roll_result[0]] * 4
        return [roll_result[0], roll_result[1]]
