import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):
    
    def test_roll_returns_two_integers(self):
        dice = Dice()
        
        result = dice.roll()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(v, int) for v in result))
        self.assertTrue(all(1 <= v <= 6 for v in result))
    
    def test_roll_multiple_times(self):
        dice = Dice()
        
        for _ in range(10):
            result = dice.roll()
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertTrue(all(1 <= v <= 6 for v in result))
    
    def test_is_double_true(self):
        dice = Dice()
        
        for value in range(1, 7):
            double_result = (value, value)
            self.assertTrue(dice.is_double(double_result))
    
    def test_is_double_false(self):
        dice = Dice()
 
        non_double_results = [(1, 2), (3, 4), (2, 6), (5, 1)]
        for result in non_double_results:
            self.assertFalse(dice.is_double(result))
    
    def test_get_moves_regular(self):
        dice = Dice()
        
        test_cases = [
            ((1, 2), [1, 2]),
            ((3, 4), [3, 4]),
            ((2, 6), [2, 6]),
            ((5, 1), [5, 1])
        ]
        for result, expected in test_cases:
            moves = dice.get_moves(result)
            self.assertEqual(sorted(moves), sorted(expected))
    
    def test_get_moves_double(self):
        dice = Dice()
        
        for value in range(1, 7):
            double_result = (value, value)
            moves = dice.get_moves(double_result)
            self.assertEqual(len(moves), 4)
            self.assertTrue(all(move == value for move in moves))
    
    def test_dice_initialization(self):
        dice = Dice()
        self.assertIsInstance(dice, Dice)

if __name__ == "__main__":
    unittest.main()