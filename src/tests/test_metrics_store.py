from unittest.mock import MagicMock, patch
import pytest

from metrics_store import DictMetricsStore


@pytest.fixture
def mock_default_logger():
    return MagicMock()


@pytest.fixture
def mock_open():
    with patch("builtins.open") as mock_opn:
        yield mock_opn


def test_format_string():
    assert DictMetricsStore.format_string("Test Metric Name") == "test_metric_name"
    assert DictMetricsStore.format_string("Another-Metric") == "another_metric"


def test_get_hash():
    tag_map = {"tag1": "value1", "tag2": "value2"}
    expected_hash = b"\xc1\x13\xa2\xe9u\xa0\xe1\xc1\xba\xf5\n@s\xde-F"
    assert DictMetricsStore.get_hash(tag_map) == expected_hash


def test_gauge(mock_default_logger):
    store = DictMetricsStore(logger=mock_default_logger)
    tag_map = {"tag1": "value1", "tag2": "value2"}
    store.gauge("Test Metric", tag_map, 10)

    assert dict(store.gauge_store) == {
        "test_metric": {
            b'\xc1\x13\xa2\xe9u\xa0\xe1\xc1\xba\xf5\n@s\xde-F': (
                {"tag1": "value1", "tag2": "value2"},
                10,
            )
        }
    }


def test_list_gauges(mock_default_logger):
    store = DictMetricsStore(logger=mock_default_logger)
    tag_map = {"tag1": "value1", "tag2": "value2"}
    store.gauge("Test Metric", tag_map, 10)

    gauges = list(store.list_gauges())

    assert gauges == [("test_metric", {"tag1": "value1", "tag2": "value2"}, 10)]


def test_persist(mock_default_logger, mock_open):
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    store = DictMetricsStore(persistent_file="test.json", logger=mock_default_logger)
    store.gauge("Test Metric", {"tag1": "value1", "tag2": "value2"}, 10)
    store.persist()

    mock_file.write.assert_called_once()
    mock_default_logger.debug.assert_called_once_with("Data persisted to file")
