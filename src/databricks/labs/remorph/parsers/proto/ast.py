
from databricks.labs.remorph.parsers.ast import node


@node
class Proto:
    syntax: any = None
    empty_statement: any = None
    top_level_def: any = None
    option_statement: any = None
    package_statement: any = None
    import_statement: any = None

@node
class Syntax:
    

@node
class ImportStatement:
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
    full_ident: any = None
    full_ident: any = None

@node
class FieldLabel:
    

@node
class Field:
    field_label: any = None
    type: any = None
    field_name: any = None
    field_number: any = None
    field_options: any = None

@node
class FieldOptions:
    field_option: any = None
    field_option: any = None

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
    empty_statement: any = None
    oneof_field: any = None
    option_statement: any = None

@node
class OneofField:
    type: any = None
    field_name: any = None
    field_number: any = None
    field_options: any = None

@node
class MapField:
    key_type: any = None
    type: any = None
    map_name: any = None
    field_number: any = None
    field_options: any = None

@node
class KeyType:
    

@node
class Type:
    enum_type: any = None
    message_type: any = None

@node
class Reserved:
    reserved_field_names: any = None
    ranges: any = None

@node
class Ranges:
    range: any = None
    range: any = None

@node
class Range:
    int_lit: any = None
    int_lit: any = None

@node
class ReservedFieldNames:
    str_lit: any = None
    str_lit: any = None

@node
class TopLevelDef:
    service_def: any = None
    extend_def: any = None
    enum_def: any = None
    message_def: any = None

@node
class EnumDef:
    enum_name: any = None
    enum_body: any = None

@node
class EnumBody:
    enum_element: any = None

@node
class EnumElement:
    empty_statement: any = None
    enum_field: any = None
    option_statement: any = None

@node
class EnumField:
    ident: any = None
    int_lit: any = None
    enum_value_options: any = None

@node
class EnumValueOptions:
    enum_value_option: any = None
    enum_value_option: any = None

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
    message_element: any = None

@node
class MessageElement:
    empty_statement: any = None
    reserved: any = None
    map_field: any = None
    oneof: any = None
    option_statement: any = None
    extend_def: any = None
    message_def: any = None
    enum_def: any = None
    field: any = None

@node
class ExtendDef:
    message_type: any = None
    empty_statement: any = None
    field: any = None

@node
class ServiceDef:
    service_name: any = None
    service_element: any = None

@node
class ServiceElement:
    empty_statement: any = None
    rpc: any = None
    option_statement: any = None

@node
class Rpc:
    rpc_name: any = None
    message_type: any = None
    message_type: any = None
    empty_statement: any = None
    option_statement: any = None

@node
class Constant:
    block_lit: any = None
    bool_lit: any = None
    str_lit: any = None
    float_lit: any = None
    int_lit: any = None
    full_ident: any = None

@node
class BlockLit:
    ident: any = None
    constant: any = None

@node
class EmptyStatement:
    

@node
class Ident:
    keywords: any = None

@node
class FullIdent:
    ident: any = None
    ident: any = None

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
    message_name: any = None
    ident: any = None

@node
class EnumType:
    enum_name: any = None
    ident: any = None

@node
class IntLit:
    

@node
class StrLit:
    

@node
class BoolLit:
    

@node
class FloatLit:
    

@node
class Keywords:
    
