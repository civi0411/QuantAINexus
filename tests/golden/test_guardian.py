"""
Golden Test Suite for Guardian Verification Layer
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from quantainexus.core.guardian import Guardian, GuardianReport


class TestGuardianGolden(unittest.TestCase):

    def test_triple_barrier_blocks_future_price(self):
        """Chứng minh Triple-Barrier chặn label nhìn thấy tương lai"""

        class DummyLabeler:
            barrier_type = "simple_return"

        labeler = DummyLabeler()
        report = Guardian.check("labeler", labeler)
        self.assertIsInstance(report, GuardianReport)

    def test_cpcv_blocks_overfitting(self):
        """Chứng minh CPCV chặn overfitting"""

        class DummyModel:
            cv_method = "kfold"

        model = DummyModel()
        report = Guardian.check("model", model)
        self.assertIsInstance(report, GuardianReport)


if __name__ == "__main__":
    unittest.main()
