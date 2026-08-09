"""Unit tests for the from-scratch sinh implementation (Problem 8).

Run:  python3 -m unittest -v test_sinh
"""

import math
import unittest

import sinh_d3 as s


class TestSinhValues(unittest.TestCase):
    """Accuracy of sinh against the reference math.sinh."""

    def _close(self, x, tol=1e-12):
        self.assertAlmostEqual(
            s.sinh(x), math.sinh(x), delta=tol * max(1.0, abs(math.sinh(x)))
        )

    def test_zero(self):
        self.assertEqual(s.sinh(0), 0.0)

    def test_small_positive(self):
        self._close(0.5)

    def test_one(self):
        self._close(1.0)

    def test_larger(self):
        self._close(10.0)

    def test_hundred(self):
        self._close(100.0)

    def test_near_overflow_boundary(self):
        self._close(700.0)

    def test_tiny(self):
        self._close(1e-8)


class TestOddSymmetry(unittest.TestCase):
    """sinh is odd: sinh(-x) == -sinh(x)."""

    def test_symmetry_integer(self):
        self.assertEqual(s.sinh(-3), -s.sinh(3))

    def test_symmetry_fraction(self):
        self.assertAlmostEqual(s.sinh(-2.5), -s.sinh(2.5), places=12)


class TestOverflow(unittest.TestCase):
    """Values beyond double range raise a clean, typed error."""

    def test_overflow_raises(self):
        with self.assertRaises(s.SinhOverflowError):
            s.sinh(800)

    def test_boundary_still_computes(self):
        # 710.4 is representable; must NOT raise.
        try:
            s.sinh(710.4)
        except s.SinhOverflowError:
            self.fail("sinh(710.4) should compute, not overflow")

    def test_overflow_is_sinherror(self):
        # Custom hierarchy: overflow is a SinhError.
        self.assertTrue(issubclass(s.SinhOverflowError, s.SinhError))


class TestInputParsing(unittest.TestCase):
    """parse_real accepts valid reals and rejects bad input."""

    def test_valid_integer(self):
        self.assertEqual(s.parse_real("42"), 42.0)

    def test_valid_negative_decimal(self):
        self.assertEqual(s.parse_real("  -3.14 "), -3.14)

    def test_letters_raise(self):
        with self.assertRaises(s.SinhInputError):
            s.parse_real("hello")

    def test_empty_raises(self):
        with self.assertRaises(s.SinhInputError):
            s.parse_real("   ")

    def test_input_error_is_sinherror(self):
        self.assertTrue(issubclass(s.SinhInputError, s.SinhError))


class TestAbsoluteHelper(unittest.TestCase):
    """The from-scratch _absolute replaces built-in abs()."""

    def test_positive(self):
        self.assertEqual(s._absolute(5.0), 5.0)

    def test_negative(self):
        self.assertEqual(s._absolute(-5.0), 5.0)

    def test_zero(self):
        self.assertEqual(s._absolute(0.0), 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
