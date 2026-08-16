import unittest
import pandas as pd

from quantainexus.ports.data import DataEnvelope, QNXDataset
from quantainexus.core.engine.context import PipelineContext
from quantainexus.core.guardian.checks.schema import SchemaValidator
from quantainexus.core.registry import Registry, register
from quantainexus.core.utils.exceptions import PluginNotFoundError


class TestRegistryAndSchema(unittest.TestCase):

    def test_registry_register_and_load(self):
        @register("dummy_category", "dummy_plugin")
        class DummyPlugin:
            def __init__(self, x=1):
                self.x = x

        plugin = Registry.build({"type": "dummy_category", "name": "dummy_plugin", "params": {"x": 42}})
        self.assertEqual(plugin.x, 42)

    def test_registry_raises_clear_error_when_plugin_missing(self):
        with self.assertRaises(PluginNotFoundError):
            Registry.get("dummy_category", "khong_ton_tai")

    def test_schema_validator_blocks_missing_required_column(self):
        df = pd.DataFrame({"open": [1], "high": [1], "low": [1]})  # thiếu close, volume
        envelope = DataEnvelope(schema_version="1.0.0", data_type="ohlcv", frequency="1d",
                                 point_in_time=False, source="test", checksum="dummy", generated_at="2026-01-01")
        dataset = QNXDataset(data=df, envelope=envelope)
        ctx = PipelineContext(datasets={"dataloader": dataset})
        result = SchemaValidator().run(ctx, "dataloader")
        self.assertFalse(result.passed)

    def test_schema_validator_blocks_point_in_time_true_without_field(self):
        df = pd.DataFrame({"metric": ["eps"], "value": [1.0]})   # thiếu as_of_date
        envelope = DataEnvelope(schema_version="1.0.0", data_type="fundamental", frequency="quarterly",
                                 point_in_time=True, source="test", checksum="dummy", generated_at="2026-01-01")
        dataset = QNXDataset(data=df, envelope=envelope)
        ctx = PipelineContext(datasets={"dataloader": dataset})
        result = SchemaValidator().run(ctx, "dataloader")
        self.assertFalse(result.passed)

    def test_schema_validator_passes_valid_ohlcv(self):
        df = pd.DataFrame({"open": [1], "high": [1], "low": [1], "close": [1], "volume": [100]})
        envelope = DataEnvelope(schema_version="1.0.0", data_type="ohlcv", frequency="1d",
                                 point_in_time=False, source="test", checksum="dummy", generated_at="2026-01-01")
        dataset = QNXDataset(data=df, envelope=envelope)
        ctx = PipelineContext(datasets={"dataloader": dataset})
        result = SchemaValidator().run(ctx, "dataloader")
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
