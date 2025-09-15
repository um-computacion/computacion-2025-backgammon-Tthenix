import unittest
from unittest.mock import patch
from core.dice import Dice


class TestDice(unittest.TestCase):
    
    @patch('random.randint', side_effect=[5, 2])
    def test_roll_different_values(self, mock_randint):
        """Test rolling dice with different values (5, 2)"""
        dice = Dice()
        result = dice.roll()
        
        self.assertEqual(result, (5, 2))
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(mock_randint.called)
        self.assertEqual(mock_randint.call_count, 2)
        # Verify randint was called with correct parameters
        mock_randint.assert_any_call(1, 6)
    
    @patch('random.randint', side_effect=[3, 3])
    def test_roll_double_values(self, mock_randint):
        """Test rolling dice with double values (3, 3)"""
        dice = Dice()
        result = dice.roll()
        
        self.assertEqual(result, (3, 3))
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(mock_randint.called)
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[1, 6])
    def test_roll_edge_values(self, mock_randint):
        """Test rolling dice with edge values (1, 6)"""
        dice = Dice()
        result = dice.roll()
        
        self.assertEqual(result, (1, 6))
        self.assertTrue(mock_randint.called)
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[4, 2, 1, 5])
    def test_roll_multiple_calls(self, mock_randint):
        """Test multiple dice rolls with mocked values"""
        dice = Dice()
        
        # First roll
        result1 = dice.roll()
        self.assertEqual(result1, (4, 2))
        
        # Second roll
        result2 = dice.roll()
        self.assertEqual(result2, (1, 5))
        
        self.assertEqual(mock_randint.call_count, 4)
    
    def test_is_double_true(self):
        """Test is_double method with double values"""
        dice = Dice()
        
        double_test_cases = [
            (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)
        ]
        
        for roll_result in double_test_cases:
            with self.subTest(roll_result=roll_result):
                self.assertTrue(dice.is_double(roll_result))
    
    def test_is_double_false(self):
        """Test is_double method with non-double values"""
        dice = Dice()
        
        non_double_test_cases = [
            (1, 2), (3, 4), (2, 6), (5, 1), (6, 3), (4, 1)
        ]
        
        for roll_result in non_double_test_cases:
            with self.subTest(roll_result=roll_result):
                self.assertFalse(dice.is_double(roll_result))
    
    def test_get_moves_regular_roll(self):
        """Test get_moves method with regular (non-double) rolls"""
        dice = Dice()
        
        test_cases = [
            ((1, 2), [1, 2]),
            ((3, 4), [3, 4]),
            ((2, 6), [2, 6]),
            ((5, 1), [5, 1]),
            ((6, 3), [6, 3])
        ]
        
        for roll_result, expected_moves in test_cases:
            with self.subTest(roll_result=roll_result):
                moves = dice.get_moves(roll_result)
                self.assertEqual(sorted(moves), sorted(expected_moves))
                self.assertEqual(len(moves), 2)
    
    def test_get_moves_double_roll(self):
        """Test get_moves method with double rolls"""
        dice = Dice()
        
        for value in range(1, 7):
            with self.subTest(value=value):
                double_result = (value, value)
                moves = dice.get_moves(double_result)
                
                self.assertEqual(len(moves), 4)
                self.assertTrue(all(move == value for move in moves))
                self.assertEqual(moves, [value, value, value, value])
    
    @patch('random.randint', return_value=4)
    def test_complete_workflow_double(self, mock_randint):
        """Test complete workflow: roll -> check double -> get moves (double case)"""
        dice = Dice()
        
        # Roll dice (will return (4, 4) due to mock)
        result = dice.roll()
        self.assertEqual(result, (4, 4))
        
        # Check if it's a double
        is_double = dice.is_double(result)
        self.assertTrue(is_double)
        
        # Get moves
        moves = dice.get_moves(result)
        self.assertEqual(moves, [4, 4, 4, 4])
        self.assertEqual(len(moves), 4)
        
        self.assertEqual(mock_randint.call_count, 2)
    
    @patch('random.randint', side_effect=[2, 5])
    def test_complete_workflow_regular(self, mock_randint):
        """Test complete workflow: roll -> check double -> get moves (regular case)"""
        dice = Dice()
        
        # Roll dice (will return (2, 5) due to mock)
        result = dice.roll()
        self.assertEqual(result, (2, 5))
        
        # Check if it's a double
        is_double = dice.is_double(result)
        self.assertFalse(is_double)
        
        # Get moves
        moves = dice.get_moves(result)
        self.assertEqual(sorted(moves), sorted([2, 5]))
        self.assertEqual(len(moves), 2)
        
        self.assertEqual(mock_randint.call_count, 2)
    
    def test_dice_initialization(self):
        """Test dice object initialization"""
        dice = Dice()
        self.assertIsInstance(dice, Dice)
    
    @patch('random.randint', side_effect=Exception("Random error"))
    def test_roll_with_exception(self, mock_randint):
        """Test roll method when random.randint raises an exception"""
        dice = Dice()
        
        with self.assertRaises(Exception) as context:
            dice.roll()
        
        self.assertEqual(str(context.exception), "Random error")
        self.assertTrue(mock_randint.called)
        self.assertEqual(mock_randint.call_count, 1)


if __name__ == "__main__":
    unittest.main()