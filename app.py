from aws_cost_explorer import AwsCostExplorer
from metrics_store import DictMetricsStore
from prometheus_client import generate_latest
from flask import Flask, Response

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from gauge_store import GaugeStore

app = Flask(__name__)

gauge_store = GaugeStore(["team", "service"])
cost_explorer = AwsCostExplorer(gauge_store, ["team", "service"])


@app.route("/metrics/")
def metrics():
    return Response(
        generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8"
    )


@app.route("/trigger")
def trigger():
    cost_explorer.get_daily_costs()
    return Response("Triggered", mimetype="text/plain")


@app.route("/health")
def health():
    return "OK"


scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(
#     func=cost_explorer.get_daily_costs,
#     trigger=IntervalTrigger(hours=1),
#     id="get_daily_costs",
#     name="Get daily costs",
#     replace_existing=True,
# )
