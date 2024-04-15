import boto3
from datetime import datetime, timedelta
from collections import defaultdict
from abc import ABC, abstractmethod


class AbstractCostExplorer(ABC):
    
    @abstractmethod
    def get_daily_costs(self):
        pass


    @abstractmethod
    def get_daily_usages(self):
        pass


class AwsCostExplorer(AbstractCostExplorer):
    def __init__(self, metrics_store, tag_list):
        self.client = boto3.client("ce")
        self.metrics_store = metrics_store
        self.tag_values = defaultdict(list)
        for tag in tag_list:
            tag_values = self.client.get_tags(
                TimePeriod={
                    "Start": (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 
                    "End":  datetime.now().strftime("%Y-%m-%d"),
                }, TagKey=tag
            ).get("Tags", [])
            self.tag_values[tag] = tag_values
        
    def get_last_cost_and_usage(self, **kwargs):
        kwargs["TimePeriod"] = {
            "Start": (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"), 
            "End": datetime.now().strftime("%Y-%m-%d")
        }
        return self.client.get_cost_and_usage(**kwargs)


    def get_daily_costs(self):
        for tag, values in self.tag_values.items():
            for value in values:
                resp = self.get_last_cost_and_usage(
                    Granularity="DAILY",
                    Metrics=["BlendedCost"],
                    Filter={  
                        "Tags": {
                            "Key": tag,
                            "Values": [value]
                        }
                    }
                )
                self.metrics_store.add_metric(tag, value, "BlendedCost", resp["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"])

    def get_daily_usages(self):
        usages = self.get_last_cost_and_usage(
            Granularity="DAILY",
            Metrics=["BlendedCost"],
            Filter={  
                "Tags": {
                    "Key": "team",
                    "Values": ["infrastructure"]
                }
            }
        )["ResultsByTime"][0]["Total"]["UsageQuantity"]["Amount"]
        return usages
