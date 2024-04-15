from prometheus_client import Gauge

class GaugeStore():
    def __init__(self, tags):
        self.gauges = {}
        self.tags = tags

    def gauge(self, metric, tag, value, gauge):
        print(self.gauges)
        print(f"adding {metric}   with  {tag}")
        if f"{metric}" not in self.gauges:
            self.gauges[f"{metric}"] = Gauge(f"{metric}", "This is a gauge metric", self.tags)  
        g = self.gauges[f"{metric}"]
        labels = {
            tag: "" for tag in self.tags
        }
        labels[tag] = value
        
        g.labels(
            **labels
        ).set(gauge)