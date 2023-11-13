from databricks.labs.remorph.parsers.base import node


@node
class Proto:
    syntax: 'Syntax' = None
    import_statement: list['ImportStatement'] = None
    package_statement: list['PackageStatement'] = None
    option_statement: list['OptionStatement'] = None
    top_level_def: list['TopLevelDef'] = None
    empty_statement: list['EmptyStatement'] = None
    eof: str = None

@node
class ImportStatement:
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
    right: 'FullIdent' = None

@node
class Field:
    field_label: list['FieldLabel'] = None
    type_: 'Type' = None
    field_name: 'FieldName' = None
    field_number: 'FieldNumber' = None
    field_options: 'FieldOptions' = None

@node
class FieldOptions:
    left: 'FieldOption' = None
    right: list['FieldOption'] = None

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
    field_options: 'FieldOptions' = None

@node
class MapField:
    key_type: 'KeyType' = None
    type_: 'Type' = None
    map_name: 'MapName' = None
    field_number: 'FieldNumber' = None
    field_options: 'FieldOptions' = None

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
    left: 'Range' = None
    right: list['Range'] = None

@node
class Range:
    int_lit: 'IntLit' = None

@node
class ReservedFieldNames:
    left: 'StrLit' = None
    right: list['StrLit'] = None

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
    int_lit: 'IntLit' = None
    enum_value_options: list['EnumValueOptions'] = None

@node
class EnumValueOptions:
    left: 'EnumValueOption' = None
    right: list['EnumValueOption'] = None

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
    left: 'MessageType' = None
    right: 'MessageType' = None

@node
class Constant:
    full_ident: 'FullIdent' = None
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
    identifier: str = None
    keywords: 'Keywords' = None

@node
class FullIdent:
    left: 'Ident' = None
    right: list['Ident'] = None

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
    ident: list['Ident'] = None
    message_name: 'MessageName' = None

@node
class EnumType:
    ident: list['Ident'] = None
    enum_name: 'EnumName' = None

@node
class IntLit:
    int_lit: str = None

@node
class StrLit:
    str_lit: str = None

@node
class BoolLit:
    bool_lit: str = None

@node
class FloatLit:
    float_lit: str = None

@node
class Keywords:
    bool_lit: str = None
