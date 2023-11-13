import collections
import pathlib
from dataclasses import dataclass
from typing import Callable

from databricks.labs.remorph.parsers.g4 import parse_file
from databricks.labs.remorph.parsers.g4.g4ast import *
from databricks.labs.remorph.parsers.g4.visitor import AntlrAST


@dataclass
class Field:
    field_name: str
    in_context: str
    ctx_index: int
    is_optional: bool = False  # ?
    is_repeated: bool = False  # *
    is_non_greedy: bool = False  # ??
    is_terminal: bool = False

    @property
    def is_flag(self) -> bool:
        return self.is_optional and self.is_terminal

    def snake_name(self) -> str:
        return Named(self.field_name).snake_name()

    def pascal_name(self) -> str:
        return Named(self.in_context).pascal_name()

    def type_ref(self) -> str:
        if self.is_terminal:
            return 'str'
        return f"'{self.pascal_name()}'"

    def title(self):
        return self.in_context[0].upper() + self.in_context[1:]

    def context_name(self):
        return f'{self.title()}Context'


class Node(Named):
    def __init__(self, name: str):
        super().__init__(name)
        self._fields: list[Field] = []
        self._counts = collections.defaultdict(int)
        self._enum = []

    def title(self):
        return self.name[0].upper() + self.name[1:]

    def context_name(self):
        return f'{self.title()}Context'

    def add_field(self, idx: int, in_context: str, field_name: str, zero_or_one: bool = False,
                  zero_or_more: bool = False,
                  one_or_more: bool = False,
                  is_non_greedy: bool = False, terminal: bool = False):
        is_repeated = zero_or_more or one_or_more
        field = Field(field_name, in_context, idx,
                      is_optional=zero_or_one,
                      is_repeated=is_repeated,
                      is_non_greedy=is_non_greedy,
                      is_terminal=terminal)
        for existing in self._fields:
            if in_context == existing.in_context and idx == existing.ctx_index:
                return
        self._fields.append(field)
        self._counts[field.in_context] += 1

    def needs_index(self, field: Field) -> bool:
        return self._counts[field.in_context] > 1

    def add_enum(self, name: str):
        self._enum.append(Named(name))

    def fields(self) -> list[Field]:
        return self._fields

    def __len__(self):
        return len(self._fields)

    def __repr__(self):
        fields = [_.in_context for _ in self.fields()]
        return f'{self.pascal_name()}({",".join(fields)})'


class VisitorCodeGenerator:
    def __init__(self, spec: GrammarSpec, package: str):
        self.spec = spec
        self._package = package
        self._nodes = []
        self._lexer_atoms = {}
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
'''

    def parser_name(self):
        return f'{self.spec.decl.name}Parser'

    def process_rules(self):
        for r in self.spec.rules:
            if not r.lexer:
                continue
            alternatives = r.lexer.lexer_block
            if len(alternatives) > 1:
                continue
            lexer_alternative = alternatives[0]
            if len(lexer_alternative.elements) > 1:
                continue
            self._lexer_atoms[r.lexer.token_ref] = len(alternatives)
        for r in self.spec.rules:
            if not r.parser:
                continue
            node = self._rule_to_node(r.parser)
            if not node:
                continue
            self._nodes.append(node)
        for node in self._nodes:
            self.generate_node(node)

    def generate_node(self, node: Node):
        visitor_fields = []
        ast_fields = []
        field_names = []
        for field in node.fields():
            if field.is_repeated:
                visitor_fields.append(
                    f'{field.snake_name()} = self.repeated(ctx, {self._package}.{field.context_name()})')
                ast_fields.append(f"{field.snake_name()}: list['{field.pascal_name()}'] = None")
            elif field.is_flag:
                visitor_fields.append(f'{field.snake_name()} = self._(ctx.{field.in_context}()) is not None')
                ast_fields.append(f'{field.snake_name()}: bool = False')
            else:
                index = ''
                if node.needs_index(field):
                    index = field.ctx_index
                visitor_fields.append(f'{field.snake_name()} = self._(ctx.{field.in_context}({index}))')
                ast_fields.append(f"{field.snake_name()}: {field.type_ref()} = None")
            field_names.append(field.snake_name())

        visitor_code = "\n        ".join(visitor_fields)
        ast_code = "\n    ".join(ast_fields)
        self._visitor_code += f'''
    def visit{node.title()}(self, ctx: {self._package}.{node.context_name()}):
        {visitor_code}
        return {node.pascal_name()}({", ".join(field_names)})
'''
        self._ast_code += f'''
@node
class {node.pascal_name()}:
    {ast_code}
'''

    def _has_alternative_labels(self, rule: ParserRuleSpec) -> bool:
        # TODO: has more than one visitor
        for labeled_alternative in rule.labeled_alternatives:
            if labeled_alternative.identifier is not None:
                return True
        return False

    def _rule_to_node(self, rule: ParserRuleSpec) -> Node:
        return self._unfold_direct_fields(rule)

    def _unfold_direct_fields(self, rule: ParserRuleSpec) -> Node:
        node = Node(rule.name)
        for labeled_alternative in rule.labeled_alternatives:
            alternative = labeled_alternative.alternative
            renamer = self._duplicate_field_renamer(alternative)
            for element in self._unfold_elements(alternative):
                match element:
                    case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                        idx, in_context, field_name = renamer(rule_ref)
                        node.add_field(idx, in_context, field_name,
                                       zero_or_one=element.zero_or_one,
                                       zero_or_more=element.zero_or_more,
                                       one_or_more=element.one_or_more,
                                       is_non_greedy=element.is_non_greedy)
                    case Element(atom=Atom(terminal=flag)):
                        if flag in self._lexer_atoms:
                            continue
                        idx, in_context, field_name = renamer(flag)
                        # TODO: remove those non-flags with one alternative
                        node.add_field(idx, in_context, field_name,
                                       zero_or_one=element.zero_or_one,
                                       zero_or_more=element.zero_or_more,
                                       one_or_more=element.one_or_more,
                                       is_non_greedy=element.is_non_greedy,
                                       terminal=True)
        return node

    def _duplicate_field_renamer(self, alternative: Alternative) -> Callable[[str], tuple[int, str, str]]:
        child_counter = collections.defaultdict(int)
        for element in self._unfold_elements(alternative):
            match element:
                case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                    # if rule_ref in self._lexer_rules:
                    #     continue
                    child_counter[rule_ref] += 1
                case Element(atom=Atom(terminal=flag), zero_or_one=True):
                    child_counter[flag] += 1
                case Element(atom=Atom(terminal=name)):
                    child_counter[name] += 1

        renames = ['left', 'right', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
        current_counter = collections.defaultdict(int)

        def renamer(name: str) -> tuple[int, str, str]:
            if child_counter[name] < 2:
                return 0, name, name
            current_index = current_counter[rule_ref]
            if current_index == len(renames):
                raise ValueError('cannot rename field')
            field_name = renames[current_index]
            current_counter[rule_ref] += 1
            return current_index, name, field_name

        return renamer

    @classmethod
    def _unfold_elements(cls, alternative: Alternative) -> Iterator[Element]:
        element_queue = []
        element_queue.extend(alternative.elements)
        default_ebnf = EBNF(Block([]))
        while element_queue:
            element = element_queue.pop(0)
            match element:
                case Element(ebnf=EBNF(block=Block(alternatives=alternatives))):
                    ebnf = element.ebnf
                    if not ebnf:
                        ebnf = default_ebnf
                    for nested_alternative in alternatives:
                        for alt_element in nested_alternative.elements:
                            yield replace(alt_element,
                                          zero_or_one=ebnf.zero_or_one,
                                          zero_or_more=ebnf.zero_or_more,
                                          one_or_more=ebnf.one_or_more,
                                          is_non_greedy=ebnf.is_non_greedy)
                case _:
                    yield element

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
