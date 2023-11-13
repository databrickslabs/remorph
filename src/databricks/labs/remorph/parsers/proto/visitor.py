import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.proto.generated.Protobuf3Parser import Protobuf3Parser as proto
from databricks.labs.remorph.parsers.proto.generated.Protobuf3Visitor import Protobuf3Visitor
from databricks.labs.remorph.parsers.proto.ast import *


class Protobuf3AST(Protobuf3Visitor):
    def _(self, ctx: antlr4.ParserRuleContext):
        if not ctx:
            return None
        if type(ctx) == list: # TODO: looks like a hack, but it's still better
            return [self.visit(_) for _ in ctx]
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
        eof = self._(ctx.EOF())
        return Proto(syntax, import_statement, package_statement, option_statement, top_level_def, empty_statement, eof)

    def visitSyntax(self, ctx: proto.SyntaxContext):
        proto3_lit_single = self._(ctx.PROTO3_LIT_SINGLE()) is not None
        proto3_lit_dobule = self._(ctx.PROTO3_LIT_DOBULE()) is not None
        return Syntax(proto3_lit_single, proto3_lit_dobule)

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
        full_ident = self._(ctx.fullIdent(0))
        lp = self._(ctx.LP()) is not None
        rp = self._(ctx.RP()) is not None
        dot = self._(ctx.DOT()) is not None
        right = self._(ctx.fullIdent(1))
        return OptionName(full_ident, lp, rp, dot, right)

    def visitFieldLabel(self, ctx: proto.FieldLabelContext):
        optional = self._(ctx.OPTIONAL()) is not None
        repeated = self._(ctx.REPEATED()) is not None
        return FieldLabel(optional, repeated)

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
        left = self._(ctx.fieldOption(0))
        right = self.repeated(ctx, proto.FieldOptionContext)
        return FieldOptions(left, right)

    def visitFieldOption(self, ctx: proto.FieldOptionContext):
        option_name = self._(ctx.optionName())
        constant = self._(ctx.constant())
        return FieldOption(option_name, constant)

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

    def visitKeyType(self, ctx: proto.KeyTypeContext):
        int32 = self._(ctx.INT32()) is not None
        int64 = self._(ctx.INT64()) is not None
        uint32 = self._(ctx.UINT32()) is not None
        uint64 = self._(ctx.UINT64()) is not None
        sint32 = self._(ctx.SINT32()) is not None
        sint64 = self._(ctx.SINT64()) is not None
        fixed32 = self._(ctx.FIXED32()) is not None
        fixed64 = self._(ctx.FIXED64()) is not None
        sfixed32 = self._(ctx.SFIXED32()) is not None
        sfixed64 = self._(ctx.SFIXED64()) is not None
        bool_ = self._(ctx.BOOL()) is not None
        string = self._(ctx.STRING()) is not None
        return KeyType(int32, int64, uint32, uint64, sint32, sint64, fixed32, fixed64, sfixed32, sfixed64, bool_, string)

    def visitType_(self, ctx: proto.Type_Context):
        double = self._(ctx.DOUBLE()) is not None
        float = self._(ctx.FLOAT()) is not None
        int32 = self._(ctx.INT32()) is not None
        int64 = self._(ctx.INT64()) is not None
        uint32 = self._(ctx.UINT32()) is not None
        uint64 = self._(ctx.UINT64()) is not None
        sint32 = self._(ctx.SINT32()) is not None
        sint64 = self._(ctx.SINT64()) is not None
        fixed32 = self._(ctx.FIXED32()) is not None
        fixed64 = self._(ctx.FIXED64()) is not None
        sfixed32 = self._(ctx.SFIXED32()) is not None
        sfixed64 = self._(ctx.SFIXED64()) is not None
        bool_ = self._(ctx.BOOL()) is not None
        string = self._(ctx.STRING()) is not None
        bytes = self._(ctx.BYTES()) is not None
        message_type = self._(ctx.messageType())
        enum_type = self._(ctx.enumType())
        return Type(double, float, int32, int64, uint32, uint64, sint32, sint64, fixed32, fixed64, sfixed32, sfixed64, bool_, string, bytes, message_type, enum_type)

    def visitReserved(self, ctx: proto.ReservedContext):
        ranges = self._(ctx.ranges())
        reserved_field_names = self._(ctx.reservedFieldNames())
        return Reserved(ranges, reserved_field_names)

    def visitRanges(self, ctx: proto.RangesContext):
        left = self._(ctx.range_(0))
        right = self.repeated(ctx, proto.Range_Context)
        return Ranges(left, right)

    def visitRange_(self, ctx: proto.Range_Context):
        left = self._(ctx.intLit(0))
        to = self._(ctx.TO()) is not None
        right = self._(ctx.intLit(1))
        max = self._(ctx.MAX()) is not None
        return Range(left, to, right, max)

    def visitReservedFieldNames(self, ctx: proto.ReservedFieldNamesContext):
        left = self._(ctx.strLit(0))
        right = self.repeated(ctx, proto.StrLitContext)
        return ReservedFieldNames(left, right)

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
        left = self._(ctx.enumValueOption(0))
        right = self.repeated(ctx, proto.EnumValueOptionContext)
        return EnumValueOptions(left, right)

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
        left = self._(ctx.STREAM()) is not None
        right = self._(ctx.messageType(1))
        third = self._(ctx.STREAM()) is not None
        fourth = self._(ctx.messageType(3))
        lc = self._(ctx.LC()) is not None
        rc = self._(ctx.RC()) is not None
        semi = self._(ctx.SEMI()) is not None
        option_statement = self.repeated(ctx, proto.OptionStatementContext)
        empty_statement = self.repeated(ctx, proto.EmptyStatement_Context)
        return Rpc(rpc_name, left, right, third, fourth, lc, rc, semi, option_statement, empty_statement)

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
        identifier = self._(ctx.IDENTIFIER())
        keywords = self._(ctx.keywords())
        return Ident(identifier, keywords)

    def visitFullIdent(self, ctx: proto.FullIdentContext):
        left = self._(ctx.ident(0))
        right = self.repeated(ctx, proto.IdentContext)
        return FullIdent(left, right)

    def visitMessageType(self, ctx: proto.MessageTypeContext):
        left = self._(ctx.DOT()) is not None
        ident = self.repeated(ctx, proto.IdentContext)
        message_name = self._(ctx.messageName())
        return MessageType(left, ident, message_name)

    def visitEnumType(self, ctx: proto.EnumTypeContext):
        left = self._(ctx.DOT()) is not None
        ident = self.repeated(ctx, proto.IdentContext)
        enum_name = self._(ctx.enumName())
        return EnumType(left, ident, enum_name)

    def visitIntLit(self, ctx: proto.IntLitContext):
        int_lit = self._(ctx.INT_LIT())
        return IntLit(int_lit)

    def visitStrLit(self, ctx: proto.StrLitContext):
        str_lit = self._(ctx.STR_LIT())
        proto3_lit_single = self._(ctx.PROTO3_LIT_SINGLE()) is not None
        proto3_lit_dobule = self._(ctx.PROTO3_LIT_DOBULE()) is not None
        return StrLit(str_lit, proto3_lit_single, proto3_lit_dobule)

    def visitBoolLit(self, ctx: proto.BoolLitContext):
        bool_lit = self._(ctx.BOOL_LIT())
        return BoolLit(bool_lit)

    def visitFloatLit(self, ctx: proto.FloatLitContext):
        float_lit = self._(ctx.FLOAT_LIT())
        return FloatLit(float_lit)

    def visitKeywords(self, ctx: proto.KeywordsContext):
        syntax = self._(ctx.SYNTAX()) is not None
        import_ = self._(ctx.IMPORT()) is not None
        weak = self._(ctx.WEAK()) is not None
        public = self._(ctx.PUBLIC()) is not None
        package_ = self._(ctx.PACKAGE()) is not None
        option = self._(ctx.OPTION()) is not None
        optional = self._(ctx.OPTIONAL()) is not None
        repeated = self._(ctx.REPEATED()) is not None
        oneof = self._(ctx.ONEOF()) is not None
        map_ = self._(ctx.MAP()) is not None
        int32 = self._(ctx.INT32()) is not None
        int64 = self._(ctx.INT64()) is not None
        uint32 = self._(ctx.UINT32()) is not None
        uint64 = self._(ctx.UINT64()) is not None
        sint32 = self._(ctx.SINT32()) is not None
        sint64 = self._(ctx.SINT64()) is not None
        fixed32 = self._(ctx.FIXED32()) is not None
        fixed64 = self._(ctx.FIXED64()) is not None
        sfixed32 = self._(ctx.SFIXED32()) is not None
        sfixed64 = self._(ctx.SFIXED64()) is not None
        bool_ = self._(ctx.BOOL()) is not None
        string = self._(ctx.STRING()) is not None
        double = self._(ctx.DOUBLE()) is not None
        float = self._(ctx.FLOAT()) is not None
        bytes = self._(ctx.BYTES()) is not None
        reserved = self._(ctx.RESERVED()) is not None
        to = self._(ctx.TO()) is not None
        max = self._(ctx.MAX()) is not None
        enum = self._(ctx.ENUM()) is not None
        message = self._(ctx.MESSAGE()) is not None
        service = self._(ctx.SERVICE()) is not None
        extend = self._(ctx.EXTEND()) is not None
        rpc = self._(ctx.RPC()) is not None
        stream = self._(ctx.STREAM()) is not None
        returns = self._(ctx.RETURNS()) is not None
        bool_lit = self._(ctx.BOOL_LIT())
        return Keywords(syntax, import_, weak, public, package_, option, optional, repeated, oneof, map_, int32, int64, uint32, uint64, sint32, sint64, fixed32, fixed64, sfixed32, sfixed64, bool_, string, double, float, bytes, reserved, to, max, enum, message, service, extend, rpc, stream, returns, bool_lit)
