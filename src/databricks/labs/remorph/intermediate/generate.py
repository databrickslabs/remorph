import pathlib

from databricks.labs.remorph.parsers.proto import parse_file, Protobuf3Visitor, Protobuf3Parser


class AstBuilder(Protobuf3Visitor):

    def visitMessageDef(self, ctx: Protobuf3Parser.MessageDefContext):
        name = self.visit(ctx.messageName())
        body = self.visit(ctx.messageBody())
        return None

    def visitField(self, ctx: Protobuf3Parser.FieldContext):
        name = self.visit(ctx.fieldName())
        type = self.visit(ctx.type_())
        return super().visitField(ctx)

    def visitIdent(self, ctx: Protobuf3Parser.IdentContext):
        identifier = ctx.IDENTIFIER()
        if not identifier:
            return None
        return identifier.getText()

    def visitType_(self, ctx: Protobuf3Parser.Type_Context):
        return super().visitType_(ctx)


def main():
    __dir__ = pathlib.Path(__file__).parent
    ast_builder = AstBuilder()
    for proto in (__dir__ / 'proto/spark/connect').glob('*.proto'):
        res = parse_file(proto)
        res.accept(ast_builder)
    print(1)


if __name__ == '__main__':
    main()
