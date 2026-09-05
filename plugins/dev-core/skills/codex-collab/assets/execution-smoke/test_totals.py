import unittest

from totals import total_cents


class TotalCentsTests(unittest.TestCase):
    def test_empty_lines_total_zero(self):
        self.assertEqual(total_cents([]), 0)

    def test_quantity_defaults_to_one(self):
        self.assertEqual(
            total_cents([{"unit_price_cents": 250}, {"unit_price_cents": 175}]),
            425,
        )


if __name__ == "__main__":
    unittest.main()
