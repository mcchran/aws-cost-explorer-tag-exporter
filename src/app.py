from aws_cost_explorer import AwsCostExplorer
from aws_service_tag_exporter import AWSServiceTagExporter
from config import Config
from flask import Flask, Response
from gauge_store import GaugeStore
from tags_provider import HttpTagsProvider
from metrics_store import DictMetricsStore
import json
import os


# let's load the application configuration
appConfig = Config()
app = Flask(__name__)

if appConfig.is_cost_provisioning():
    tags_provider = HttpTagsProvider(os.path.join(appConfig.tags_host, "service_tags"))
    persistent_gauge_store = DictMetricsStore(
        persistent_file=appConfig.persistent_file_path
    )
    cost_explorer = AwsCostExplorer(
        persistent_gauge_store,
        tags_provider,
    )
    cost_explorer.run_on(appConfig.schedule_minute, appConfig.schedule_minute)

    gauge_store = GaugeStore()

    @app.route("/metrics/")
    def metrics():
        for metric, tag_map, gauge in persistent_gauge_store.list_gauges():
            gauge_store.gauge(metric, tag_map, gauge)
        return Response(
            gauge_store.generate_latest(),
            mimetype="text/plain; version=0.0.4; charset=utf-8",
        )

    @app.route("/trigger")
    def trigger():
        cost_explorer.get_daily_costs()
        return Response("Triggered", mimetype="text/plain")


if appConfig.is_tag_provisioning():

    tag_list = ["team", "service"]
    tag_exporter = AWSServiceTagExporter(appConfig.tags_list)
    services_with_tags = tag_exporter.get_services_for_tags()

    @app.route("/service_tags")
    def service_tags():
        return Response(json.dumps(services_with_tags), mimetype="text/plain")


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    cost_explorer.get_daily_costs()
