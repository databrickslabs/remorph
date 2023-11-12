# Generated from src/databricks/labs/remorph/parsers/proto/Protobuf3.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .Protobuf3Parser import Protobuf3Parser
else:
    from Protobuf3Parser import Protobuf3Parser


# This class defines a complete generic visitor for a parse tree produced by Protobuf3Parser.

class Protobuf3Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by Protobuf3Parser#proto.
    def visitProto(self, ctx: Protobuf3Parser.ProtoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#syntax.
    def visitSyntax(self, ctx: Protobuf3Parser.SyntaxContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#importStatement.
    def visitImportStatement(self, ctx: Protobuf3Parser.ImportStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#packageStatement.
    def visitPackageStatement(self, ctx: Protobuf3Parser.PackageStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#optionStatement.
    def visitOptionStatement(self, ctx: Protobuf3Parser.OptionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#optionName.
    def visitOptionName(self, ctx: Protobuf3Parser.OptionNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fieldLabel.
    def visitFieldLabel(self, ctx: Protobuf3Parser.FieldLabelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#field.
    def visitField(self, ctx: Protobuf3Parser.FieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fieldOptions.
    def visitFieldOptions(self, ctx: Protobuf3Parser.FieldOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fieldOption.
    def visitFieldOption(self, ctx: Protobuf3Parser.FieldOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fieldNumber.
    def visitFieldNumber(self, ctx: Protobuf3Parser.FieldNumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#oneof.
    def visitOneof(self, ctx: Protobuf3Parser.OneofContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#oneofField.
    def visitOneofField(self, ctx: Protobuf3Parser.OneofFieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#mapField.
    def visitMapField(self, ctx: Protobuf3Parser.MapFieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#keyType.
    def visitKeyType(self, ctx: Protobuf3Parser.KeyTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#type_.
    def visitType_(self, ctx: Protobuf3Parser.Type_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#reserved.
    def visitReserved(self, ctx: Protobuf3Parser.ReservedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#ranges.
    def visitRanges(self, ctx: Protobuf3Parser.RangesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#range_.
    def visitRange_(self, ctx: Protobuf3Parser.Range_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#reservedFieldNames.
    def visitReservedFieldNames(self, ctx: Protobuf3Parser.ReservedFieldNamesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#topLevelDef.
    def visitTopLevelDef(self, ctx: Protobuf3Parser.TopLevelDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumDef.
    def visitEnumDef(self, ctx: Protobuf3Parser.EnumDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumBody.
    def visitEnumBody(self, ctx: Protobuf3Parser.EnumBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumElement.
    def visitEnumElement(self, ctx: Protobuf3Parser.EnumElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumField.
    def visitEnumField(self, ctx: Protobuf3Parser.EnumFieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumValueOptions.
    def visitEnumValueOptions(self, ctx: Protobuf3Parser.EnumValueOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumValueOption.
    def visitEnumValueOption(self, ctx: Protobuf3Parser.EnumValueOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#messageDef.
    def visitMessageDef(self, ctx: Protobuf3Parser.MessageDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#messageBody.
    def visitMessageBody(self, ctx: Protobuf3Parser.MessageBodyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#messageElement.
    def visitMessageElement(self, ctx: Protobuf3Parser.MessageElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#extendDef.
    def visitExtendDef(self, ctx: Protobuf3Parser.ExtendDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#serviceDef.
    def visitServiceDef(self, ctx: Protobuf3Parser.ServiceDefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#serviceElement.
    def visitServiceElement(self, ctx: Protobuf3Parser.ServiceElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#rpc.
    def visitRpc(self, ctx: Protobuf3Parser.RpcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#constant.
    def visitConstant(self, ctx: Protobuf3Parser.ConstantContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#blockLit.
    def visitBlockLit(self, ctx: Protobuf3Parser.BlockLitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#emptyStatement_.
    def visitEmptyStatement_(self, ctx: Protobuf3Parser.EmptyStatement_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#ident.
    def visitIdent(self, ctx: Protobuf3Parser.IdentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fullIdent.
    def visitFullIdent(self, ctx: Protobuf3Parser.FullIdentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#messageName.
    def visitMessageName(self, ctx: Protobuf3Parser.MessageNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumName.
    def visitEnumName(self, ctx: Protobuf3Parser.EnumNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#fieldName.
    def visitFieldName(self, ctx: Protobuf3Parser.FieldNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#oneofName.
    def visitOneofName(self, ctx: Protobuf3Parser.OneofNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#mapName.
    def visitMapName(self, ctx: Protobuf3Parser.MapNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#serviceName.
    def visitServiceName(self, ctx: Protobuf3Parser.ServiceNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#rpcName.
    def visitRpcName(self, ctx: Protobuf3Parser.RpcNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#messageType.
    def visitMessageType(self, ctx: Protobuf3Parser.MessageTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#enumType.
    def visitEnumType(self, ctx: Protobuf3Parser.EnumTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#intLit.
    def visitIntLit(self, ctx: Protobuf3Parser.IntLitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#strLit.
    def visitStrLit(self, ctx: Protobuf3Parser.StrLitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#boolLit.
    def visitBoolLit(self, ctx: Protobuf3Parser.BoolLitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#floatLit.
    def visitFloatLit(self, ctx: Protobuf3Parser.FloatLitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Protobuf3Parser#keywords.
    def visitKeywords(self, ctx: Protobuf3Parser.KeywordsContext):
        return self.visitChildren(ctx)


del Protobuf3Parser
