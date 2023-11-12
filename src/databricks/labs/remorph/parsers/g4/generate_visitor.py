import pathlib

from databricks.labs.remorph.parsers.g4 import parse_file
from databricks.labs.remorph.parsers.g4.g4ast import *
from databricks.labs.remorph.parsers.g4.visitor import AntlrAST


class VisitorCodeGenerator:
    def __init__(self, spec: GrammarSpec, package: str):
        self.spec = spec
        self._package = package
        self._ast_code = f'''
from databricks.labs.remorph.parsers.ast import node

'''
        self._visitor_code = f'''import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.{package}.generated.{spec.decl.name}Parser import {spec.decl.name}Parser as {package}
from databricks.labs.remorph.parsers.{package}.generated.{spec.decl.name}Visitor import {spec.decl.name}Visitor
from databricks.labs.remorph.parsers.{package}.ast import *


class {spec.decl.name}AST({spec.decl.name}Visitor):
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
'''

    def parser_name(self):
        return f'{self.spec.decl.name}Parser'

    def process_rules(self):
        for r in self.spec.rules:
            if not r.parser:
                continue
            self.parser_rule(r.parser)

    def parser_rule(self, rule: ParserRuleSpec):
        title = rule.name[0].upper() + rule.name[1:]
        node_name = Named(rule.name).pascal_name()
        visitor_fields = []
        ast_fields = []
        field_names = []
        for field in rule.fields():
            visitor_fields.append(f'{field.snake_name()} = self._(ctx.{field.name}())')
            ast_fields.append(f'{field.snake_name()}: any = None')
            field_names.append(field.snake_name())

        if not field_names:
            return

        visitor_code = "\n        ".join(visitor_fields)
        ast_code = "\n    ".join(ast_fields)
        self._visitor_code += f'''
    def visit{title}(self, ctx: {self._package}.{title}Context):
        {visitor_code}
        return {node_name}({", ".join(field_names)})
'''
        self._ast_code += f'''
@node
class {node_name}:
    {ast_code}
'''

    def visitor_code(self):
        return self._visitor_code

    def ast_code(self):
        return self._ast_code


if __name__ == '__main__':
    __dir__ = pathlib.Path(__file__).parent
    grammar_file = __dir__.parent / 'proto/Protobuf3.g4'
    parsed_grammar = parse_file(grammar_file)
    grammar_spec = parsed_grammar.accept(AntlrAST())
    visitor_gen = VisitorCodeGenerator(grammar_spec, 'proto')

    visitor_gen.process_rules()

    with (grammar_file.parent / 'visitor.py').open('w') as f:
        f.write(visitor_gen.visitor_code())

    with (grammar_file.parent / 'ast.py').open('w') as f:
        f.write(visitor_gen.ast_code())

    print('done')

