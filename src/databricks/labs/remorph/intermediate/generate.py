import collections
import dataclasses
import enum
import logging
import os
from pathlib import Path
from dataclasses import dataclass, replace
from typing import Iterator

from databricks.labs.remorph.framework.entrypoint import get_logger, run_main, relative_paths
from databricks.labs.remorph.framework.logger import install_logger
from databricks.labs.remorph.parsers.proto import parse_proto
from databricks.labs.remorph.parsers.proto.ast import (
    BoolLit,
    Constant,
    EnumDef,
    Field,
    FieldLabel,
    FieldOptions,
    FloatLit,
    FullIdent,
    Ident,
    IntLit,
    Keywords,
    MapField,
    MessageDef,
    MessageElement,
    Oneof,
    OneofField,
    OptionName,
    Proto,
    StrLit,
    TopLevelDef,
    Type, ServiceDef, MessageType,
)

logger = get_logger(__file__)


@dataclass
class Scope:
    path: list[str]
    children: dict[str, 'Scope']
    parent: 'Scope' = None
    nodes: list['Node'] = dataclasses.field(default_factory=list)
    renames: dict[str, str] = dataclasses.field(default_factory=dict)

    def nest(self, name: str) -> 'Scope':
        return Scope(self.path + [name], {}, self, nodes=[])

    def prefix(self):
        if not self.path:
            return ''
        return f"{'.'.join(self.path)}."

    def resolve(self, type_ref: str) -> str:
        current = self
        while current is not None:
            ref = type_ref.lstrip(current.prefix())
            if ref in current.renames:
                return current.renames[ref]
            if ref in current.children:
                return ref
            current = current.parent
            continue
        raise KeyError(f'cannot resolve {type_ref}')

    def __repr__(self):
        nodes = ','.join(_.name for _ in self.nodes)
        if nodes:
            nodes = f' nodes={nodes}'
        prefix = self.prefix()
        if prefix:
            prefix = f' {prefix.rstrip(".")}'
        return f'<Scope{prefix}{nodes}>'


@dataclass
class NodeField:
    name: str
    type_ref: str
    optional: bool = False
    repeated: bool = False
    is_map: bool = False

    def decl(self, scope: Scope) -> str:
        return f'{self.name}: {self.annotation(scope)}{self.default()}'

    def default(self):
        if not self.optional:
            return ''
        if self.type_ref.name() == 'bool':
            return ' = False'
        return ' = None'

    def annotation(self, scope: Scope) -> str:
        ref = self.in_container(scope)
        if self.is_builtin_ref():
            return ref
        return f'"{ref}"'

    def is_builtin_ref(self):
        return self.is_builtin(self.type_ref)

    @staticmethod
    def is_builtin(ref):
        return ref in (bool.__name__, bytes.__name__, float.__name__, int.__name__, str.__name__)

    def in_container(self, scope: Scope):
        type_ref = self.type_ref
        if not self.is_builtin_ref():
            type_ref = scope.resolve(type_ref)
        if self.repeated:
            return f'list[{type_ref}]'
        if self.is_map:
            return f'dict[str,{type_ref}]'
        return type_ref


@dataclass
class Node:
    name: str
    scope: Scope
    fields: list[NodeField]
    parent_ref: str = None

    def full_name(self) -> str:
        return f'{self.scope.prefix()}{self.name}'

    def decl(self):
        lines = "\n    ".join(_.decl(self.scope) for _ in self.fields)
        if not lines:
            lines = 'pass'
        return f"{self.prelude()}\n    {lines}\n\n"

    def prelude(self):
        return f"@node\nclass {self.name}{self.extends()}:"

    def extends(self):
        if self.parent_ref is None:
            return ''
        return f'({self.parent_ref})'



class Transformer:

    def __init__(self, src: Path) -> None:
        self.path = src
        self.proto = parse_proto(self.path)
        self.nodes: list[Node] = []
        self.enums: list[enum.Enum] = []
        self.one_of = collections.defaultdict(set)
        self.as_field = collections.defaultdict(set)
        self.scope = Scope([], {}, nodes=[])
        self.imported = {}
        self.direct_extends = {}

    def source_name(self):
        return f'spark/connect/{self.path.name}'

    def derived_name(self):
        return self.path.name.rstrip('.proto')

    def parse(self):
        for tld in self.proto.top_level_def:
            self._top_level_def(tld, self.scope)
        self._deconflict_node_names()

    def _deconflict_node_names(self):
        potential_dupes = collections.defaultdict(set)
        for node in self.nodes:
            short_name = node.name
            full_name = node.full_name()
            potential_dupes[short_name].add(full_name)
        replace_refs = {}
        for base, full_names in potential_dupes.items():
            if len(full_names) == 1:
                continue
            for full_name in full_names:
                replace_refs[full_name] = full_name.replace('.', '')
        if not replace_refs:
            return
        for node in self.nodes:
            if node.full_name() not in replace_refs:
                continue
            full_name = node.full_name()
            node.name = replace_refs[full_name]
            logger.debug(f'replaced {full_name} with {node.name}')

    def link(self, sources: 'Sources'):
        exported = {}
        for source in sources.values():
            if source.source_name() == self.source_name():
                continue
            for symbol in source.exported:
                exported[symbol] = source
        for node in self.nodes:
            for field in node.fields:
                if field.type_ref not in exported:
                    continue
                # here we're a bit naive and assume that there's no conflict
                # between .proto files
                self.imported[field.type_ref] = exported[field.type_ref]

    def generate(self, dst):
        proto_name = self.path.name.rstrip('.proto')
        py_file = dst / f'{proto_name}.py'
        with py_file.open('w') as f:
            f.write(f"from databricks.labs.remorph.parsers.base import node\n")
            for ref, source in self.imported.items():
                f.write(f"from .{source.derived_name()} import {ref.name()}\n")
            f.write(f"\n\n")
            for node in self.nodes:
                f.write(node.decl())
                f.write(f"\n")
        relative_src, relative_dst = relative_paths(self.path, py_file)
        logger.info(f'generated {relative_dst} from {relative_src}')

    def _top_level_def(self, tld: TopLevelDef, scope: Scope):
        match tld:
            case TopLevelDef(service_def=ServiceDef(_, _)):
                return
            case TopLevelDef(message_def=message_def):
                for node in self._message_def(message_def, scope):
                    self.nodes.append(node)
            case TopLevelDef(enum_def=enum_def):
                self._enum_def(enum_def, scope)

    def _message_def(self, message_def: MessageDef, scope: Scope) -> Iterator[Node]:
        fields = []
        child_nodes = []
        node_ref = self._ident(message_def.message_name)
        child_scope = scope.nest(node_ref)

        oneof_types = set()

        for element in message_def.message_body.message_element: # TODO: collapse message_element to body
            match element:
                case MessageElement(field=Field(label, field_type, field_name)):
                    name = self._ident(field_name)
                    type_ref = self._type(field_type)
                    if not type_ref:
                        continue
                    optional, repeated = self._label(label)
                    fields.append(NodeField(name, type_ref, optional, repeated))
                case MessageElement(oneof=Oneof(oneof_field=oneof_fields)):
                    for oneof_field in oneof_fields:
                        match oneof_field:
                            case OneofField(field_type, field_name):
                                name = self._ident(field_name)
                                type_ref = self._type(field_type)
                                if not type_ref:
                                    continue
                                oneof_types.add(type_ref)
                                self._capture_hierarchy(scope, node_ref, type_ref)
                                fields.append(NodeField(name, type_ref, optional=True))
                case MessageElement(map_field=MapField(type_=value_t, map_name=field_name, field_options=opts)):
                    options = self._field_options(opts)
                    if "deprecated" in options:
                        continue
                    name = self._ident(field_name)
                    value_type_ref = self._type(value_t)
                    if not value_type_ref:
                        continue
                    fields.append(NodeField(name, value_type_ref, is_map=True))
                case MessageElement(message_def=MessageDef(nested_name, nested_body)):
                    nested_message_def = MessageDef(nested_name, nested_body)
                    for child_node in self._message_def(nested_message_def, child_scope):
                        child_nodes.append(child_node)
                case MessageElement(enum_def=EnumDef(left, right)):
                    name = self._ident(left)
                    values = []
                    for enum_element in right.enum_element:
                        value = self._ident(enum_element.enum_field.ident)
                        values.append(value)
                    self.enums.append(enum.Enum(name, values))
                case MessageElement(reserved=_):
                    continue
                case _:
                    continue

        node = Node(node_ref, scope, fields)
        scope.nodes.append(node)
        yield node

        if child_nodes:
            scope.children[node_ref] = child_scope

        for node in child_nodes:
            child_scope.nodes.append(node)
            if node.name in oneof_types:
                node.parent_ref = node_ref
                self.direct_extends[node.name] = node_ref
            yield node

    def _capture_hierarchy(self, scope: Scope, node_ref: str, type_ref: str):
        if NodeField.is_builtin(type_ref):
            return
        if node_ref == 'Persist' or type_ref == 'Persist':
            logger.debug('...')
        node_ref = f'{scope.prefix()}{node_ref}'
        self.one_of[type_ref].add(node_ref)
        self.one_of[node_ref].add(type_ref)
        self.as_field[node_ref].add(type_ref)

    def _enum_def(self, enum_def: EnumDef, scope: Scope):
        pass

    def _ident(self, ident: Ident) -> str:
        match ident:
            case Ident(keywords=Keywords(bool_lit=bl)):
                return "true" # FIXME: incorrectly parsing bool lit
            case Ident(identifier=v):
                return v
            case _:
                raise ValueError(f"unknown: {ident}")

    def _type(self, t: Type) -> str | None:
        if t.bool_:
            return bool.__name__
        if t.bytes:
            return bytes.__name__
        if t.double or t.float:
            return float.__name__
        if t.enum_type:
            return self._ident(t.enum_type.enum_name)
        if t.fixed32 or t.fixed64 or t.int32 or t.int64 or t.sint32 or t.sint64:
            return int.__name__
        if t.string:
            return str.__name__
        if t.message_type:
            return self._message_type(t.message_type)

    def _message_type(self, message_type: MessageType) -> str | None:
        match message_type:
            case MessageType(False, [], ident):
                return self._ident(ident)
            case MessageType(True, prefix, ident):
                prefix = [self._ident(_) for _ in prefix]
                if prefix[0] == 'google':
                    return None
                return '.'.join(prefix + [self._ident(ident)])

    def _label(self, labels: list["FieldLabel"]) -> tuple[bool, bool]:
        optional, repeated = False, False
        for label in labels:
            if label.optional:
                optional = True
            if label.repeated:
                repeated = True
        return optional, repeated

    @staticmethod
    def _try_list(value: list[any]) -> list[any]:
        if not value:
            return []
        return value

    def _field_options(self, opts: FieldOptions) -> dict[str, str]:
        if not opts:
            return {}
        options = {}
        field_options = [opts.left] + self._try_list(opts.right)
        for field_option in field_options:
            name = self._option_name(field_option.option_name)
            value = self._constant(field_option.constant)
            options[name] = value
        return options

    def _option_name(self, option_name: OptionName) -> str:
        match option_name:
            case OptionName(full_ident, right=None):
                return self._full_ident(full_ident)
            case OptionName(left, right=right):
                return f"({self._ident(left)}).{self._ident(right)}"
            case _:
                raise ValueError(option_name)

    def _constant(self, constant: Constant):
        mult = 1
        if constant.minus:
            mult = -1
        match constant:
            case Constant(full_ident=full_ident):
                return self._full_ident(full_ident)
            case Constant(int_lit=IntLit(v)):
                return int(v) * mult
            case Constant(float_lit=FloatLit(v)):
                return float(v) * mult
            case Constant(str_lit=StrLit(v, s, d)):
                return self._str_lit(StrLit(v, s, d))
            case Constant(bool_lit=BoolLit(v)):
                return v == "true"
            case Constant(block_lit=block_lit):
                raise ValueError(f"what is block lit? {block_lit}")
            case _:
                raise ValueError(f"unknown: {constant}")

    def _str_lit(self, str_lit: StrLit) -> str:
        return str_lit.str_lit.strip("'\"")

    def _full_ident(self, full_ident: FullIdent):
        left = [full_ident.left]
        right = self._try_list(
            full_ident.right)[1:] # FIXME: if alternative is repeated, it includes first child
        arr = [self._ident(_) for _ in left + right]
        return ".".join(arr)

    def __repr__(self):
        return f'<Transformer {self.source_name()}, {len(self.nodes)} types>'


class Sources(dict[str, Transformer]):

    def __init__(self, root: Path):
        super().__init__()
        self.root = root

    def __setitem__(self, key: str, value: Transformer):
        key = Path(key).relative_to(self.root).as_posix()
        value.parse()
        super().__setitem__(key, value)

    def link(self):
        one_of = collections.defaultdict(set)
        as_field = collections.defaultdict(set)
        for _, value in sorted(self.items()):
            for k,values in value.one_of.items():
                for v in values:
                    one_of[k].add(v)
            for k,values in value.as_field.items():
                for v in values:
                    as_field[k].add(v)
        extends = collections.defaultdict(set)
        for key, values in one_of.items():
            key_as_field = as_field.get(key, None)
            # if key_as_field is None:
            #     continue
            for v in values:
                v_as_field = as_field.get(v, {})

                other_values = one_of[v]
                if key in other_values and key in v_as_field:
                    logger.debug(f'{key}({v}) key_as_field={key_as_field}, v_as_field={v_as_field}')
                    extends[key].add(v)
        ext2 = sorted(extends.items())
        logger.debug('...')

        for path, value in sorted(self.items()):
            logger.debug(f'loading {path}')
            value.link(self)

    def generate(self, dst: Path):
        for path, value in sorted(self.items()):
            logger.debug(f'cross-compiling {path}')
            value.generate(dst)


def main():
    __folder__ = Path(__file__).parent
    dst = __folder__ / 'spark_connect'

    sources = Sources(__folder__ / 'proto')
    for path in sources.root.glob('**/*.proto'):
        # if path.name != 'expressions.proto':
        #     continue
        sources[path.as_posix()] = Transformer(path)
    sources.link()
    sources.generate(dst)


if __name__ == "__main__":
    run_main(main)
