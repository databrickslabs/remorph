import pathlib

from .ast import Proto
from .generated.Protobuf3Lexer import Protobuf3Lexer
from .generated.Protobuf3Parser import Protobuf3Parser
from .visitor import Protobuf3AST

__all__ = ["parse_proto"]

from ..base import init_parse


def parse_proto(path: pathlib.Path) -> Proto:
    return init_parse(path, Protobuf3Lexer, Protobuf3Parser, Protobuf3AST, "proto")
