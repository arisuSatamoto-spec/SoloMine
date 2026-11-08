import unittest

from reward_math import split_reward


class RewardMathTests(unittest.TestCase):
    def test_typical_reward(self):
        self.assertEqual(split_reward(320_000_000), (313_600_000, 6_400_000))

    def test_zero(self):
        self.assertEqual(split_reward(0), (0, 0))

    def test_satoshi_rounding(self):
        self.assertEqual(split_reward(49), (49, 0))
        self.assertEqual(split_reward(50), (49, 1))
        self.assertEqual(split_reward(99), (98, 1))

    def test_conservation(self):
        for amount in (1, 49, 50, 99, 101, 312_500_000, 21_000_000 * 100_000_000):
            miner, developer = split_reward(amount)
            self.assertEqual(miner + developer, amount)
            self.assertGreaterEqual(miner, 0)
            self.assertGreaterEqual(developer, 0)

    def test_reject_invalid(self):
        for value in (-1, 21_000_000 * 100_000_000 + 1):
            with self.assertRaises(ValueError):
                split_reward(value)
        for value in (3.2, "100", True, None):
            with self.assertRaises(TypeError):
                split_reward(value)


if __name__ == "__main__":
    unittest.main()
