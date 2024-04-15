from aws_cost_explorer import AwsCostExplorer
from cost_store import DictMetricsStore
from prometheus_client import Gauge, generate_latest, REGISTRY
from flask import Flask, Response

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from gauge_store import GaugeStore
app = Flask(__name__)

metrics_store = DictMetricsStore()
cost_explorer = AwsCostExplorer(metrics_store, ["team", "customer"])
gauge_store = GaugeStore(["team", "customer"])

@app.route("/metrics/")
def metrics():
    for metric, tag, value, gauge in metrics_store.list_metrics():
        gauge_store.gauge(metric, tag, value, gauge)
        
    return Response(
        generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8"
    )

@app.route("/health")
def health():
    return "OK"

scheduler = BackgroundScheduler()

if __name__ == "__main__":

    scheduler.start()    
    scheduler.add_job(
        func=cost_explorer.get_daily_costs,
        trigger=IntervalTrigger(seconds=10),
        id="get_daily_costs",
        name="Get daily costs",
        replace_existing=True,
    )
    app.run(port=3000)
