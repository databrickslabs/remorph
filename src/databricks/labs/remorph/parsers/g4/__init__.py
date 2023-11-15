import pathlib

from databricks.labs.remorph.parsers.base import init_parse
from databricks.labs.remorph.parsers.g4.g4ast import GrammarSpec
from databricks.labs.remorph.parsers.g4.generated.ANTLRv4Lexer import ANTLRv4Lexer
from databricks.labs.remorph.parsers.g4.generated.ANTLRv4Parser import ANTLRv4Parser
from databricks.labs.remorph.parsers.g4.visitor import AntlrAST

__all__ = ["parse_g4"]


def parse_g4(path: pathlib.Path) -> GrammarSpec:
    return init_parse(path, ANTLRv4Lexer, ANTLRv4Parser, AntlrAST, "grammarSpec")
