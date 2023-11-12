import antlr4
import pathlib

from .generated.Protobuf3Lexer import Protobuf3Lexer
from .generated.Protobuf3Parser import Protobuf3Parser
from .generated.Protobuf3Visitor import Protobuf3Visitor
from .visitor import Protobuf3AST

__all__ = ['parse_file', 'Protobuf3Visitor']


def parse_file(path: pathlib.Path):
    fs = antlr4.FileStream(path.as_posix(), 'utf8')
    lexer = Protobuf3Lexer(fs)
    stream = antlr4.CommonTokenStream(lexer)
    parser = Protobuf3Parser(stream)
    proto = parser.proto()
    return proto.accept(Protobuf3AST())
