all: clean dev fmt lint test

clean:
	rm -fr .venv clean htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml

dev:
	pip3 install hatch
	hatch env create
	hatch run pip install -e '.[test]'
	hatch run which python

lint:
	hatch run verify

fmt: fmt-python fmt-scala

fmt-python:
	hatch run fmt

fmt-scala:
	mvn -f pom.xml scalafmt:format

test: test-python test-scala

test-python:
	hatch run test

test-scala:
	mvn test -f pom.xml

integration:
	hatch run integration

coverage:
	hatch run coverage && open htmlcov/index.html

dialect_coverage_report:
	hatch run python src/databricks/labs/remorph/coverage/remorph_snow_transpilation_coverage.py
	hatch -e sqlglot-latest run python src/databricks/labs/remorph/coverage/sqlglot_snow_transpilation_coverage.py
