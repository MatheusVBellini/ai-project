MAIN=main.py
TEST=test_alg.py
SOURCES=*.py

all:
	python3 main.py 

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

