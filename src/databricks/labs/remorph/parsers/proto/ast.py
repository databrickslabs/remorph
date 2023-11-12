
from databricks.labs.remorph.parsers.ast import node


@node
class Proto:
    syntax: 'Syntax' = None
    import_statement: list['ImportStatement'] = None
    package_statement: list['PackageStatement'] = None
    option_statement: list['OptionStatement'] = None
    top_level_def: list['TopLevelDef'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class ImportStatement:
    weak: bool = False
    public: bool = False
    str_lit: 'StrLit' = None

@node
class PackageStatement:
    full_ident: 'FullIdent' = None

@node
class OptionStatement:
    option_name: 'OptionName' = None
    constant: 'Constant' = None

@node
class OptionName:
    full_ident: 'FullIdent' = None
    dot: bool = False
    right_full_ident: 'FullIdent' = None

@node
class Field:
    field_label: list['FieldLabel'] = None
    type_: 'Type' = None
    field_name: 'FieldName' = None
    field_number: 'FieldNumber' = None
    lb: bool = False
    field_options: 'FieldOptions' = None
    rb: bool = False

@node
class FieldOptions:
    left_field_option: 'FieldOption' = None
    right_field_option: list['FieldOption'] = None

@node
class FieldOption:
    option_name: 'OptionName' = None
    constant: 'Constant' = None

@node
class FieldNumber:
    int_lit: 'IntLit' = None

@node
class Oneof:
    oneof_name: 'OneofName' = None
    option_statement: list['OptionStatement'] = None
    oneof_field: list['OneofField'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class OneofField:
    type_: 'Type' = None
    field_name: 'FieldName' = None
    field_number: 'FieldNumber' = None
    lb: bool = False
    field_options: 'FieldOptions' = None
    rb: bool = False

@node
class MapField:
    key_type: 'KeyType' = None
    type_: 'Type' = None
    map_name: 'MapName' = None
    field_number: 'FieldNumber' = None
    lb: bool = False
    field_options: 'FieldOptions' = None
    rb: bool = False

@node
class Type:
    message_type: 'MessageType' = None
    enum_type: 'EnumType' = None

@node
class Reserved:
    ranges: 'Ranges' = None
    reserved_field_names: 'ReservedFieldNames' = None

@node
class Ranges:
    left_range: 'Range' = None
    right_range: list['Range'] = None

@node
class Range:
    int_lit: 'IntLit' = None
    to: bool = False

@node
class ReservedFieldNames:
    left_str_lit: 'StrLit' = None
    right_str_lit: list['StrLit'] = None

@node
class TopLevelDef:
    message_def: 'MessageDef' = None
    enum_def: 'EnumDef' = None
    extend_def: 'ExtendDef' = None
    service_def: 'ServiceDef' = None

@node
class EnumDef:
    enum_name: 'EnumName' = None
    enum_body: 'EnumBody' = None

@node
class EnumBody:
    enum_element: list['EnumElement'] = None

@node
class EnumElement:
    option_statement: 'OptionStatement' = None
    enum_field: 'EnumField' = None
    empty_statement: 'EmptyStatement' = None

@node
class EnumField:
    ident: 'Ident' = None
    minus: bool = False
    int_lit: 'IntLit' = None
    enum_value_options: list['EnumValueOptions'] = None

@node
class EnumValueOptions:
    left_enum_value_option: 'EnumValueOption' = None
    right_enum_value_option: list['EnumValueOption'] = None

@node
class EnumValueOption:
    option_name: 'OptionName' = None
    constant: 'Constant' = None

@node
class MessageDef:
    message_name: 'MessageName' = None
    message_body: 'MessageBody' = None

@node
class MessageBody:
    message_element: list['MessageElement'] = None

@node
class MessageElement:
    field: 'Field' = None
    enum_def: 'EnumDef' = None
    message_def: 'MessageDef' = None
    extend_def: 'ExtendDef' = None
    option_statement: 'OptionStatement' = None
    oneof: 'Oneof' = None
    map_field: 'MapField' = None
    reserved: 'Reserved' = None
    empty_statement: 'EmptyStatement' = None

@node
class ExtendDef:
    message_type: 'MessageType' = None
    field: list['Field'] = None
    empty_statement: list['EmptyStatement'] = None

@node
class ServiceDef:
    service_name: 'ServiceName' = None
    service_element: list['ServiceElement'] = None

@node
class ServiceElement:
    option_statement: 'OptionStatement' = None
    rpc: 'Rpc' = None
    empty_statement: 'EmptyStatement' = None

@node
class Rpc:
    rpc_name: 'RpcName' = None
    right_stream: bool = False
    third_message_type: 'MessageType' = None
    sixth_stream: bool = False
    seventh_message_type: 'MessageType' = None

@node
class Constant:
    full_ident: 'FullIdent' = None
    minus: bool = False
    plus: bool = False
    int_lit: 'IntLit' = None
    float_lit: 'FloatLit' = None
    str_lit: 'StrLit' = None
    bool_lit: 'BoolLit' = None
    block_lit: 'BlockLit' = None

@node
class BlockLit:
    ident: list['Ident'] = None
    constant: list['Constant'] = None

@node
class Ident:
    keywords: 'Keywords' = None

@node
class FullIdent:
    left_ident: 'Ident' = None
    right_ident: list['Ident'] = None

@node
class MessageName:
    ident: 'Ident' = None

@node
class EnumName:
    ident: 'Ident' = None

@node
class FieldName:
    ident: 'Ident' = None

@node
class OneofName:
    ident: 'Ident' = None

@node
class MapName:
    ident: 'Ident' = None

@node
class ServiceName:
    ident: 'Ident' = None

@node
class RpcName:
    ident: 'Ident' = None

@node
class MessageType:
    left_dot: bool = False
    ident: list['Ident'] = None
    message_name: 'MessageName' = None

@node
class EnumType:
    left_dot: bool = False
    ident: list['Ident'] = None
    enum_name: 'EnumName' = None
