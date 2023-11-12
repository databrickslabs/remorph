import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.proto.generated.Protobuf3Parser import Protobuf3Parser as proto
from databricks.labs.remorph.parsers.proto.generated.Protobuf3Visitor import Protobuf3Visitor
from databricks.labs.remorph.parsers.proto.ast import *


class Protobuf3AST(Protobuf3Visitor):
    def _(self, ctx: antlr4.ParserRuleContext):
        if not ctx:
            return None
        return self.visit(ctx)
    
    def repeated(self, ctx: antlr4.ParserRuleContext, ctx_type: type) -> list[any]:
        if not ctx:
            return []
        out = []
        for rc in ctx.getTypedRuleContexts(ctx_type):
            mapped = self._(rc)
            if not mapped:
                continue
            out.append(mapped)
        return out

    def visitTerminal(self, ctx: TerminalNodeImpl):
        return ctx.getText()

    def visitProto(self, ctx: proto.ProtoContext):
        syntax = self._(ctx.syntax())
        empty_statement = self._(ctx.emptyStatement_())
        top_level_def = self._(ctx.topLevelDef())
        option_statement = self._(ctx.optionStatement())
        package_statement = self._(ctx.packageStatement())
        import_statement = self._(ctx.importStatement())
        return Proto(syntax, empty_statement, top_level_def, option_statement, package_statement, import_statement)

    def visitImportStatement(self, ctx: proto.ImportStatementContext):
        str_lit = self._(ctx.strLit())
        return ImportStatement(str_lit)

    def visitPackageStatement(self, ctx: proto.PackageStatementContext):
        full_ident = self._(ctx.fullIdent())
        return PackageStatement(full_ident)

    def visitOptionStatement(self, ctx: proto.OptionStatementContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return OptionStatement(option_name, constant)

    def visitOptionName(self, ctx: proto.OptionNameContext):
        full_ident = self._(ctx.fullIdent())
        full_ident = self._(ctx.fullIdent())
        full_ident = self._(ctx.fullIdent())
        return OptionName(full_ident, full_ident, full_ident)

    def visitField(self, ctx: proto.FieldContext):
        field_label = self._(ctx.fieldLabel())
        type = self._(ctx.type_())
        field_name = self._(ctx.fieldName())
        field_number = self._(ctx.fieldNumber())
        field_options = self._(ctx.fieldOptions())
        return Field(field_label, type, field_name, field_number, field_options)

    def visitFieldOptions(self, ctx: proto.FieldOptionsContext):
        field_option = self._(ctx.fieldOption())
        field_option = self._(ctx.fieldOption())
        return FieldOptions(field_option, field_option)

    def visitFieldOption(self, ctx: proto.FieldOptionContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return FieldOption(option_name, constant)

    def visitFieldNumber(self, ctx: proto.FieldNumberContext):
        int_lit = self._(ctx.intLit())
        return FieldNumber(int_lit)

    def visitOneof(self, ctx: proto.OneofContext):
        oneof_name = self._(ctx.oneofName())
        empty_statement = self._(ctx.emptyStatement_())
        oneof_field = self._(ctx.oneofField())
        option_statement = self._(ctx.optionStatement())
        return Oneof(oneof_name, empty_statement, oneof_field, option_statement)

    def visitOneofField(self, ctx: proto.OneofFieldContext):
        type = self._(ctx.type_())
        field_name = self._(ctx.fieldName())
        field_number = self._(ctx.fieldNumber())
        field_options = self._(ctx.fieldOptions())
        return OneofField(type, field_name, field_number, field_options)

    def visitMapField(self, ctx: proto.MapFieldContext):
        key_type = self._(ctx.keyType())
        type = self._(ctx.type_())
        map_name = self._(ctx.mapName())
        field_number = self._(ctx.fieldNumber())
        field_options = self._(ctx.fieldOptions())
        return MapField(key_type, type, map_name, field_number, field_options)

    def visitType_(self, ctx: proto.Type_Context):
        enum_type = self._(ctx.enumType())
        message_type = self._(ctx.messageType())
        return Type(enum_type, message_type)

    def visitReserved(self, ctx: proto.ReservedContext):
        reserved_field_names = self._(ctx.reservedFieldNames())
        ranges = self._(ctx.ranges())
        return Reserved(reserved_field_names, ranges)

    def visitRanges(self, ctx: proto.RangesContext):
        range = self._(ctx.range_())
        range = self._(ctx.range_())
        return Ranges(range, range)

    def visitRange_(self, ctx: proto.Range_Context):
        int_lit = self._(ctx.intLit())
        int_lit = self._(ctx.intLit())
        return Range(int_lit, int_lit)

    def visitReservedFieldNames(self, ctx: proto.ReservedFieldNamesContext):
        str_lit = self._(ctx.strLit())
        str_lit = self._(ctx.strLit())
        return ReservedFieldNames(str_lit, str_lit)

    def visitTopLevelDef(self, ctx: proto.TopLevelDefContext):
        service_def = self._(ctx.serviceDef())
        extend_def = self._(ctx.extendDef())
        enum_def = self._(ctx.enumDef())
        message_def = self._(ctx.messageDef())
        return TopLevelDef(service_def, extend_def, enum_def, message_def)

    def visitEnumDef(self, ctx: proto.EnumDefContext):
        enum_name = self._(ctx.enumName())
        enum_body = self._(ctx.enumBody())
        return EnumDef(enum_name, enum_body)

    def visitEnumBody(self, ctx: proto.EnumBodyContext):
        enum_element = self._(ctx.enumElement())
        return EnumBody(enum_element)

    def visitEnumElement(self, ctx: proto.EnumElementContext):
        empty_statement = self._(ctx.emptyStatement_())
        enum_field = self._(ctx.enumField())
        option_statement = self._(ctx.optionStatement())
        return EnumElement(empty_statement, enum_field, option_statement)

    def visitEnumField(self, ctx: proto.EnumFieldContext):
        ident = self._(ctx.ident())
        int_lit = self._(ctx.intLit())
        enum_value_options = self._(ctx.enumValueOptions())
        return EnumField(ident, int_lit, enum_value_options)

    def visitEnumValueOptions(self, ctx: proto.EnumValueOptionsContext):
        enum_value_option = self._(ctx.enumValueOption())
        enum_value_option = self._(ctx.enumValueOption())
        return EnumValueOptions(enum_value_option, enum_value_option)

    def visitEnumValueOption(self, ctx: proto.EnumValueOptionContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return EnumValueOption(option_name, constant)

    def visitMessageDef(self, ctx: proto.MessageDefContext):
        message_name = self._(ctx.messageName())
        message_body = self._(ctx.messageBody())
        return MessageDef(message_name, message_body)

    def visitMessageBody(self, ctx: proto.MessageBodyContext):
        message_element = self._(ctx.messageElement())
        return MessageBody(message_element)

    def visitMessageElement(self, ctx: proto.MessageElementContext):
        empty_statement = self._(ctx.emptyStatement_())
        reserved = self._(ctx.reserved())
        map_field = self._(ctx.mapField())
        oneof = self._(ctx.oneof())
        option_statement = self._(ctx.optionStatement())
        extend_def = self._(ctx.extendDef())
        message_def = self._(ctx.messageDef())
        enum_def = self._(ctx.enumDef())
        field = self._(ctx.field())
        return MessageElement(empty_statement, reserved, map_field, oneof, option_statement, extend_def, message_def, enum_def, field)

    def visitExtendDef(self, ctx: proto.ExtendDefContext):
        message_type = self._(ctx.messageType())
        empty_statement = self._(ctx.emptyStatement_())
        field = self._(ctx.field())
        return ExtendDef(message_type, empty_statement, field)

    def visitServiceDef(self, ctx: proto.ServiceDefContext):
        service_name = self._(ctx.serviceName())
        service_element = self._(ctx.serviceElement())
        return ServiceDef(service_name, service_element)

    def visitServiceElement(self, ctx: proto.ServiceElementContext):
        empty_statement = self._(ctx.emptyStatement_())
        rpc = self._(ctx.rpc())
        option_statement = self._(ctx.optionStatement())
        return ServiceElement(empty_statement, rpc, option_statement)

    def visitRpc(self, ctx: proto.RpcContext):
        rpc_name = self._(ctx.rpcName())
        message_type = self._(ctx.messageType())
        message_type = self._(ctx.messageType())
        empty_statement = self._(ctx.emptyStatement_())
        option_statement = self._(ctx.optionStatement())
        return Rpc(rpc_name, message_type, message_type, empty_statement, option_statement)

    def visitConstant(self, ctx: proto.ConstantContext):
        block_lit = self._(ctx.blockLit())
        bool_lit = self._(ctx.boolLit())
        str_lit = self._(ctx.strLit())
        float_lit = self._(ctx.floatLit())
        int_lit = self._(ctx.intLit())
        full_ident = self._(ctx.fullIdent())
        return Constant(block_lit, bool_lit, str_lit, float_lit, int_lit, full_ident)

    def visitBlockLit(self, ctx: proto.BlockLitContext):
        ident = self._(ctx.ident())
        constant = self._(ctx.constant())
        return BlockLit(ident, constant)

    def visitIdent(self, ctx: proto.IdentContext):
        keywords = self._(ctx.keywords())
        return Ident(keywords)

    def visitFullIdent(self, ctx: proto.FullIdentContext):
        ident = self._(ctx.ident())
        ident = self._(ctx.ident())
        return FullIdent(ident, ident)

    def visitMessageName(self, ctx: proto.MessageNameContext):
        ident = self._(ctx.ident())
        return MessageName(ident)

    def visitEnumName(self, ctx: proto.EnumNameContext):
        ident = self._(ctx.ident())
        return EnumName(ident)

    def visitFieldName(self, ctx: proto.FieldNameContext):
        ident = self._(ctx.ident())
        return FieldName(ident)

    def visitOneofName(self, ctx: proto.OneofNameContext):
        ident = self._(ctx.ident())
        return OneofName(ident)

    def visitMapName(self, ctx: proto.MapNameContext):
        ident = self._(ctx.ident())
        return MapName(ident)

    def visitServiceName(self, ctx: proto.ServiceNameContext):
        ident = self._(ctx.ident())
        return ServiceName(ident)

    def visitRpcName(self, ctx: proto.RpcNameContext):
        ident = self._(ctx.ident())
        return RpcName(ident)

    def visitMessageType(self, ctx: proto.MessageTypeContext):
        message_name = self._(ctx.messageName())
        ident = self._(ctx.ident())
        return MessageType(message_name, ident)

    def visitEnumType(self, ctx: proto.EnumTypeContext):
        enum_name = self._(ctx.enumName())
        ident = self._(ctx.ident())
        return EnumType(enum_name, ident)
