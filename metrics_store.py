from collections import defaultdict
from abc import ABC, abstractmethod


class AbstractMetricsStore(ABC):
    
    @abstractmethod
    def add_metric(self, metric, tag, value, gauge):
        """Add a new metrics to the store.

        Args:
            tag (string): the tag
            value (string): the value of the tag
            metric (string): the metric to add
        """
        pass


class DictMetricsStore(AbstractMetricsStore):
    def __init__(self) -> None:
        self.store = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        
    @classmethod
    def format_string(cls, string):
        return string.lower().replace(" ", "_").replace("-", "_")

    def add_metric(self, tag, value, metric, gauge):
        tag = self.format_string(tag)
        metric = self.format_string(metric)
        value = self.format_string(value)
        self.store[metric][tag][value] = gauge
        
    def list_metrics(self):
        for metric in self.store:
            for tag in self.store[metric]:
                for tag_value in self.store[metric][tag]:
                    yield metric, tag, tag_value, self.store[metric][tag][tag_value]