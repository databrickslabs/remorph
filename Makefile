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
	mvn validate -Pformat

test: test-python test-scala

setup_spark_remote:
	.github/scripts/setup_spark_remote.sh

test-python: setup_spark_remote
	hatch run test

test-scala:
	mvn test -f pom.xml

integration:
	hatch run integration

coverage:
	hatch run coverage && open htmlcov/index.html

build_core_jar:
	mvn --update-snapshots -B install -DskipTests -pl "!com.databricks.labs:remorph-coverage" --file pom.xml

clean_coverage_dir:
	rm -fr ${OUTPUT_DIR}

python_coverage_report:
	hatch run python src/databricks/labs/remorph/coverage/remorph_snow_transpilation_coverage.py
	hatch run pip install --upgrade sqlglot
	hatch -e sqlglot-latest run python src/databricks/labs/remorph/coverage/sqlglot_snow_transpilation_coverage.py
	hatch -e sqlglot-latest run python src/databricks/labs/remorph/coverage/sqlglot_tsql_transpilation_coverage.py

antlr_coverage_report: build_core_jar
	mvn compile -DskipTests exec:java -pl coverage --file pom.xml -DsourceDir=${INPUT_DIR_PARENT}/snowflake -DoutputPath=${OUTPUT_DIR} -DsourceDialect=Snow -Dextractor=full
	mvn exec:java -pl coverage --file pom.xml -DsourceDir=${INPUT_DIR_PARENT}/tsql -DoutputPath=${OUTPUT_DIR} -DsourceDialect=Tsql -Dextractor=full

dialect_coverage_report: clean_coverage_dir antlr_coverage_report python_coverage_report
	hatch run python src/databricks/labs/remorph/coverage/local_report.py

antlr-coverage: build_core_jar
	echo "Running coverage for snowflake"
	mvn -DskipTests compile exec:java -pl coverage --file pom.xml -DsourceDir=${INPUT_DIR_PARENT}/snowflake -DoutputPath=.venv/antlr-coverage -DsourceDialect=Snow -Dextractor=full
	echo "Running coverage for tsql"
	mvn exec:java -pl coverage --file pom.xml -DsourceDir=${INPUT_DIR_PARENT}/tsql -DoutputPath=.venv/antlr-coverage -DsourceDialect=Tsql -Dextractor=full
	OUTPUT_DIR=.venv/antlr-coverage hatch run python src/databricks/labs/remorph/coverage/local_report.py

antlr-lint:
	mvn compile -DskipTests exec:java -pl linter --file pom.xml -Dexec.args="-i core/src/main/antlr4 -o .venv/linter/grammar -c true"
