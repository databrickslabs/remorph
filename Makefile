all: clean dev fmt lint test

clean:
	rm -fr .venv clean htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml

dev:
	hatch env create
	hatch run pip install -e '.[test]'
	hatch run which python

lint:
	hatch run verify

fmt:
	hatch run fmt

setup_spark_remote:
	.github/scripts/setup_spark_remote.sh

test: setup_spark_remote
	hatch run test

integration:
	hatch run integration

coverage:
	hatch run coverage && open htmlcov/index.html

clean_coverage_dir:
	rm -fr ${OUTPUT_DIR}

python_coverage_report:
	hatch run python src/databricks/labs/remorph/coverage/remorph_snow_transpilation_coverage.py
	hatch run pip install --upgrade sqlglot
	hatch -e sqlglot-latest run python src/databricks/labs/remorph/coverage/sqlglot_snow_transpilation_coverage.py
	hatch -e sqlglot-latest run python src/databricks/labs/remorph/coverage/sqlglot_tsql_transpilation_coverage.py

dialect_coverage_report: clean_coverage_dir python_coverage_report
	hatch run python src/databricks/labs/remorph/coverage/local_report.py
