MAIN=src/main.py
TEST=test/test_alg.py
SOURCES=src/*.py

all:
	python3 $(MAIN) 

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black $(SOURCES)

lint:
	pylint --disable=R,C $(SOURCES)

test:
	python3 -m pytest -vv --cov=alg $(TEST)

build: install format lint

