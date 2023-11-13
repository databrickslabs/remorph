from databricks.labs.remorph.parsers.base import node


@node
class Proto:
    syntax: "Syntax" = None
    import_statement: list["ImportStatement"] = None
    package_statement: list["PackageStatement"] = None
    option_statement: list["OptionStatement"] = None
    top_level_def: list["TopLevelDef"] = None
    empty_statement: list["EmptyStatement"] = None
    eof: str = None


@node
class Syntax:
    proto3_lit_single: bool = False
    proto3_lit_dobule: bool = False


@node
class ImportStatement:
    weak: bool = False
    public: bool = False
    str_lit: "StrLit" = None


@node
class PackageStatement:
    full_ident: "FullIdent" = None


@node
class OptionStatement:
    option_name: "OptionName" = None
    constant: "Constant" = None


@node
class OptionName:
    full_ident: "FullIdent" = None
    lp: bool = False
    rp: bool = False
    dot: bool = False
    right: "FullIdent" = None


@node
class FieldLabel:
    optional: bool = False
    repeated: bool = False


@node
class Field:
    field_label: list["FieldLabel"] = None
    type_: "Type" = None
    field_name: "Ident" = None
    field_number: "IntLit" = None
    lb: bool = False
    field_options: "FieldOptions" = None
    rb: bool = False


@node
class FieldOptions:
    left: "FieldOption" = None
    right: list["FieldOption"] = None


@node
class FieldOption:
    option_name: "OptionName" = None
    constant: "Constant" = None


@node
class Oneof:
    oneof_name: "Ident" = None
    option_statement: list["OptionStatement"] = None
    oneof_field: list["OneofField"] = None
    empty_statement: list["EmptyStatement"] = None


@node
class OneofField:
    type_: "Type" = None
    field_name: "Ident" = None
    field_number: "IntLit" = None
    lb: bool = False
    field_options: "FieldOptions" = None
    rb: bool = False


@node
class MapField:
    key_type: "KeyType" = None
    type_: "Type" = None
    map_name: "Ident" = None
    field_number: "IntLit" = None
    lb: bool = False
    field_options: "FieldOptions" = None
    rb: bool = False


@node
class KeyType:
    int32: bool = False
    int64: bool = False
    uint32: bool = False
    uint64: bool = False
    sint32: bool = False
    sint64: bool = False
    fixed32: bool = False
    fixed64: bool = False
    sfixed32: bool = False
    sfixed64: bool = False
    bool_: bool = False
    string: bool = False


@node
class Type:
    double: bool = False
    float: bool = False
    int32: bool = False
    int64: bool = False
    uint32: bool = False
    uint64: bool = False
    sint32: bool = False
    sint64: bool = False
    fixed32: bool = False
    fixed64: bool = False
    sfixed32: bool = False
    sfixed64: bool = False
    bool_: bool = False
    string: bool = False
    bytes: bool = False
    message_type: "MessageType" = None
    enum_type: "EnumType" = None


@node
class Reserved:
    ranges: "Ranges" = None
    reserved_field_names: "ReservedFieldNames" = None


@node
class Ranges:
    left: "Range" = None
    right: list["Range"] = None


@node
class Range:
    left: "IntLit" = None
    to: bool = False
    right: "IntLit" = None
    max: bool = False


@node
class ReservedFieldNames:
    left: "StrLit" = None
    right: list["StrLit"] = None


@node
class TopLevelDef:
    message_def: "MessageDef" = None
    enum_def: "EnumDef" = None
    extend_def: "ExtendDef" = None
    service_def: "ServiceDef" = None


@node
class EnumDef:
    enum_name: "Ident" = None
    enum_body: "EnumBody" = None


@node
class EnumBody:
    enum_element: list["EnumElement"] = None


@node
class EnumElement:
    option_statement: "OptionStatement" = None
    enum_field: "EnumField" = None
    empty_statement: "EmptyStatement" = None


@node
class EnumField:
    ident: "Ident" = None
    minus: bool = False
    int_lit: "IntLit" = None
    enum_value_options: list["EnumValueOptions"] = None


@node
class EnumValueOptions:
    left: "EnumValueOption" = None
    right: list["EnumValueOption"] = None


@node
class EnumValueOption:
    option_name: "OptionName" = None
    constant: "Constant" = None


@node
class MessageDef:
    message_name: "Ident" = None
    message_body: "MessageBody" = None


@node
class MessageBody:
    message_element: list["MessageElement"] = None


@node
class MessageElement:
    field: "Field" = None
    enum_def: "EnumDef" = None
    message_def: "MessageDef" = None
    extend_def: "ExtendDef" = None
    option_statement: "OptionStatement" = None
    oneof: "Oneof" = None
    map_field: "MapField" = None
    reserved: "Reserved" = None
    empty_statement: "EmptyStatement" = None


@node
class ExtendDef:
    message_type: "MessageType" = None
    field: list["Field"] = None
    empty_statement: list["EmptyStatement"] = None


@node
class ServiceDef:
    service_name: "Ident" = None
    service_element: list["ServiceElement"] = None


@node
class ServiceElement:
    option_statement: "OptionStatement" = None
    rpc: "Rpc" = None
    empty_statement: "EmptyStatement" = None


@node
class Rpc:
    rpc_name: "Ident" = None
    left: bool = False
    right: "MessageType" = None
    third: bool = False
    fourth: "MessageType" = None
    lc: bool = False
    rc: bool = False
    semi: bool = False
    option_statement: list["OptionStatement"] = None
    empty_statement: list["EmptyStatement"] = None


@node
class Constant:
    full_ident: "FullIdent" = None
    minus: bool = False
    plus: bool = False
    int_lit: "IntLit" = None
    float_lit: "FloatLit" = None
    str_lit: "StrLit" = None
    bool_lit: "BoolLit" = None
    block_lit: "BlockLit" = None


@node
class BlockLit:
    ident: list["Ident"] = None
    constant: list["Constant"] = None


@node
class Ident:
    identifier: str = None
    keywords: "Keywords" = None


@node
class FullIdent:
    left: "Ident" = None
    right: list["Ident"] = None


@node
class MessageType:
    left: bool = False
    ident: list["Ident"] = None
    message_name: "Ident" = None


@node
class EnumType:
    left: bool = False
    ident: list["Ident"] = None
    enum_name: "Ident" = None


@node
class IntLit:
    int_lit: str = None


@node
class StrLit:
    str_lit: str = None
    proto3_lit_single: bool = False
    proto3_lit_dobule: bool = False


@node
class BoolLit:
    bool_lit: str = None


@node
class FloatLit:
    float_lit: str = None


@node
class Keywords:
    syntax: bool = False
    import_: bool = False
    weak: bool = False
    public: bool = False
    package_: bool = False
    option: bool = False
    optional: bool = False
    repeated: bool = False
    oneof: bool = False
    map_: bool = False
    int32: bool = False
    int64: bool = False
    uint32: bool = False
    uint64: bool = False
    sint32: bool = False
    sint64: bool = False
    fixed32: bool = False
    fixed64: bool = False
    sfixed32: bool = False
    sfixed64: bool = False
    bool_: bool = False
    string: bool = False
    double: bool = False
    float: bool = False
    bytes: bool = False
    reserved: bool = False
    to: bool = False
    max: bool = False
    enum: bool = False
    message: bool = False
    service: bool = False
    extend: bool = False
    rpc: bool = False
    stream: bool = False
    returns: bool = False
    bool_lit: str = None
