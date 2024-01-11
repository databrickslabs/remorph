all: clean lint fmt test

clean:
	rm -fr htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml
	hatch env remove unit

dev:
	pip3 install hatch
	hatch env create
	hatch run pip install -e '.[test]'
	hatch run which python

lint:
	hatch run verify

fmt:
	hatch run fmt

test:
	hatch run test

integration:
	hatch run integration:test

coverage:
	hatch run coverage && open htmlcov/index.html

