.PHONY: install scrape validate build clean all

install:
	pip install -r requirements.txt

scrape:
	python scrapers/gur_war_sanctions.py --out-dir data/ --rate-limit 1.0
	python scrapers/car_field_dispatches.py --out-dir data/

validate:
	python scripts/validate.py

build:
	python scripts/headline_numbers.py
	jupyter nbconvert --to html --execute notebooks/01_component_origin_map.ipynb || true

clean:
	rm -rf .ipynb_checkpoints __pycache__ */__pycache__

all: install scrape validate build
