"""Unit tests for the Checker class covering state and transitions."""

import unittest
from core.checker import Checker

# pylint: disable=C0116  # many simple test methods without individual docstrings


class TestChecker(unittest.TestCase):
    """Test suite for core Checker behavior and edge cases."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__white_checker__ = Checker("white")
        self.__black_checker__ = Checker("black")

    def test_checker_initialization_with_white_color(self):
        """Test checker initialization with white color.

        Returns:
            None
        """
        checker = Checker("white")

        self.assertEqual(checker.__color__, "white")
        self.assertIsNone(checker.__position__)
        self.assertFalse(checker.__is_on_bar__)
        self.assertFalse(checker.__is_borne_off__)

    def test_checker_initialization_with_black_color(self):
        """Test checker initialization with black color.

        Returns:
            None
        """
        checker = Checker("black")

        self.assertEqual(checker.__color__, "black")
        self.assertIsNone(checker.__position__)
        self.assertFalse(checker.__is_on_bar__)
        self.assertFalse(checker.__is_borne_off__)

    def test_invalid_color_raises_exception(self):
        """Test that invalid color raises ValueError.

        Returns:
            None

        Raises:
            ValueError: When invalid color is provided
        """
        with self.assertRaises(ValueError) as context:
            Checker("red")

        self.assertIn("Color must be 'white' or 'black'", str(context.exception))

    def test_none_color_raises_exception(self):
        """Test that None color raises ValueError.

        Returns:
            None

        Raises:
            ValueError: When None color is provided
        """
        with self.assertRaises(ValueError) as context:
            Checker(None)

        self.assertIn("Color must be 'white' or 'black'", str(context.exception))

    def test_place_checker_on_valid_point(self):
        self.__white_checker__.place_on_point(5)

        self.assertEqual(self.__white_checker__.__position__, 5)
        self.assertFalse(self.__white_checker__.__is_on_bar__)
        self.assertFalse(self.__white_checker__.__is_borne_off__)

    def test_place_checker_on_point_1(self):
        self.__black_checker__.place_on_point(1)
        self.assertEqual(self.__black_checker__.__position__, 1)

    def test_place_checker_on_point_24(self):
        self.__white_checker__.place_on_point(24)
        self.assertEqual(self.__white_checker__.__position__, 24)

    def test_place_checker_on_invalid_point_below_range(self):
        with self.assertRaises(ValueError) as context:
            self.__white_checker__.place_on_point(0)
        self.assertIn("Position must be between 1 and 24", str(context.exception))

    def test_place_checker_on_invalid_point_above_range(self):
        with self.assertRaises(ValueError) as context:
            self.__black_checker__.place_on_point(25)

        self.assertIn("Position must be between 1 and 24", str(context.exception))

    def test_move_checker_from_point_to_point(self):
        self.__white_checker__.place_on_point(8)
        self.__white_checker__.move_to_point(12)

        self.assertEqual(self.__white_checker__.__position__, 12)
        self.assertFalse(self.__white_checker__.__is_on_bar__)
        self.assertFalse(self.__white_checker__.__is_borne_off__)

    def test_move_checker_when_not_placed_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            self.__white_checker__.move_to_point(5)

        self.assertIn("Checker must be placed before moving", str(context.exception))

    def test_move_checker_when_on_bar_raises_exception(self):
        self.__white_checker__.send_to_bar()

        with self.assertRaises(ValueError) as context:
            self.__white_checker__.move_to_point(5)

        self.assertIn("Checker on bar cannot move directly", str(context.exception))

    def test_move_checker_when_borne_off_raises_exception(self):
        self.__white_checker__.place_on_point(1)
        self.__white_checker__.bear_off()

        with self.assertRaises(ValueError) as context:
            self.__white_checker__.move_to_point(5)

        self.assertIn(
            "Checker has already been removed from board", str(context.exception)
        )

    def test_send_checker_to_bar(self):
        self.__white_checker__.place_on_point(10)
        self.__white_checker__.send_to_bar()

        self.assertIsNone(self.__white_checker__.__position__)
        self.assertTrue(self.__white_checker__.__is_on_bar__)
        self.assertFalse(self.__white_checker__.__is_borne_off__)
        with self.assertRaises(ValueError) as ctx:
            self.__white_checker__.move_to_point(2)
        self.assertIn("Checker on bar cannot move directly", str(ctx.exception))

    def test_send_already_barred_checker_to_bar_raises_exception(self):
        self.__white_checker__.place_on_point(5)
        self.__white_checker__.send_to_bar()

        with self.assertRaises(ValueError) as context:
            self.__white_checker__.send_to_bar()

        self.assertIn("Checker is already on bar", str(context.exception))

    def test_return_checker_from_bar(self):
        self.__black_checker__.place_on_point(15)
        self.__black_checker__.send_to_bar()
        self.__black_checker__.return_from_bar(20)

        self.assertEqual(self.__black_checker__.__position__, 20)
        self.assertFalse(self.__black_checker__.__is_on_bar__)
        self.assertFalse(self.__black_checker__.__is_borne_off__)

    def test_return_checker_not_on_bar_raises_exception(self):
        self.__black_checker__.place_on_point(10)

        with self.assertRaises(ValueError) as context:
            self.__black_checker__.return_from_bar(15)

        self.assertIn("Checker is not on bar", str(context.exception))

    def test_bear_off_checker(self):
        self.__white_checker__.place_on_point(2)
        self.__white_checker__.bear_off()

        self.assertIsNone(self.__white_checker__.__position__)
        self.assertFalse(self.__white_checker__.__is_on_bar__)
        self.assertTrue(self.__white_checker__.__is_borne_off__)

    def test_bear_off_unplaced_checker_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            self.__white_checker__.bear_off()

        self.assertIn(
            "Checker must be placed before bearing off", str(context.exception)
        )

    def test_bear_off_checker_on_bar_raises_exception(self):
        self.__white_checker__.place_on_point(8)
        self.__white_checker__.send_to_bar()

        with self.assertRaises(ValueError) as context:
            self.__white_checker__.bear_off()

        self.assertIn("Checker on bar cannot be borne off", str(context.exception))

    def test_bear_off_already_borne_off_checker_raises_exception(self):
        self.__black_checker__.place_on_point(22)
        self.__black_checker__.bear_off()

        with self.assertRaises(ValueError) as context:
            self.__black_checker__.bear_off()

        self.assertIn(
            "Checker has already been removed from board", str(context.exception)
        )

    def test_checker_can_move_when_placed(self):
        self.__white_checker__.place_on_point(15)

        self.assertTrue(self.__white_checker__.can_move())

    def test_checker_cannot_move_when_not_placed(self):
        self.assertFalse(self.__white_checker__.can_move())

    def test_checker_cannot_move_when_on_bar(self):
        self.__black_checker__.place_on_point(10)
        self.__black_checker__.send_to_bar()

        self.assertFalse(self.__black_checker__.can_move())

    def test_checker_cannot_move_when_borne_off(self):
        self.__white_checker__.place_on_point(3)
        self.__white_checker__.bear_off()

        self.assertFalse(self.__white_checker__.can_move())

    def test_checker_can_be_captured_when_placed(self):
        self.__black_checker__.place_on_point(18)

        self.assertTrue(self.__black_checker__.can_be_captured())

    def test_checker_cannot_be_captured_when_not_placed(self):
        self.assertFalse(self.__white_checker__.can_be_captured())

    def test_checker_cannot_be_captured_when_on_bar(self):
        self.__white_checker__.place_on_point(7)
        self.__white_checker__.send_to_bar()

        self.assertFalse(self.__white_checker__.can_be_captured())

    def test_checker_cannot_be_captured_when_borne_off(self):
        self.__black_checker__.place_on_point(19)
        self.__black_checker__.bear_off()

        self.assertFalse(self.__black_checker__.can_be_captured())

    def test_checker_string_representation_when_not_placed(self):
        expected = "Checker(color=white, position=None, on_bar=False, borne_off=False)"
        self.assertEqual(str(self.__white_checker__), expected)

    def test_checker_string_representation_when_placed(self):
        self.__black_checker__.place_on_point(12)
        expected = "Checker(color=black, position=12, on_bar=False, borne_off=False)"
        self.assertEqual(str(self.__black_checker__), expected)

    def test_checker_string_representation_when_on_bar(self):
        self.__white_checker__.place_on_point(6)
        self.__white_checker__.send_to_bar()
        expected = "Checker(color=white, position=None, on_bar=True, borne_off=False)"
        self.assertEqual(str(self.__white_checker__), expected)

    def test_checker_string_representation_when_borne_off(self):
        self.__black_checker__.place_on_point(21)
        self.__black_checker__.bear_off()
        expected = "Checker(color=black, position=None, on_bar=False, borne_off=True)"
        self.assertEqual(str(self.__black_checker__), expected)

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
        self.__white_checker__.place_on_point(15)
        self.__white_checker__.send_to_bar()
        self.__white_checker__.reset()

        self.assertIsNone(self.__white_checker__.__position__)
        self.assertFalse(self.__white_checker__.__is_on_bar__)
        self.assertFalse(self.__white_checker__.__is_borne_off__)

    def test_get_checker_state(self):
        self.__black_checker__.place_on_point(8)
        state = self.__black_checker__.get_state()

        self.assertIn("color", state)
        self.assertIn("position", state)
        self.assertIn("is_on_bar", state)
        self.assertIn("is_borne_off", state)
        self.assertEqual(state["color"], "black")
        self.assertEqual(state["position"], 8)
        self.assertFalse(state["is_on_bar"])
        self.assertFalse(state["is_borne_off"])

    def test_copy_checker(self):
        self.__white_checker__.place_on_point(20)
        checker_copy = self.__white_checker__.copy()

        self.assertEqual(checker_copy.__color__, self.__white_checker__.__color__)
        self.assertEqual(checker_copy.__position__, self.__white_checker__.__position__)
        self.assertEqual(
            checker_copy.__is_on_bar__, self.__white_checker__.__is_on_bar__
        )
        self.assertEqual(
            checker_copy.__is_borne_off__, self.__white_checker__.__is_borne_off__
        )

        self.__white_checker__.move_to_point(24)
        self.assertEqual(checker_copy.__position__, 20)

    def test_multiple_state_transitions(self):
        self.__black_checker__.place_on_point(10)
        self.assertEqual(self.__black_checker__.__position__, 10)

        self.__black_checker__.move_to_point(15)
        self.assertEqual(self.__black_checker__.__position__, 15)

        self.__black_checker__.send_to_bar()
        self.assertTrue(self.__black_checker__.__is_on_bar__)

        self.__black_checker__.return_from_bar(20)
        self.assertEqual(self.__black_checker__.__position__, 20)
        self.assertFalse(self.__black_checker__.__is_on_bar__)

        self.__black_checker__.bear_off()
        self.assertTrue(self.__black_checker__.__is_borne_off__)
        self.assertIsNone(self.__black_checker__.__position__)


if __name__ == "__main__":
    unittest.main()
