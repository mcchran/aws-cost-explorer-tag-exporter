from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timedelta
from utils import get_dict_product

import boto3


class AbstractCostExplorer(ABC):

    @abstractmethod
    def get_daily_costs(self):
        pass


class AwsCostExplorer(AbstractCostExplorer):
    def __init__(self, metrics_store, tag_list):
        self.client = boto3.client("ce")
        self.metrics_store = metrics_store
        self.tag_values = defaultdict(list)

        tag_values_dict = {}
        for tag in tag_list:
            tag_values = self.client.get_tags(
                TimePeriod={
                    "Start": (datetime.today() - timedelta(days=1)).strftime(
                        "%Y-%m-%d"
                    ),
                    "End": datetime.today().strftime("%Y-%m-%d"),
                },
                TagKey=tag,
            ).get("Tags", [])
            tag_values_dict[tag] = tag_values
            self.tag_maps = get_dict_product(tag_values_dict)

    def get_last_cost_and_usage(self, **kwargs):
        kwargs["TimePeriod"] = {
            "Start": (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "End": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
        }
        return self.client.get_cost_and_usage(**kwargs)

    @staticmethod
    def __get_aws_filters(tag_map):
        return {
            "And": [
                {"Tags": {"Key": f"{tag}", "Values": [f"{value}"]}}
                for tag, value in tag_map.items()
            ]
        }

    def get_daily_costs(self):
        for tag_map in self.tag_maps:
            resp = self.get_last_cost_and_usage(
                Granularity="DAILY",
                Metrics=["BlendedCost"],
                Filter=self.__get_aws_filters(tag_map),
            )
            
            self.metrics_store.gauge(
                "BlendedCost",
                tag_map,
                resp["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"],
            )
