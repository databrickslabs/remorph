all: clean dev fmt lint test

clean:
	rm -fr .venv clean htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml .python-version

setup_pyenv:
	@echo "You have selected pyenv setup. It will install pyenv on your system."
	brew list pyenv &>/dev/null || brew install pyenv
	pyenv install -s 3.10
	pyenv init - | grep PATH | tail -1
	@echo "Append the above line (export PATH...) to your profile i.e ~/.zshrc or ~/.bash_profile or ~/.profile and resource your profile for the changes in PATH variable to take effect."


dev_with_pyenv:
	pyenv local 3.10
	pip install --upgrade pip
	pip install hatch
	hatch env create
	hatch run pip install --upgrade pip
	hatch run pip install -e '.[test]'
	hatch run which python
	@echo "Hatch has created the above virtual environment. Please activate it using 'source .venv/bin/activate' and also select the .venv/bin/python interpreter in your IDE."

dev:
	hatch env create
	hatch run pip install --upgrade pip
	hatch run pip install -e '.[test]'
	hatch run which python
	@echo "Hatch has created the above virtual environment. Please activate it using 'source .venv/bin/activate' and also select the .venv/bin/python interpreter in your IDE."

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
