import enum
import pathlib
from dataclasses import dataclass

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
    Type,
)


@dataclass
class NodeField:
    name: str
    type_ref: str
    optional: bool = False
    repeated: bool = False
    is_map: bool = False


@dataclass
class Node:
    name: str
    fields: list[NodeField]
    parent_ref: str = None


class IntermediateRepresentationGenerator:

    def __init__(self, proto: Proto) -> None:
        self.proto = proto
        self.nodes = []
        self.enums = []

    def run(self):
        for tld in self.proto.top_level_def:
            self._top_level_def(tld)

    def _top_level_def(self, tld: TopLevelDef):
        match tld:
            case TopLevelDef(service_def=_):
                return
            case TopLevelDef(message_def=message_def):
                self.nodes.append(self._message_def(message_def))
            case TopLevelDef(enum_def=enum_def):
                self._enum_def(enum_def)

    def _message_def(self, message_def: MessageDef, parent_ref: str = None) -> Node:
        fields = []
        node_name = self._ident(message_def.message_name)
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
                                fields.append(NodeField(name, type_ref, optional=True))
                case MessageElement(
                    map_field=MapField(type_=value_t, map_name=field_name, field_options=opts)):
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
                    child_node = self._message_def(nested_message_def, node_name)
                    self.nodes.append(child_node)
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
        return Node(node_name, fields, parent_ref)

    def _enum_def(self, enum_def: EnumDef):
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
            prefix = ""
            if t.message_type.ident:
                # TODO: skip if it's google
                prefix = ".".join([self._ident(_) for _ in t.message_type.ident]) + "."
            return prefix + self._ident(t.message_type.message_name)

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
            case Constant(str_lit=StrLit(v)):
                return v.strip("'\"")
            case Constant(bool_lit=BoolLit(v)):
                return v == "true"
            case Constant(block_lit=block_lit):
                raise ValueError(f"what is block lit? {block_lit}")
            case _:
                raise ValueError(f"unknown: {constant}")

    def _full_ident(self, full_ident: FullIdent):
        left = [full_ident.left]
        right = self._try_list(
            full_ident.right)[1:] # FIXME: if alternative is repeated, it includes first child
        arr = [self._ident(_) for _ in left + right]
        return ".".join(arr)


def main():
    __folder__ = pathlib.Path(__file__).parent

    for path in (__folder__ / "proto/spark/connect").glob("*.proto"):
        proto = parse_proto(path)

        ir_gen = IntermediateRepresentationGenerator(proto)
        ir_gen.run()


if __name__ == "__main__":
    main()
