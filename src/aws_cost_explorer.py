from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from utils import DefaultLogger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import boto3

class AbstractCostExplorer(ABC):

    @abstractmethod
    def get_daily_costs(self):
        pass
    
    @abstractmethod
    def run_on(self, hour=None, minute=None):
        pass


class AwsCostExplorer(AbstractCostExplorer):
    def __init__(self, metrics_store, tags_provider, logger=None):
        self.client = boto3.client("ce")
        self.aws_blending_cost = AWSBlendingCostExplorer(self.client)
        self.metrics_store = metrics_store
        self.tags_provider_client = tags_provider
        self.logger = logger or DefaultLogger()

    def get_daily_costs(self):
        service_tags = self.tags_provider_client.get_service_tags()
        for aws_service in service_tags:
            for tag_map in service_tags[aws_service]:
                cost = self.aws_blending_cost.get_costs_for(aws_service, tag_map)
                
                extended_tag_map = tag_map.copy()
                extended_tag_map["aws_service"] = aws_service
                self.metrics_store.gauge(
                    "BlendedCost",
                    extended_tag_map,
                    cost,
                )
                
            # TODO: Remove this break statement
            break
        self.metrics_store.persist()
        
    def run_on(self, hour=None, minute=None):
        hour = hour or 23
        minute = minute or 10
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.scheduler.add_job(
            func=self.get_daily_costs,
            trigger=CronTrigger(hour=hour, minute=minute),
            id="get_daily_costs",
            name="Get daily costs",
            replace_existing=True,
        )



class AWSBlendingCostExplorer:
        
    def __init__(self, ce_client):
        self.client = ce_client

    @staticmethod
    def _get_aws_filters(aws_service, tag_map):
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
    
    def _get_last_cost_and_usage(self, **kwargs):
        kwargs["TimePeriod"] = {
            "Start": (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "End": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
        }
        return self.client.get_cost_and_usage(**kwargs)
    
    
    def get_costs_for(self, aws_service, tag_map):
        f = self._get_aws_filters(aws_service, tag_map)
        resp = self._get_last_cost_and_usage(
            Granularity="DAILY",
            Metrics=["BlendedCost"],
            Filter=f,
        )
        return resp["ResultsByTime"][0]["Total"]["BlendedCost"]["Amount"]
    

 
    