import pytest
from cost_store import DictMetricsStore

@pytest.fixture
def metrics_store():
    return DictMetricsStore()

def test_add_metric(metrics_store):
    # Add a metric
    metrics_store.add_metric('tag1', 10.5, 'metric1')
    
    # Check if metric was added correctly
    assert metrics_store.get_metrics('tag1')['metric1'] == 10.5

def test_get_metrics(metrics_store):
    # Add metrics
    metrics_store.add_metric('tag1', 10.5, 'metric1')
    metrics_store.add_metric('tag1', 20.5, 'metric2')
    metrics_store.add_metric('tag2', 30.5, 'metric1')
    
    # Check if metrics are retrieved correctly
    assert metrics_store.get_metrics('tag1') == {'metric1': 10.5, 'metric2': 20.5}
    assert metrics_store.get_metrics('tag2') == {'metric1': 30.5}

def test_repr(metrics_store):
    # Add metrics
    metrics_store.add_metric('tag1', 10.5, 'metric1')
    metrics_store.add_metric('tag1', 20.5, 'metric2')
    metrics_store.add_metric('tag2', 30.5, 'metric1')
    
    # Check if __repr__ method returns the correct string representation
    expected_repr = "tag1 metric1 10.5\ntag1 metric2 20.5\ntag2 metric1 30.5\n"
    assert repr(metrics_store) == expected_repr
