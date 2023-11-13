import pathlib

from .generated.ANTLRv4Lexer import ANTLRv4Lexer
from .generated.ANTLRv4Parser import ANTLRv4Parser
from .generated.ANTLRv4ParserVisitor import ANTLRv4ParserVisitor
from .visitor import AntlrAST
from ..base import init_parse

__all__ = ['parse_g4']


def parse_g4(path: pathlib.Path):
    return init_parse(path, ANTLRv4Lexer, ANTLRv4Parser, AntlrAST, 'grammarSpec')
