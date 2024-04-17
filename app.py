from aws_cost_explorer import AwsCostExplorer
from prometheus_client import generate_latest
from flask import Flask, Response

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from gauge_store import GaugeStore
from retry import retry

import requests
import json
import os

app = Flask(__name__)

mode = os.environ.get("MODE", "cost_provisioning")
tags_discovery_url = os.environ.get("TAGS_DISCOVERY_URL", "http://localhost:3000")
tags_discovery_url = os.path.join(tags_discovery_url, "service_tags")

@retry(
        attempts=10,
        max_delay=40,
    )
def get_tags_for_services():
    response = requests.get("http://localhost:3000/service_tags")
    return json.loads(response.text)

if mode == "cost_provisioning":
    
    # let's perform a post request to the /service_tags endpoint to get the services with tags
    services_with_tags = get_tags_for_services()
    
    gauge_store = GaugeStore(["team", "service", "aws_service"])
    cost_explorer = AwsCostExplorer(
        gauge_store,
        services_with_tags,
    )

    @app.route("/metrics/")
    def metrics():
        return Response(
            generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8"
        )

    @app.route("/trigger")
    def trigger():
        cost_explorer.get_daily_costs()
        return Response("Triggered", mimetype="text/plain")

    scheduler = BackgroundScheduler()

    scheduler.start()
    scheduler.add_job(
        func=cost_explorer.get_daily_costs,
        trigger=IntervalTrigger(hours=24),
        id="get_daily_costs",
        name="Get daily costs",
        replace_existing=True,
)

if mode == "tag_procisioning":

    from get_tag_grouping import get_services_for_tags
    import json
    import boto3

    tagging_client = boto3.client("resourcegroupstaggingapi")
    tag_list = ["team", "service"]
    services_with_tags = get_services_for_tags(tag_list, tagging_client)

    @app.route("/service_tags")
    def service_tags():
        return Response(json.dumps(services_with_tags), mimetype="text/plain")


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    cost_explorer.get_daily_costs()
