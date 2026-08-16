"""Golden tests — bằng chứng Guardian Layer THỰC SỰ chặn được leakage.

Đây là bộ test quan trọng nhất của toàn bộ framework: lời hứa "anti-leakage bắt
buộc" chỉ có giá trị nếu có test chứng minh nó hoạt động.
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pandas as pd

from quantainexus.nexus import QuantAINexus
from quantainexus.ports.data import DataEnvelope, QNXDataset
from quantainexus.core.engine.context import PipelineContext
from quantainexus.core.guardian.checks.cpcv import CPCVCheck
from quantainexus.core.guardian.checks.point_in_time import PointInTimeValidator
from quantainexus.core.guardian.checks.triple_barrier import TripleBarrierCheck


def _base_pipeline_def(**config_overrides):
    return {
        "loader": {"name": "synthetic_ohlcv", "kwargs": {
            "symbols": ["VNM"], "start": "2023-01-01", "end": "2024-06-30", "seed": 42
        }},
        "factor": {"name": "momentum", "init_kwargs": {"window": 10}},
        "labeler": {"name": "triple_barrier", "init_kwargs": {"horizon": 5}},
        "model": {"name": "random_forest"},
        "strategy": {"name": "direct_signal"},
        "execution": {"name": "simple_fill"},
        "backtest": {"name": "vectorized"},
        "feature_cols": ["momentum"],
        "label_col": "label",
        "config": {
            "cost_bps": 15, "max_factor_lookback": 10, "barrier_horizon": 5,
            "cpcv_purge": 10, "fracdiff_approved": True,
            **config_overrides,
        },
    }


class TestGuardianBlocksLeakage(unittest.TestCase):

    def test_full_pipeline_completes_with_valid_config(self):
        qnx = QuantAINexus()
        ctx = qnx.run_pipeline(_base_pipeline_def())
        self.assertEqual(ctx.status, "completed")
        self.assertIn("sharpe", ctx.scratch["backtest_result"])

    def test_fractional_diff_pauses_for_veto_when_not_approved(self):
        qnx = QuantAINexus()
        pdef = _base_pipeline_def()
        del pdef["config"]["fracdiff_approved"]
        ctx = qnx.run_pipeline(pdef)
        self.assertEqual(ctx.status, "paused_for_veto")
        self.assertTrue(any(r.check_name == "FractionalDiffCheck" and not r.passed for r in ctx.guardian_reports))

    def test_cpcv_blocks_when_purge_smaller_than_lookback(self):
        qnx = QuantAINexus()
        pdef = _base_pipeline_def(cpcv_purge=2)   # nhỏ hơn max(lookback=10, horizon=5)
        ctx = qnx.run_pipeline(pdef)
        self.assertEqual(ctx.status, "failed")
        self.assertTrue(any(r.check_name == "CPCVCheck" and not r.passed for r in ctx.guardian_reports))

    def test_transaction_cost_blocks_when_cost_is_zero(self):
        qnx = QuantAINexus()
        pdef = _base_pipeline_def(cost_bps=0)
        ctx = qnx.run_pipeline(pdef)
        self.assertEqual(ctx.status, "failed")
        self.assertTrue(any(r.check_name == "TransactionCostValidator" and not r.passed for r in ctx.guardian_reports))

    def test_point_in_time_blocks_future_restatement(self):
        df = pd.DataFrame([
            {"symbol": "VNM", "period_end": pd.Timestamp("2024-01-01"),
             "as_of_date": pd.Timestamp("2026-01-01"), "metric": "eps", "value": 2.1},
        ]).set_index(["symbol", "period_end", "as_of_date"])
        envelope = DataEnvelope(
            schema_version="1.0.0", data_type="fundamental", frequency="quarterly",
            point_in_time=True, source="test", checksum="dummy", generated_at="2026-01-01",
        )
        ctx = PipelineContext(run_id="test", config={"as_of": "2025-01-01"})
        ctx.datasets["load_data"] = QNXDataset(data=df, envelope=envelope)

        result = PointInTimeValidator().run(ctx, "load_data")
        self.assertFalse(result.passed)

    def test_point_in_time_passes_when_all_data_available_in_time(self):
        df = pd.DataFrame([
            {"symbol": "VNM", "period_end": pd.Timestamp("2024-01-01"),
             "as_of_date": pd.Timestamp("2024-03-01"), "metric": "eps", "value": 2.1},
        ]).set_index(["symbol", "period_end", "as_of_date"])
        envelope = DataEnvelope(
            schema_version="1.0.0", data_type="fundamental", frequency="quarterly",
            point_in_time=True, source="test", checksum="dummy", generated_at="2026-01-01",
        )
        ctx = PipelineContext(run_id="test", config={"as_of": "2025-01-01"})
        ctx.datasets["load_data"] = QNXDataset(data=df, envelope=envelope)

        result = PointInTimeValidator().run(ctx, "load_data")
        self.assertTrue(result.passed)

    def test_triple_barrier_check_blocks_when_tail_labels_are_not_nan(self):
        dates = pd.date_range("2024-01-01", periods=20, freq="D")
        df = pd.DataFrame({
            "date": list(dates), "symbol": ["VNM"] * 20,
            "close": range(100, 120), "label": [1] * 20,
        }).set_index(["date", "symbol"])

        ctx = PipelineContext(run_id="test", config={"barrier_horizon": 5})
        ctx.datasets["label_data"] = type("D", (), {"data": df})()

        result = TripleBarrierCheck().run(ctx, "label_data")
        self.assertFalse(result.passed)
        self.assertEqual(result.status, "BLOCK")

    def test_cpcv_check_requires_purge_covering_max_lookback_and_horizon(self):
        ctx = PipelineContext(run_id="test", config={
            "max_factor_lookback": 20, "barrier_horizon": 5, "cpcv_purge": 10, "cpcv_embargo": 2,
        })
        result = CPCVCheck().run(ctx, "train_model")
        self.assertFalse(result.passed)

        ctx.config["cpcv_purge"] = 20
        result = CPCVCheck().run(ctx, "train_model")
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
