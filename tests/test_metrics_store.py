from metrics_store import DictMetricsStore
import pytest

@pytest.fixture
def metrics_store():
    return DictMetricsStore()

def test_add_metric(metrics_store):
    # Add a metric
    metrics_store.add_metric('tag1', 'value1', 'metric1', 10.5)
    
    # Check if metric was added correctly
    assert metrics_store.store['metric1']['tag1']['value1'] == 10.5

def test_list_metrics(metrics_store):
    # Add metrics
    metrics_store.add_metric('tag1', 'value1', 'metric1', 10.5)
    metrics_store.add_metric('tag2', 'value2', 'metric2', 20.5)
    
    # Get list of metrics
    metrics_list = list(metrics_store.list_metrics())
    
    # Check if the metrics are listed correctly
    assert len(metrics_list) == 2
    assert ('metric1', 'tag1', 'value1', 10.5) in metrics_list
    assert ('metric2', 'tag2', 'value2', 20.5) in metrics_list

def test_format_string():
    # Test format_string method
    assert DictMetricsStore.format_string('Test String') == 'test_string'
    assert DictMetricsStore.format_string('Another-String') == 'another_string'
    assert DictMetricsStore.format_string('Yet Another String') == 'yet_another_string'
