import pytest
from unittest.mock import MagicMock, patch
from prometheus_client import Gauge

from gauge_store import GaugeStore


@pytest.fixture
def mock_gauge():
    return MagicMock(spec=Gauge)


def test_gauge_initialization():
    store = GaugeStore()
    assert store.gauges == {}

@patch("gauge_store.Gauge")
def test_gauge(mock_gauge):
    mocked_gauge_instance = MagicMock()
    mock_gauge.return_value = mocked_gauge_instance
    store = GaugeStore()
    tag_map = {"tag1": "value1", "tag2": "value2"}
    store.gauge("TestMetric", tag_map, 10)
    assert "TestMetric" in store.gauges
    mocked_gauge_instance.labels.assert_called_once_with(tag1="value1", tag2="value2")
    mocked_gauge_instance.labels().set.assert_called_once_with(10)

@patch("gauge_store.generate_latest")
def test_generate_latest(mocked_generate_latest):
    store = GaugeStore()
    store.generate_latest()
    mocked_generate_latest.assert_called_once()
