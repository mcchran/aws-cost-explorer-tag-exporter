.PHOBY: setup run test run-cost-exporter run-tag-exporter

setup:
	pip install -r requirements.txt > /dev/null

test: setup
	python -m pytest

run-cost-exporter: setup
	FLASK_APP=app.py && MODE=cost_provisioning flask run --host 0.0.0.0 --port 3001

run-tag-exporter: setup
	FLASK_APP=app.py && MODE=tag_provisioning flask run --host  0.0.0.0 --port 3000
