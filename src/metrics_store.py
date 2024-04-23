from collections import defaultdict
from abc import ABC, abstractmethod
from hashlib import md5
from utils import DefaultLogger
import json

class AbstractMetricsStore(ABC):
    
    @abstractmethod
    def gauge(self, metric, tag_map, gauge):
        """Add a new metrics to the store.

        Args:
            tag (string): the tag
            value (string): the value of the tag
            metric (string): the metric to add
        """
        pass
    
    @abstractmethod
    def list_gauges(self):
        """List all the gauges in the store.

        Returns:
            list: a list of tuples containing the metric, tag_map and gauge
        """
        pass
    
    def persist(self):
        """Persist the data to a file."""
        pass


class DictMetricsStore(AbstractMetricsStore):
    def __init__(self, persistent_file=None, logger=None):
        self.logger = logger or DefaultLogger()
        self.persistent_file = persistent_file
        self.gauge_store = defaultdict(defaultdict)
        # let's load the data from the file
        try:
            with open(self.persistent_file, "r") as f:
                self.gauge_store = json.loads((f.read()))
        except FileNotFoundError:
            print("File not found, creating a new one")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        
    @classmethod
    def format_string(cls, string):
        return string.lower().replace(" ", "_").replace("-", "_")
    
    @staticmethod
    def get_hash(tag_map):
        # let's concatenate all tags and values and hash them
        concatenated = ""
        for tag, value in tag_map.items():
            concatenated += f"{tag}{value}"
        hashed = md5(concatenated.encode("utf-8"))
        return hashed.digest()

    def gauge(self, metric, tag_map, gauge):
        metric = self.format_string(metric)
        self.gauge_store[metric][self.get_hash(tag_map)] = (tag_map, gauge)
        
    def list_gauges(self):
        for metric in self.gauge_store:
            for (tag_map, gauge) in self.gauge_store[metric].values():
                yield metric, tag_map, gauge
                
    def persist(self):
        # in case there is no file to perish the data just return
        if not self.persistent_file:
            self.logger.debug("No file to persist the data")
            return
        # should persist the data to a file
        with open(self.persistent_file, "w") as f:
            # let's decode all keys to strings
            for key in self.gauge_store.keys():
                self.gauge_store[key] = {
                    str(k): v for k, v in self.gauge_store[key].items()}
            f.write(json.dumps(self.gauge_store))
            # let's encode back
            for key in self.gauge_store.keys():
                self.gauge_store[key] = {
                    bytes(k, "utf-8"): v for k, v in self.gauge_store[key].items()}
            self.logger.debug("Data persisted to file")