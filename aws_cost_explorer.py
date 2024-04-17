from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from utils import dict_orthogonal_product as get_dict_product
from utils import DefaultLogger

import boto3

class AbstractCostExplorer(ABC):

    @abstractmethod
    def get_daily_costs(self):
        pass


class AwsCostExplorer(AbstractCostExplorer):
    def __init__(self, metrics_store, service_tag_map_lists, logger=None):
        """_summary_

        Args:
            metrics_store (_type_): _description_
            service_tag_map_lists (dict(dict(list))): _description_
        """
        self.client = boto3.client("ce")
        self.metrics_store = metrics_store
        self.logger = logger or DefaultLogger()
        self.service_tags = {}
        for service in service_tag_map_lists:
            self.service_tags[service] = get_dict_product(
                service_tag_map_lists[service]
            )

        # let's log the total number of filters which apparently is going to equal to the total number of requests
        count = 0
        for service in self.service_tags:
            for _ in self.service_tags[service]:
                count += 1
        self.logger.info(f"Total number of filters: {count}")

    def get_last_cost_and_usage(self, **kwargs):
        kwargs["TimePeriod"] = {
            "Start": (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "End": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
        }
        return self.client.get_cost_and_usage(**kwargs)

    @staticmethod
    def __get_aws_filters(aws_service, tag_map):
        filter = {
            "And": [
                {"Tags": {"Key": f"{tag}", "Values": [f"{value}"]}}
                for tag, value in tag_map.items()
                if value != ""
            ]
        }

        filter["And"].append(
            {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [f"{aws_service}"],
                    "MatchOptions": ["EQUALS"],
                }
            }
        )
        return filter

    def get_daily_costs(self):
        count = 0
        for aws_service in self.service_tags:
            for tag_map in self.service_tags[aws_service]:
                count += 1
                f = self.__get_aws_filters(aws_service, tag_map)
                resp = self.get_last_cost_and_usage(
                    Granularity="DAILY",
                    Metrics=["BlendedCost"],
                    Filter=f,
                )
                extended_tag_map = tag_map.copy()
                extended_tag_map["aws_service"] = aws_service
                self.metrics_store.gauge(
                    "BlendedCost",
                    extended_tag_map,
                    resp["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"],
                )
        print(f"Total number of requests: {count}")
