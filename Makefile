all: clean lint fmt test

# See https://www.gnu.org/software/make/manual/make.html

clean:
	rm -fr htmlcov .mypy_cache .pytest_cache .ruff_cache .coverage coverage.xml
	hatch env remove unit
	hatch env remove default

dev:
	pip3 install hatch
	hatch env create
	hatch run pip install -e '.[test]'
	hatch run which python
	curl https://www.antlr.org/download/antlr-4.13.1-complete.jar -o .venv/antlr.jar

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

$(PARSERS)/g4/generated/LexBasic.py: $(PARSERS)/g4/LexBasic.g4
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

$(PARSERS)/g4/generated/ANTLRv4Lexer.py: $(PARSERS)/g4/ANTLRv4Lexer.g4 $(PARSERS)/g4/generated/LexBasic.py
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp
	@echo "..adaptor import LexerAdaptor\n__all__ = ['LexerAdaptor']" >> $(PARSERS)/g4/generated/LexerAdaptor.py

$(PARSERS)/g4/generated/ANTLRv4Parser.py: $(PARSERS)/g4/ANTLRv4Parser.g4
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

$(PARSERS)/g4/generate_visitor.py: \
	$(PARSERS)/g4/generated/LexBasic.py \
	$(PARSERS)/g4/generated/ANTLRv4Lexer.py \
	$(PARSERS)/g4/generated/ANTLRv4Parser.py

clean-g4:
	rm -fr $(PARSERS)/g4/generated

$(PARSERS)/tsql/generated/TSqlLexer.py: $(PARSERS)/tsql/TSqlLexer.g4
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

$(PARSERS)/tsql/generated/TSqlParser.py: $(PARSERS)/tsql/TSqlParser.g4
	@$(ANTLR) -o $(dir $@) $<
	@rm $(basename $@).interp

$(PARSERS)/tsql/ast.py: \
	$(PARSERS)/tsql/generated/TSqlLexer.py \
	$(PARSERS)/tsql/generated/TSqlParser.py \
	$(PARSERS)/g4/generate_visitor.py
	hatch run python $(PARSERS)/g4/generate_visitor.py $(PARSERS)/tsql/TSqlParser.g4
	hatch run lint:fmt $(PARSERS)/tsql/ast.py $(PARSERS)/tsql/visitor.py

tsql: $(PARSERS)/tsql/ast.py

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

IR = src/databricks/labs/remorph/intermediate

$(IR)/proto/spark/connect:
	sh src/databricks/labs/remorph/intermediate/download.sh

intermediate: proto $(IR)/proto/spark/connect
	echo done

parsers: tsql
	echo done