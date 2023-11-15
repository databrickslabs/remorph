import pathlib

from databricks.labs.remorph.parsers.base import init_parse
from databricks.labs.remorph.parsers.tsql.ast import TsqlFile
from databricks.labs.remorph.parsers.tsql.generated.TSqlLexer import TSqlLexer
from databricks.labs.remorph.parsers.tsql.generated.TSqlParser import TSqlParser
from databricks.labs.remorph.parsers.tsql.generated.TSqlParserVisitor import TSqlParserVisitor
from databricks.labs.remorph.parsers.tsql.visitor import TSqlAST


def parse_tsql(path: pathlib.Path) -> TsqlFile:
    return init_parse(path, TSqlLexer, TSqlParser, TSqlAST, "tsql_file")

def parse_tsql_dummy(path: pathlib.Path):
    return init_parse(path, TSqlLexer, TSqlParser, TSqlParserVisitor, "tsql_file")
