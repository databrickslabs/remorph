import antlr4
import pathlib

from .generated.ANTLRv4Lexer import ANTLRv4Lexer
from .generated.ANTLRv4Parser import ANTLRv4Parser
from .generated.ANTLRv4ParserVisitor import ANTLRv4ParserVisitor

__all__ = ['parse_file', 'ANTLRv4ParserVisitor']


def parse_file(path: pathlib.Path):
    fs = antlr4.FileStream(path.as_posix(), 'utf8')
    lexer = ANTLRv4Lexer(fs)
    stream = antlr4.CommonTokenStream(lexer)
    parser = ANTLRv4Parser(stream)
    grammar_spec = parser.grammarSpec()
    return grammar_spec
