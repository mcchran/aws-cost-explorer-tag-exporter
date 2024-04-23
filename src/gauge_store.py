from prometheus_client import Gauge, generate_latest
class GaugeStore:
    def __init__(self):
        self.gauges = {}

    def gauge(self, metric, tag_map, gauge):
        if f"{metric}" not in self.gauges:
            self.gauges[f"{metric}"] = Gauge(f"{metric}", "This is a gauge metric", list(tag_map.keys()))  
        g = self.gauges[f"{metric}"]
        labels = {
            tag: "" for tag in tag_map.keys()
        }
        for tag, value in tag_map.items():
            labels[tag] = value
        
        g.labels(
            **labels
        ).set(gauge)
        
    def generate_latest(self):
        return generate_latest()