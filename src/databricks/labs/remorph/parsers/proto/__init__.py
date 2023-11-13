import antlr4
import pathlib

from .generated.Protobuf3Lexer import Protobuf3Lexer
from .generated.Protobuf3Parser import Protobuf3Parser
from .generated.Protobuf3Visitor import Protobuf3Visitor
from .visitor import Protobuf3AST

__all__ = ['parse_proto', 'Protobuf3Visitor']

from ..base import init_parse


def parse_proto(path: pathlib.Path):
    return init_parse(path, Protobuf3Lexer, Protobuf3Parser, Protobuf3AST, 'proto')
