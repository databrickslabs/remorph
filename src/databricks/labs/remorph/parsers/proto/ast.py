
from databricks.labs.remorph.parsers.ast import node


@node
class Proto:
    syntax: any = None
    import_statement: list['ImportStatement'] = None
    package_statement: list['PackageStatement'] = None
    option_statement: list['OptionStatement'] = None
    top_level_def: list['TopLevelDef'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class ImportStatement:
    weak: bool = False
    public: bool = False
    str_lit: any = None

@node
class PackageStatement:
    full_ident: any = None

@node
class OptionStatement:
    option_name: any = None
    constant: any = None

@node
class OptionName:
    full_ident: any = None
    dot: bool = False
    right_full_ident: any = None

@node
class Field:
    field_label: list['FieldLabel'] = None
    type_: any = None
    field_name: any = None
    field_number: any = None
    lb: bool = False
    field_options: any = None
    rb: bool = False

@node
class FieldOptions:
    left_field_option: any = None
    right_field_option: list['FieldOption'] = None

@node
class FieldOption:
    option_name: any = None
    constant: any = None

@node
class FieldNumber:
    int_lit: any = None

@node
class Oneof:
    oneof_name: any = None
    option_statement: list['OptionStatement'] = None
    oneof_field: list['OneofField'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class OneofField:
    type_: any = None
    field_name: any = None
    field_number: any = None
    lb: bool = False
    field_options: any = None
    rb: bool = False

@node
class MapField:
    key_type: any = None
    type_: any = None
    map_name: any = None
    field_number: any = None
    lb: bool = False
    field_options: any = None
    rb: bool = False

@node
class Type:
    message_type: any = None
    enum_type: any = None

@node
class Reserved:
    ranges: any = None
    reserved_field_names: any = None

@node
class Ranges:
    left_range: any = None
    right_range: list['Range'] = None

@node
class Range:
    int_lit: any = None
    to: bool = False

@node
class ReservedFieldNames:
    left_str_lit: any = None
    right_str_lit: list['StrLit'] = None

@node
class TopLevelDef:
    message_def: any = None
    enum_def: any = None
    extend_def: any = None
    service_def: any = None

@node
class EnumDef:
    enum_name: any = None
    enum_body: any = None

@node
class EnumBody:
    enum_element: list['EnumElement'] = None

@node
class EnumElement:
    option_statement: any = None
    enum_field: any = None
    empty_statement: any = None

@node
class EnumField:
    ident: any = None
    minus: bool = False
    int_lit: any = None
    enum_value_options: list['EnumValueOptions'] = None

@node
class EnumValueOptions:
    left_enum_value_option: any = None
    right_enum_value_option: list['EnumValueOption'] = None

@node
class EnumValueOption:
    option_name: any = None
    constant: any = None

@node
class MessageDef:
    message_name: any = None
    message_body: any = None

@node
class MessageBody:
    message_element: list['MessageElement'] = None

@node
class MessageElement:
    field: any = None
    enum_def: any = None
    message_def: any = None
    extend_def: any = None
    option_statement: any = None
    oneof: any = None
    map_field: any = None
    reserved: any = None
    empty_statement: any = None

@node
class ExtendDef:
    message_type: any = None
    field: list['Field'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class ServiceDef:
    service_name: any = None
    service_element: list['ServiceElement'] = None

@node
class ServiceElement:
    option_statement: any = None
    rpc: any = None
    empty_statement: any = None

@node
class Rpc:
    rpc_name: any = None
    right_stream: bool = False
    third_message_type: any = None
    sixth_stream: bool = False
    seventh_message_type: any = None

@node
class Constant:
    full_ident: any = None
    minus: bool = False
    plus: bool = False
    int_lit: any = None
    float_lit: any = None
    str_lit: any = None
    bool_lit: any = None
    block_lit: any = None

@node
class BlockLit:
    ident: list['Ident'] = None
    constant: list['Constant'] = None

@node
class Ident:
    keywords: any = None

@node
class FullIdent:
    left_ident: any = None
    right_ident: list['Ident'] = None

@node
class MessageName:
    ident: any = None

@node
class EnumName:
    ident: any = None

@node
class FieldName:
    ident: any = None

@node
class OneofName:
    ident: any = None

@node
class MapName:
    ident: any = None

@node
class ServiceName:
    ident: any = None

@node
class RpcName:
    ident: any = None

@node
class MessageType:
    left_dot: bool = False
    ident: list['Ident'] = None
    message_name: any = None

@node
class EnumType:
    left_dot: bool = False
    ident: list['Ident'] = None
    enum_name: any = None
