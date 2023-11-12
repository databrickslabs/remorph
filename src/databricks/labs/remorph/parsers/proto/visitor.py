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
        import_statement = self.repeated(ctx, proto.ImportStatementContext)
        package_statement = self.repeated(ctx, proto.PackageStatementContext)
        option_statement = self.repeated(ctx, proto.OptionStatementContext)
        top_level_def = self.repeated(ctx, proto.TopLevelDefContext)
        empty_statement = self.repeated(ctx, proto.EmptyStatement_Context)
        return Proto(syntax, import_statement, package_statement, option_statement, top_level_def, empty_statement)

    def visitImportStatement(self, ctx: proto.ImportStatementContext):
        weak = self._(ctx.WEAK()) is not None
        public = self._(ctx.PUBLIC()) is not None
        str_lit = self._(ctx.strLit())
        return ImportStatement(weak, public, str_lit)

    def visitPackageStatement(self, ctx: proto.PackageStatementContext):
        full_ident = self._(ctx.fullIdent())
        return PackageStatement(full_ident)

    def visitOptionStatement(self, ctx: proto.OptionStatementContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return OptionStatement(option_name, constant)

    def visitOptionName(self, ctx: proto.OptionNameContext):
        full_ident = self._(ctx.fullIdent())
        dot = self._(ctx.DOT()) is not None
        right_full_ident = self._(ctx.fullIdent())
        return OptionName(full_ident, dot, right_full_ident)

    def visitField(self, ctx: proto.FieldContext):
        field_label = self.repeated(ctx, proto.FieldLabelContext)
        type_ = self._(ctx.type_())
        field_name = self._(ctx.fieldName())
        field_number = self._(ctx.fieldNumber())
        lb = self._(ctx.LB()) is not None
        field_options = self._(ctx.fieldOptions())
        rb = self._(ctx.RB()) is not None
        return Field(field_label, type_, field_name, field_number, lb, field_options, rb)

    def visitFieldOptions(self, ctx: proto.FieldOptionsContext):
        left_field_option = self._(ctx.fieldOption())
        right_field_option = self.repeated(ctx, proto.FieldOptionContext)
        return FieldOptions(left_field_option, right_field_option)

    def visitFieldOption(self, ctx: proto.FieldOptionContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return FieldOption(option_name, constant)

    def visitFieldNumber(self, ctx: proto.FieldNumberContext):
        int_lit = self._(ctx.intLit())
        return FieldNumber(int_lit)

    def visitOneof(self, ctx: proto.OneofContext):
        oneof_name = self._(ctx.oneofName())
        option_statement = self.repeated(ctx, proto.OptionStatementContext)
        oneof_field = self.repeated(ctx, proto.OneofFieldContext)
        empty_statement = self.repeated(ctx, proto.EmptyStatement_Context)
        return Oneof(oneof_name, option_statement, oneof_field, empty_statement)

    def visitOneofField(self, ctx: proto.OneofFieldContext):
        type_ = self._(ctx.type_())
        field_name = self._(ctx.fieldName())
        field_number = self._(ctx.fieldNumber())
        lb = self._(ctx.LB()) is not None
        field_options = self._(ctx.fieldOptions())
        rb = self._(ctx.RB()) is not None
        return OneofField(type_, field_name, field_number, lb, field_options, rb)

    def visitMapField(self, ctx: proto.MapFieldContext):
        key_type = self._(ctx.keyType())
        type_ = self._(ctx.type_())
        map_name = self._(ctx.mapName())
        field_number = self._(ctx.fieldNumber())
        lb = self._(ctx.LB()) is not None
        field_options = self._(ctx.fieldOptions())
        rb = self._(ctx.RB()) is not None
        return MapField(key_type, type_, map_name, field_number, lb, field_options, rb)

    def visitType_(self, ctx: proto.Type_Context):
        message_type = self._(ctx.messageType())
        enum_type = self._(ctx.enumType())
        return Type(message_type, enum_type)

    def visitReserved(self, ctx: proto.ReservedContext):
        ranges = self._(ctx.ranges())
        reserved_field_names = self._(ctx.reservedFieldNames())
        return Reserved(ranges, reserved_field_names)

    def visitRanges(self, ctx: proto.RangesContext):
        left_range = self._(ctx.range_())
        right_range = self.repeated(ctx, proto.Range_Context)
        return Ranges(left_range, right_range)

    def visitRange_(self, ctx: proto.Range_Context):
        int_lit = self._(ctx.intLit())
        to = self._(ctx.TO()) is not None
        return Range(int_lit, to)

    def visitReservedFieldNames(self, ctx: proto.ReservedFieldNamesContext):
        left_str_lit = self._(ctx.strLit())
        right_str_lit = self.repeated(ctx, proto.StrLitContext)
        return ReservedFieldNames(left_str_lit, right_str_lit)

    def visitTopLevelDef(self, ctx: proto.TopLevelDefContext):
        message_def = self._(ctx.messageDef())
        enum_def = self._(ctx.enumDef())
        extend_def = self._(ctx.extendDef())
        service_def = self._(ctx.serviceDef())
        return TopLevelDef(message_def, enum_def, extend_def, service_def)

    def visitEnumDef(self, ctx: proto.EnumDefContext):
        enum_name = self._(ctx.enumName())
        enum_body = self._(ctx.enumBody())
        return EnumDef(enum_name, enum_body)

    def visitEnumBody(self, ctx: proto.EnumBodyContext):
        enum_element = self.repeated(ctx, proto.EnumElementContext)
        return EnumBody(enum_element)

    def visitEnumElement(self, ctx: proto.EnumElementContext):
        option_statement = self._(ctx.optionStatement())
        enum_field = self._(ctx.enumField())
        empty_statement = self._(ctx.emptyStatement_())
        return EnumElement(option_statement, enum_field, empty_statement)

    def visitEnumField(self, ctx: proto.EnumFieldContext):
        ident = self._(ctx.ident())
        minus = self._(ctx.MINUS()) is not None
        int_lit = self._(ctx.intLit())
        enum_value_options = self.repeated(ctx, proto.EnumValueOptionsContext)
        return EnumField(ident, minus, int_lit, enum_value_options)

    def visitEnumValueOptions(self, ctx: proto.EnumValueOptionsContext):
        left_enum_value_option = self._(ctx.enumValueOption())
        right_enum_value_option = self.repeated(ctx, proto.EnumValueOptionContext)
        return EnumValueOptions(left_enum_value_option, right_enum_value_option)

    def visitEnumValueOption(self, ctx: proto.EnumValueOptionContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return EnumValueOption(option_name, constant)

    def visitMessageDef(self, ctx: proto.MessageDefContext):
        message_name = self._(ctx.messageName())
        message_body = self._(ctx.messageBody())
        return MessageDef(message_name, message_body)

    def visitMessageBody(self, ctx: proto.MessageBodyContext):
        message_element = self.repeated(ctx, proto.MessageElementContext)
        return MessageBody(message_element)

    def visitMessageElement(self, ctx: proto.MessageElementContext):
        field = self._(ctx.field())
        enum_def = self._(ctx.enumDef())
        message_def = self._(ctx.messageDef())
        extend_def = self._(ctx.extendDef())
        option_statement = self._(ctx.optionStatement())
        oneof = self._(ctx.oneof())
        map_field = self._(ctx.mapField())
        reserved = self._(ctx.reserved())
        empty_statement = self._(ctx.emptyStatement_())
        return MessageElement(field, enum_def, message_def, extend_def, option_statement, oneof, map_field, reserved, empty_statement)

    def visitExtendDef(self, ctx: proto.ExtendDefContext):
        message_type = self._(ctx.messageType())
        field = self.repeated(ctx, proto.FieldContext)
        empty_statement = self.repeated(ctx, proto.EmptyStatement_Context)
        return ExtendDef(message_type, field, empty_statement)

    def visitServiceDef(self, ctx: proto.ServiceDefContext):
        service_name = self._(ctx.serviceName())
        service_element = self.repeated(ctx, proto.ServiceElementContext)
        return ServiceDef(service_name, service_element)

    def visitServiceElement(self, ctx: proto.ServiceElementContext):
        option_statement = self._(ctx.optionStatement())
        rpc = self._(ctx.rpc())
        empty_statement = self._(ctx.emptyStatement_())
        return ServiceElement(option_statement, rpc, empty_statement)

    def visitRpc(self, ctx: proto.RpcContext):
        rpc_name = self._(ctx.rpcName())
        right_stream = self._(ctx.STREAM()) is not None
        third_message_type = self._(ctx.messageType())
        sixth_stream = self._(ctx.STREAM()) is not None
        seventh_message_type = self._(ctx.messageType())
        return Rpc(rpc_name, right_stream, third_message_type, sixth_stream, seventh_message_type)

    def visitConstant(self, ctx: proto.ConstantContext):
        full_ident = self._(ctx.fullIdent())
        minus = self._(ctx.MINUS()) is not None
        plus = self._(ctx.PLUS()) is not None
        int_lit = self._(ctx.intLit())
        float_lit = self._(ctx.floatLit())
        str_lit = self._(ctx.strLit())
        bool_lit = self._(ctx.boolLit())
        block_lit = self._(ctx.blockLit())
        return Constant(full_ident, minus, plus, int_lit, float_lit, str_lit, bool_lit, block_lit)

    def visitBlockLit(self, ctx: proto.BlockLitContext):
        ident = self.repeated(ctx, proto.IdentContext)
        constant = self.repeated(ctx, proto.ConstantContext)
        return BlockLit(ident, constant)

    def visitIdent(self, ctx: proto.IdentContext):
        keywords = self._(ctx.keywords())
        return Ident(keywords)

    def visitFullIdent(self, ctx: proto.FullIdentContext):
        left_ident = self._(ctx.ident())
        right_ident = self.repeated(ctx, proto.IdentContext)
        return FullIdent(left_ident, right_ident)

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
        left_dot = self._(ctx.DOT()) is not None
        ident = self.repeated(ctx, proto.IdentContext)
        message_name = self._(ctx.messageName())
        return MessageType(left_dot, ident, message_name)

    def visitEnumType(self, ctx: proto.EnumTypeContext):
        left_dot = self._(ctx.DOT()) is not None
        ident = self.repeated(ctx, proto.IdentContext)
        enum_name = self._(ctx.enumName())
        return EnumType(left_dot, ident, enum_name)
