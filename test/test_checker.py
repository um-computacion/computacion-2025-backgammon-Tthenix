import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):
	
	def setUp(self):
		self.white_checker = Checker("white")
		self.black_checker = Checker("black")
	
	def test_checker_initialization_with_white_color(self):
		checker = Checker("white")
		
		self.assertEqual(checker.color, "white")
		self.assertIsNone(checker.position)
		self.assertFalse(checker.is_on_bar)
		self.assertFalse(checker.is_borne_off)
	
	def test_checker_initialization_with_black_color(self):
		checker = Checker("black")
		
		self.assertEqual(checker.color, "black")
		self.assertIsNone(checker.position)
		self.assertFalse(checker.is_on_bar)
		self.assertFalse(checker.is_borne_off)
	
	def test_invalid_color_raises_exception(self):
		with self.assertRaises(ValueError) as context:
			Checker("red")
		
		self.assertIn("Color must be 'white' or 'black'", str(context.exception))
	
	def test_none_color_raises_exception(self):
		with self.assertRaises(ValueError) as context:
			Checker(None)
		
		self.assertIn("Color must be 'white' or 'black'", str(context.exception))
	
	def test_place_checker_on_valid_point(self):
		self.white_checker.place_on_point(5)
		
		self.assertEqual(self.white_checker.position, 5)
		self.assertFalse(self.white_checker.is_on_bar)
		self.assertFalse(self.white_checker.is_borne_off)
	
	def test_place_checker_on_point_1(self):
		self.black_checker.place_on_point(1)
		
		self.assertEqual(self.black_checker.position, 1)
	
	def test_place_checker_on_point_24(self):
		self.white_checker.place_on_point(24)
		
		self.assertEqual(self.white_checker.position, 24)
	
	def test_place_checker_on_invalid_point_below_range(self):
		with self.assertRaises(ValueError) as context:
			self.white_checker.place_on_point(0)
		
		self.assertIn("Position must be between 1 and 24", str(context.exception))
	
	def test_place_checker_on_invalid_point_above_range(self):
		with self.assertRaises(ValueError) as context:
			self.black_checker.place_on_point(25)
		
		self.assertIn("Position must be between 1 and 24", str(context.exception))
	
	def test_move_checker_from_point_to_point(self):
		self.white_checker.place_on_point(8)
		self.white_checker.move_to_point(12)
		
		self.assertEqual(self.white_checker.position, 12)
		self.assertFalse(self.white_checker.is_on_bar)
		self.assertFalse(self.white_checker.is_borne_off)
	
	def test_move_checker_when_not_placed_raises_exception(self):
		with self.assertRaises(ValueError) as context:
			self.white_checker.move_to_point(5)
		
		self.assertIn("Checker must be placed before moving", str(context.exception))
	
	def test_move_checker_when_on_bar_raises_exception(self):
		self.white_checker.send_to_bar()
		
		with self.assertRaises(ValueError) as context:
			self.white_checker.move_to_point(5)
		
		self.assertIn("Checker on bar cannot move directly", str(context.exception))
	
	def test_move_checker_when_borne_off_raises_exception(self):
		self.white_checker.place_on_point(1)
		self.white_checker.bear_off()
		
		with self.assertRaises(ValueError) as context:
			self.white_checker.move_to_point(5)
		
		self.assertIn("Checker has already been removed from board", str(context.exception))
	
	def test_send_checker_to_bar(self):
		self.white_checker.place_on_point(10)
		self.white_checker.send_to_bar()
		
		self.assertIsNone(self.white_checker.position)
		self.assertTrue(self.white_checker.is_on_bar)
		self.assertFalse(self.white_checker.is_borne_off)
	
	def test_move_checker_when_on_bar_raises_exception(self):
		self.white_checker.place_on_point(1)
		self.white_checker.send_to_bar()
  
		with self.assertRaises(ValueError) as ctx:
			self.white_checker.move_to_point(2)
		self.assertIn("Checker on bar cannot move directly", str(ctx.exception))

	def test_send_already_barred_checker_to_bar_raises_exception(self):
		self.white_checker.place_on_point(5)
		self.white_checker.send_to_bar()
		
		with self.assertRaises(ValueError) as context:
			self.white_checker.send_to_bar()
		
		self.assertIn("Checker is already on bar", str(context.exception))
	
	def test_return_checker_from_bar(self):
		self.black_checker.place_on_point(15)
		self.black_checker.send_to_bar()
		self.black_checker.return_from_bar(20)
		
		self.assertEqual(self.black_checker.position, 20)
		self.assertFalse(self.black_checker.is_on_bar)
		self.assertFalse(self.black_checker.is_borne_off)
	
	def test_return_checker_not_on_bar_raises_exception(self):
		self.black_checker.place_on_point(10)
		
		with self.assertRaises(ValueError) as context:
			self.black_checker.return_from_bar(15)
		
		self.assertIn("Checker is not on bar", str(context.exception))
	
	def test_bear_off_checker(self):
		self.white_checker.place_on_point(2)
		self.white_checker.bear_off()
		
		self.assertIsNone(self.white_checker.position)
		self.assertFalse(self.white_checker.is_on_bar)
		self.assertTrue(self.white_checker.is_borne_off)
	
	def test_bear_off_unplaced_checker_raises_exception(self):
		with self.assertRaises(ValueError) as context:
			self.white_checker.bear_off()
		
		self.assertIn("Checker must be placed before bearing off", str(context.exception))
	
	def test_bear_off_checker_on_bar_raises_exception(self):
		self.white_checker.place_on_point(8)
		self.white_checker.send_to_bar()
		
		with self.assertRaises(ValueError) as context:
			self.white_checker.bear_off()
		
		self.assertIn("Checker on bar cannot be borne off", str(context.exception))
	
	def test_bear_off_already_borne_off_checker_raises_exception(self):
		self.black_checker.place_on_point(22)
		self.black_checker.bear_off()
		
		with self.assertRaises(ValueError) as context:
			self.black_checker.bear_off()
		
		self.assertIn("Checker has already been removed from board", str(context.exception))
	
	def test_checker_can_move_when_placed(self):
		self.white_checker.place_on_point(15)
		
		self.assertTrue(self.white_checker.can_move())
	
	def test_checker_cannot_move_when_not_placed(self):
		self.assertFalse(self.white_checker.can_move())
	
	def test_checker_cannot_move_when_on_bar(self):
		self.black_checker.place_on_point(10)
		self.black_checker.send_to_bar()
		
		self.assertFalse(self.black_checker.can_move())
	
	def test_checker_cannot_move_when_borne_off(self):
		self.white_checker.place_on_point(3)
		self.white_checker.bear_off()
		
		self.assertFalse(self.white_checker.can_move())
	
	def test_checker_can_be_captured_when_placed(self):
		self.black_checker.place_on_point(18)
		
		self.assertTrue(self.black_checker.can_be_captured())
	
	def test_checker_cannot_be_captured_when_not_placed(self):
		self.assertFalse(self.white_checker.can_be_captured())
	
	def test_checker_cannot_be_captured_when_on_bar(self):
		self.white_checker.place_on_point(7)
		self.white_checker.send_to_bar()
		
		self.assertFalse(self.white_checker.can_be_captured())
	
	def test_checker_cannot_be_captured_when_borne_off(self):
		self.black_checker.place_on_point(19)
		self.black_checker.bear_off()
		
		self.assertFalse(self.black_checker.can_be_captured())
	
	def test_checker_string_representation_when_not_placed(self):
		expected = "Checker(color=white, position=None, on_bar=False, borne_off=False)"
		self.assertEqual(str(self.white_checker), expected)
	
	def test_checker_string_representation_when_placed(self):
		self.black_checker.place_on_point(12)
		expected = "Checker(color=black, position=12, on_bar=False, borne_off=False)"
		self.assertEqual(str(self.black_checker), expected)
	
	def test_checker_string_representation_when_on_bar(self):
		self.white_checker.place_on_point(6)
		self.white_checker.send_to_bar()
		expected = "Checker(color=white, position=None, on_bar=True, borne_off=False)"
		self.assertEqual(str(self.white_checker), expected)
	
	def test_checker_string_representation_when_borne_off(self):
		self.black_checker.place_on_point(21)
		self.black_checker.bear_off()
		expected = "Checker(color=black, position=None, on_bar=False, borne_off=True)"
		self.assertEqual(str(self.black_checker), expected)
	
	def test_checker_equality_based_on_color_and_state(self):
		checker1 = Checker("white")
		checker2 = Checker("white")
		checker3 = Checker("black")
		
		checker1.place_on_point(5)
		checker2.place_on_point(5)
		
		self.assertEqual(checker1, checker2)
		self.assertNotEqual(checker1, checker3)
	
	def test_checker_hash_consistency(self):
		checker1 = Checker("white")
		checker2 = Checker("white")
		
		checker1.place_on_point(10)
		checker2.place_on_point(10)
		
		self.assertEqual(hash(checker1), hash(checker2))
	
	def test_reset_checker_state(self):
		self.white_checker.place_on_point(15)
		self.white_checker.send_to_bar()
		self.white_checker.reset()
		
		self.assertIsNone(self.white_checker.position)
		self.assertFalse(self.white_checker.is_on_bar)
		self.assertFalse(self.white_checker.is_borne_off)
	
	def test_get_checker_state(self):
		self.black_checker.place_on_point(8)
		state = self.black_checker.get_state()
		
		self.assertIn('color', state)
		self.assertIn('position', state)
		self.assertIn('is_on_bar', state)
		self.assertIn('is_borne_off', state)
		self.assertEqual(state['color'], 'black')
		self.assertEqual(state['position'], 8)
		self.assertFalse(state['is_on_bar'])
		self.assertFalse(state['is_borne_off'])
	
	def test_copy_checker(self):
		self.white_checker.place_on_point(20)
		checker_copy = self.white_checker.copy()
		
		self.assertEqual(checker_copy.color, self.white_checker.color)
		self.assertEqual(checker_copy.position, self.white_checker.position)
		self.assertEqual(checker_copy.is_on_bar, self.white_checker.is_on_bar)
		self.assertEqual(checker_copy.is_borne_off, self.white_checker.is_borne_off)
		
		self.white_checker.move_to_point(24)
		self.assertEqual(checker_copy.position, 20)
	
	def test_multiple_state_transitions(self):
		self.black_checker.place_on_point(10)
		self.assertEqual(self.black_checker.position, 10)
		
		self.black_checker.move_to_point(15)
		self.assertEqual(self.black_checker.position, 15)
		
		self.black_checker.send_to_bar()
		self.assertTrue(self.black_checker.is_on_bar)
		
		self.black_checker.return_from_bar(20)
		self.assertEqual(self.black_checker.position, 20)
		self.assertFalse(self.black_checker.is_on_bar)
		
		self.black_checker.bear_off()
		self.assertTrue(self.black_checker.is_borne_off)
		self.assertIsNone(self.black_checker.position)

if __name__ == "__main__":
	unittest.main()