all: clean lint fmt test

antlr:
	wget https://www.antlr.org/download/antlr-4.13.1-complete.jar -o .venv/antlr.jar

clean:
	rm -fr htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml
	hatch env remove unit

dev:
	curl https://www.antlr.org/download/antlr-4.13.1-complete.jar -o .venv/antlr.jar
	pip3 install hatch
	hatch env create
	hatch run pip install -e '.[test]'
	hatch run which python

lint:
	hatch run lint:verify

fmt:
	hatch run lint:fmt

test:
	hatch run unit:test

integration:
	hatch run integration:test

coverage:
	hatch run unit:test-cov-report && open htmlcov/index.html

