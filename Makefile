.PHOBY: setup run test

setup:
	pip install -r requirements.txt > /dev/null

run: setup
	python main.py

test: setup
	python -m pytest .