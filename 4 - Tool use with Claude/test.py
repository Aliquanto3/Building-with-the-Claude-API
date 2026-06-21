import unittest
from main import greeting, calculate_pi_5_digits
from io import StringIO
import sys


class TestMainFunctions(unittest.TestCase):
    """Test suite for main.py functions"""
    
    def test_greeting(self):
        """Test that greeting() prints 'Hi there!'"""
        captured_output = StringIO()
        sys.stdout = captured_output
        greeting()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Hi there!")
    
    def test_calculate_pi_5_digits_returns_float(self):
        """Test that calculate_pi_5_digits returns a float"""
        result = calculate_pi_5_digits()
        self.assertIsInstance(result, float)
    
    def test_calculate_pi_5_digits_correct_value(self):
        """Test that calculate_pi_5_digits returns approximately 3.14159"""
        result = calculate_pi_5_digits()
        expected = 3.14159
        self.assertEqual(result, expected)
    
    def test_calculate_pi_5_digits_in_correct_range(self):
        """Test that pi is within expected range"""
        result = calculate_pi_5_digits()
        self.assertGreater(result, 3.14)
        self.assertLess(result, 3.15)
    
    def test_calculate_pi_5_digits_has_5_decimal_places(self):
        """Test that the result has 5 decimal places"""
        result = calculate_pi_5_digits()
        result_str = f"{result:.5f}"
        # Count decimal places
        decimal_places = len(result_str.split('.')[1])
        self.assertEqual(decimal_places, 5)


if __name__ == '__main__':
    unittest.main()
