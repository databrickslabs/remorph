import dataclasses
import functools
import os
import typing
from pathlib import Path
from typing import Callable

from antlr4 import CommonTokenStream, FileStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken

__all__ = ["node", 'TreeNode', "init_parse"]

T = typing.TypeVar('T')


class TransformStack(tuple['TreeNode']):

    def nest(self, node: 'TreeNode') -> 'TransformStack':
        return TransformStack(self + (node,))

    def skip_levels(self, klass: type[T]) -> T:
        remaining = self
        while remaining:
            if not isinstance(remaining[-1], klass):
                remaining = remaining[:-1]
                continue
            return remaining[-1]
        raise ValueError(f'no {klass.__name__} found')


class TreeNode:

    def replace(self, /, **kwargs):
        return dataclasses.replace(self, **kwargs)

    def transform_up_with_path(self, rule: Callable[[T, TransformStack], T], path: TransformStack = None) -> T:
        """Returns a copy of this node where `rule` has been recursively applied first to all of its
        children and then itself (post-order)."""
        if not path:
            path = TransformStack()
        dupe = []
        for field_name in self.__slots__:
            current_value = getattr(self, field_name)
            if not current_value:
                dupe.append(current_value)
                continue
            if isinstance(current_value, list):
                new_list = []
                for item in current_value:
                    if isinstance(item, TreeNode):
                        item = item.transform_up_with_path(rule, path.nest(self))
                    if item is not None:
                        new_list.append(item)
                dupe.append(new_list)
                continue
            if isinstance(current_value, dict):
                new_dict = {}
                for key, value in current_value.items():
                    if isinstance(value, TreeNode):
                        value = value.transform_up_with_path(rule, path.nest(self))
                    if value is not None:
                        new_dict[key] = value
                dupe.append(new_dict)
                continue
            if isinstance(current_value, TreeNode):
                current_value = current_value.transform_up_with_path(rule, path.nest(self))
            dupe.append(current_value)
        out = self.__class__(*dupe)
        return rule(out, path)

    def __hash__(self):
        h = 31
        for field_name in self.__slots__:
            current_value = getattr(self, field_name)
            if not current_value:
                h *= hash(current_value)
                continue
            if isinstance(current_value, list):
                for item in current_value:
                    h *= hash(item)
                continue
            if isinstance(current_value, dict):
                for key, value in sorted(current_value.items()):
                    h *= hash(key)
                    h *= hash(value)
                continue
            h *= hash(current_value)
        return h

    def __repr__(self):
        values = []
        for field_name in self.__slots__:
            current_value = getattr(self, field_name)
            if not current_value:
                continue
            values.append(f"{field_name}={current_value}")
        return f'{self.__class__.__name__}({", ".join(values)})'


def node(cls):
    cls = functools.partial(dataclasses.dataclass, slots=True, match_args=True, repr=False)(cls)
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
