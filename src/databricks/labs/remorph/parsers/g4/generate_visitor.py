import collections
import pathlib
from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace

from databricks.labs.remorph.intermediate.named import Named
from databricks.labs.remorph.parsers.g4 import parse_g4
from databricks.labs.remorph.parsers.g4.g4ast import (
    EBNF,
    Alternative,
    Atom,
    Block,
    Element,
    GrammarSpec,
    ParserRuleSpec,
    RuleRef,
)

_VISITOR_PREAMBLE = """import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.{package}.generated.{name}Parser import {name}Parser as {package}
from databricks.labs.remorph.parsers.{package}.generated.{name}Visitor import {name}Visitor
from databricks.labs.remorph.parsers.{package}.ast import *


class {name}AST({name}Visitor):
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
"""


@dataclass
class Field:
    field_name: str
    in_context: str
    ctx_index: int
    is_optional: bool = False # ?
    is_repeated: bool = False # *
    is_non_greedy: bool = False # ??
    is_terminal: bool = False

    @property
    def is_flag(self) -> bool:
        return self.is_optional and self.is_terminal

    def snake_name(self) -> str:
        return Named(self.field_name).snake_name()

    def title(self):
        return self.in_context[0].upper() + self.in_context[1:]

    def context_name(self):
        return f"{self.title()}Context"


class Node(Named):

    def __init__(self, name: str):
        super().__init__(name)
        self._fields: list[Field] = []
        self._counts = collections.defaultdict(int)
        self._enum = []

    def title(self):
        return self.name[0].upper() + self.name[1:]

    def context_name(self):
        return f"{self.title()}Context"

    def add_field(self,
                  idx: int,
                  in_context: str,
                  field_name: str,
                  *,
                  zero_or_one: bool = False,
                  zero_or_more: bool = False,
                  one_or_more: bool = False,
                  is_non_greedy: bool = False,
                  terminal: bool = False):
        is_repeated = zero_or_more or one_or_more
        field = Field(field_name,
                      in_context,
                      idx,
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
        self._lexer_atoms = []
        self._alias_rules = {}
        self._ast_code = "from databricks.labs.remorph.parsers.base import node\n\n\n"
        self._visitor_code = _VISITOR_PREAMBLE.format(package=package, name=spec.decl.name)

    def process_rules(self):
        self._lexer_rules()
        self._detect_alias_rules()
        for r in self.spec.rules:
            if not r.parser:
                continue
            node = self._rule_to_node(r.parser)
            if not node:
                continue
            self._nodes.append(node)
        for node in self._nodes:
            self._generate_node(node)

    def _generate_node(self, node: Node):
        visitor_fields = []
        ast_fields = []
        field_names = []
        for field in node.fields():
            if not self._is_type_defined(field):
                continue
            if field.is_repeated:
                visitor_fields.append(
                    f"{field.snake_name()} = self.repeated(ctx, {self._package}.{field.context_name()})")
                ast_fields.append(f"{field.snake_name()}: list[{self._type_name(field)}] = None")
            elif field.is_flag:
                visitor_fields.append(f"{field.snake_name()} = self._(ctx.{field.in_context}()) is not None")
                ast_fields.append(f"{field.snake_name()}: bool = False")
            else:
                index = ""
                if node.needs_index(field):
                    index = field.ctx_index
                visitor_fields.append(f"{field.snake_name()} = self._(ctx.{field.in_context}({index}))")
                ast_fields.append(f"{field.snake_name()}: {self._type_name(field)} = None")
            field_names.append(field.snake_name())

        visitor_code = "\n        ".join(visitor_fields)
        ast_code = "\n    ".join(ast_fields)
        self._visitor_code += f"""
    def visit{node.title()}(self, ctx: {self._package}.{node.context_name()}):
        {visitor_code}
        return {node.pascal_name()}({", ".join(field_names)})
"""
        self._ast_code += f"@node\nclass {node.pascal_name()}:\n    {ast_code}\n\n\n"

    def _detect_alias_rules(self):
        for r in self.spec.rules:
            rule = r.parser
            if not rule:
                continue
            alternatives = rule.labeled_alternatives
            if len(alternatives) > 1:
                continue
            elements = alternatives[0].alternative.elements
            if len(elements) > 1:
                continue
            match elements[0]:
                case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                    if not rule_ref:
                        continue
                    self._alias_rules[rule.name] = rule_ref

    def _lexer_rules(self):
        for r in self.spec.rules:
            if not r.lexer:
                continue
            alternatives = r.lexer.lexer_block
            if len(alternatives) > 1:
                continue
            lexer_alternative = alternatives[0]
            if len(lexer_alternative.elements) > 1:
                continue
            self._lexer_atoms.append(r.lexer.token_ref)
        self._lexer_atoms = sorted(self._lexer_atoms)

    def _type_name(self, field: Field) -> str:
        if field.is_terminal:
            return "str"
        pascal_name = Named(self._type_ref(field)).pascal_name()
        return f'"{pascal_name}"'

    def _type_ref(self, field: Field) -> str:
        in_context = field.in_context
        return self._alias_rules.get(in_context, in_context)

    def _is_type_defined(self, field: Field) -> bool:
        if field.is_terminal:
            return True
        ref = self._type_ref(field)
        for node in self._nodes:
            if node.name == ref:
                return True
        return False

    def _has_alternative_labels(self, rule: ParserRuleSpec) -> bool:
        # TODO: has more than one visitor
        for labeled_alternative in rule.labeled_alternatives:
            if labeled_alternative.identifier is not None:
                return True
        return False

    def _rule_to_node(self, rule: ParserRuleSpec) -> Node | None:
        if rule.name in self._alias_rules:
            return None
        return self._unfold_direct_fields(rule)

    def _unfold_direct_fields(self, rule: ParserRuleSpec) -> Node:
        node = Node(rule.name)
        has_alternatives = len(rule.labeled_alternatives) > 1
        for labeled_alternative in rule.labeled_alternatives:
            alternative = labeled_alternative.alternative
            renamer = self._duplicate_field_renamer(alternative)
            for element in self._unfold_elements(alternative, zero_or_one=has_alternatives):
                match element:
                    case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                        self._add_field_to_node(node, rule_ref, renamer, element)
                    case Element(atom=Atom(terminal=flag)):
                        self._add_field_to_node(node, flag, renamer, element, terminal=True)
        return node

    def _add_field_to_node(self,
                           node: Node,
                           rule_name: str,
                           renamer: Callable[[str], tuple[int, str, str]],
                           element: Element,
                           terminal: bool = False):
        if rule_name in self._lexer_atoms:
            if not element.zero_or_one:
                return
            if element.zero_or_more:
                return
            if element.one_or_more:
                return
        if terminal and rule_name not in self._lexer_atoms:
            element = replace(element, zero_or_one=False)
        idx, in_context, field_name = renamer(rule_name)
        node.add_field(idx,
                       in_context,
                       field_name,
                       zero_or_one=element.zero_or_one,
                       zero_or_more=element.zero_or_more,
                       one_or_more=element.one_or_more,
                       is_non_greedy=element.is_non_greedy,
                       terminal=terminal)

    def _duplicate_field_renamer(self, alternative: Alternative) -> Callable[[str], tuple[int, str, str]]:
        child_counter = collections.defaultdict(int)
        for element in self._unfold_elements(alternative):
            match element:
                case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                    child_counter[rule_ref] += 1
                case Element(atom=Atom(terminal=flag), zero_or_one=True):
                    child_counter[flag] += 1
                case Element(atom=Atom(terminal=name)):
                    child_counter[name] += 1

        renames = ["left", "right", "third", "fourth", "fifth"]
        current_counter = collections.defaultdict(int)

        def renamer(name: str) -> tuple[int, str, str]:
            if child_counter[name] < 2:
                return 0, name, name
            current_index = current_counter[rule_ref]
            if current_index == len(renames):
                raise ValueError("cannot rename field")
            field_name = renames[current_index]
            current_counter[rule_ref] += 1
            return current_index, name, field_name

        return renamer

    @classmethod
    def _unfold_elements(cls, alternative: Alternative, zero_or_one: bool = False) -> Iterator[Element]:
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
                            if alt_element.ebnf is not None:
                                element_queue.append(alt_element)
                                continue
                            # element is part of the alternative, so it's always zero or one
                            yield replace(alt_element,
                                          zero_or_one=True,
                                          zero_or_more=ebnf.zero_or_more,
                                          one_or_more=ebnf.one_or_more,
                                          is_non_greedy=ebnf.is_non_greedy,
                                          )
                case _:
                    yield replace(element, zero_or_one=zero_or_one)

    def visitor_code(self):
        return self._visitor_code

    def ast_code(self):
        return self._ast_code


if __name__ == "__main__":
    __dir__ = pathlib.Path(__file__).parent
    grammar_file = __dir__.parent / "proto/Protobuf3.g4"
    grammar_spec = parse_g4(grammar_file)
    visitor_gen = VisitorCodeGenerator(grammar_spec, "proto")

    visitor_gen.process_rules()

    with (grammar_file.parent / "visitor.py").open("w") as f:
        f.write(visitor_gen.visitor_code())

    with (grammar_file.parent / "ast.py").open("w") as f:
        f.write(visitor_gen.ast_code())

    print("done")
