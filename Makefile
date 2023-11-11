all: clean lint fmt test


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

.venv/antlr.jar:
	curl https://www.antlr.org/download/antlr-4.13.1-complete.jar -o .venv/antlr.jar

ANTLR = java -jar .venv/antlr.jar \
		-Dlanguage=Python3 \
		-Xexact-output-dir \
		-no-listener \
		-visitor

PARSERS = src/databricks/labs/remorph/parsers

src/databricks/labs/remorph/parsers/g4/ANTLRv4Lexer.py: src/databricks/labs/remorph/parsers/g4/ANTLRv4Lexer.g4
	$(ANTLR) \
		-o src/databricks/labs/remorph/parsers/g4 \
		src/databricks/labs/remorph/parsers/g4/ANTLRv4Lexer.g4
	rm src/databricks/labs/remorph/parsers/g4/*.interp

src/databricks/labs/remorph/parsers/g4/ANTLRv4Parser.py: src/databricks/labs/remorph/parsers/g4/ANTLRv4Parser.g4
	$(ANTLR) \
		-o src/databricks/labs/remorph/parsers/g4 \
		src/databricks/labs/remorph/parsers/g4/ANTLRv4Parser.g4
	rm src/databricks/labs/remorph/parsers/g4/*.interp

src/databricks/labs/remorph/parsers/g4: \
	src/databricks/labs/remorph/parsers/g4/ANTLRv4Lexer.py \
	src/databricks/labs/remorph/parsers/g4/ANTLRv4Parser.py

$(PARSERS)/tsql/generated: .venv/antlr.jar
	@mkdir $@
	@touch $@/__init__.py

$(PARSERS)/tsql/generated/TSqlLexer.py: $(PARSERS)/tsql/TSqlLexer.g4 $(PARSERS)/tsql/generated
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

$(PARSERS)/tsql/generated/TSqlParser.py: $(PARSERS)/tsql/TSqlParser.g4 $(PARSERS)/tsql/generated
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

tsql: \
	$(PARSERS)/tsql/generated/TSqlLexer.py \
	$(PARSERS)/tsql/generated/TSqlParser.py
	echo "Generated T-SQL parsers"

clean-tsql:
	rm -fr $(PARSERS)/tsql/generated

# Protobuf parser

$(PARSERS)/proto/generated/Protobuf3Parser.py: $(wildcard $(PARSERS)/proto/*.g4)
	@$(ANTLR) -o $(dir $@) $<
	@rm $(PARSERS)/proto/generated/*.interp

proto: $(PARSERS)/proto/generated/Protobuf3Parser.py
	touch $(PARSERS)/proto/generated/__init__.py

clean-proto:
	rm -fr $(PARSERS)/proto/generated


parsers: tsql
	echo done