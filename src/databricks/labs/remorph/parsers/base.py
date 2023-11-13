import dataclasses
import functools
import os
from pathlib import Path

from antlr4 import CommonTokenStream, FileStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken

__all__ = ["node", "init_parse"]


def node(cls):
    cls = functools.partial(dataclasses.dataclass, slots=True, match_args=True, frozen=True, repr=False)(cls)
    fields = dataclasses.fields(cls)

    def __repr__(self):
        values = []
        for field in fields:
            v = getattr(self, field.name)
            if not v:
                continue
            values.append(f"{field.name}={v}")
        return f'{cls.__name__}({", ".join(values)})'

    __repr__.__qualname__ = f"{cls.__qualname__}.__repr__"
    cls.__repr__ = __repr__

    return cls


class SyntaxErrorListener(ErrorListener):

    def __init__(self, context_lines: int = 2) -> None:
        self._context_lines = context_lines

    def syntaxError(self, recognizer: Recognizer, token: CommonToken, line: int, pos: int, msg: str,
                    e: Exception,
                    ):
        buf = [f"{msg} at line {line}:{pos}", ""]
        stream = token.getInputStream()
        if isinstance(stream, FileStream):
            current_dir = Path(os.curdir).absolute()
            src = Path(stream.fileName).absolute()
            common_path = Path(os.path.commonpath([src.as_posix(), current_dir.as_posix()]))
            relative_path = src.relative_to(common_path)
            buf.append(f"{relative_path.as_posix()}:")
        buf.append(self._surround(stream, token))
        raise SyntaxError("\n".join(buf))

    def _surround(self, stream: InputStream, token: CommonToken):
        start = token.line - self._context_lines - 1
        finish = token.line + self._context_lines - 1
        lines = []
        for num, line in enumerate(str(stream).splitlines()):
            if num < start:
                continue
            if num > finish:
                continue
            lines.append((num + 1, line))
        num_padding = len(str(max(_[0] for _ in lines)))
        buf = []
        for num, line in lines:
            buf.append(f"{num:{num_padding}d}: {line}")
            if token.line == num:
                left_pad = "-" * (token.column + num_padding + 2)
                highlight = "^" * (token.stop + 1 - token.start)
                buf.append(f"{left_pad}{highlight}")
        return "\n".join(buf)


def init_parse(path: Path, lexer_type: type, parser_type: type, visitor_type: type, main: str):
    fs = FileStream(path.as_posix(), "utf8")
    stream = CommonTokenStream(lexer_type(fs))
    parser = parser_type(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(SyntaxErrorListener())
    main_rule = getattr(parser, main)()
    visitor = visitor_type()
    return main_rule.accept(visitor)
