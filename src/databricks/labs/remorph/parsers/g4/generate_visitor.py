import collections
import keyword
import pathlib
from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace
from string import punctuation

from databricks.labs.remorph.framework.entrypoint import get_logger, run_main
from databricks.labs.remorph.intermediate.named import Named
from databricks.labs.remorph.parsers.base import TreeNode, TransformStack
from databricks.labs.remorph.parsers.g4 import parse_g4
from databricks.labs.remorph.parsers.g4.g4ast import (
    EBNF,
    Alternative,
    Atom,
    Block,
    Element,
    GrammarSpec,
    ParserRuleSpec,
    RuleRef, PrequelConstruct, Option, OptionValue, LexerAlternative, LexerElement, LexerAtom, LabeledAlt, RuleSpec,
    LexerRuleSpec, LabeledElement,
)

_VISITOR_PREAMBLE = """import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.{package}.generated.{name}Parser import {name}Parser as {package}
from databricks.labs.remorph.parsers.{package}.generated.{name}ParserVisitor import {name}ParserVisitor
from databricks.labs.remorph.parsers.{package}.ast import *


class {name}AST({name}ParserVisitor):
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

_AST_PREAMBLE = """import functools

from dataclasses import dataclass
from databricks.labs.remorph.parsers.base import TreeNode

dataclass = functools.partial(dataclass, slots=True, match_args=True, repr=False, frozen=True)

"""

logger = get_logger(__file__)


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
        field_name = Named(self.field_name).snake_name()
        if keyword.iskeyword(field_name):
            field_name = f'{field_name}_'
        return field_name

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

    def __init__(self, grammar_file: pathlib.Path):
        self.spec: GrammarSpec = parse_g4(grammar_file)
        self._path = grammar_file
        self._package = grammar_file.parent.name
        self._nodes = []
        self._lexer_atoms = []
        self._alias_rules = {}
        self._ast_code = _AST_PREAMBLE
        name = self.spec.decl.name.rstrip('Parser')
        self._visitor_code = _VISITOR_PREAMBLE.format(package=self._package, name=name)
        self._punctuation = set(punctuation) | {f"'{_}'" for _ in punctuation}
        self._implicit_lexer_atoms = []
        self._complex_lexers = []
        self._virtual_visitors = {}

    def process_rules(self):
        self._lexer_rules()
        self._detect_alias_rules()
        self._extract_rules_from_labeled_blocks()
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
        context_name = self._virtual_visitors.get(node.name, node.name)
        context_name = context_name[0].upper() + context_name[1:]
        self._visitor_code += f"""
    def visit{node.title()}(self, ctx: {self._package}.{context_name}Context):
        {visitor_code}
        return {node.pascal_name()}({", ".join(field_names)})
"""
        self._ast_code += f"@dataclass\nclass {node.pascal_name()}(TreeNode):\n    {ast_code}\n\n\n"

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
        self._try_load_token_vocab()
        for rule_spec in self.spec.rules:
            self._match_complex_lexer(rule_spec)
        self._detect_implicit_token_alias_parser_rules()
        for rule_spec in self.spec.rules:
            if not rule_spec.lexer:
                continue
            alternatives = rule_spec.lexer.lexer_block
            if len(alternatives) > 1:
                continue
            lexer_alternative = alternatives[0]
            if len(lexer_alternative.elements) > 1:
                continue
            self._lexer_atoms.append(rule_spec.lexer.token_ref)
        self._lexer_atoms = sorted(self._lexer_atoms)

    def _match_complex_lexer(self, rule_spec: RuleSpec):
        match rule_spec:
            case RuleSpec(_, LexerRuleSpec(token_ref, _, alternatives, _)):
                for lexer_alternative in alternatives:
                    self._match_multielement_lexer_alternative(token_ref, lexer_alternative)

    def _match_multielement_lexer_alternative(self, token_ref: str, lexer_alternative: LexerAlternative):
        match lexer_alternative:
            case LexerAlternative(elements):
                if len(elements) == 1:
                    return
                self._complex_lexers.append(token_ref)

    def _detect_implicit_token_alias_parser_rules(self):
        for r in self.spec.rules:
            match r:
                case RuleSpec(ParserRuleSpec(name, [LabeledAlt(Alternative([Element(atom=Atom(terminal=term))]))])):
                    if not term:
                        # I don't understand why python is so bad at case matching still...
                        continue
                    if term in self._complex_lexers:
                        continue
                    # rules like:
                    #
                    # file_directory_path_separator
                    # : '\\'
                    # ;
                    is_quoted = "'" in term
                    if not is_quoted:
                        continue
                    self._implicit_lexer_atoms.append(name)

    def _try_load_token_vocab(self):
        options = self._prequel_options()
        if 'tokenVocab' in options:
            lexer_grammar = parse_g4(self._path.parent / f'{options["tokenVocab"]}.g4')
            for prequel in lexer_grammar.prequel:
                self.spec.prequel.append(prequel)
            for r in lexer_grammar.rules:
                if not r.lexer:
                    continue
                self.spec.rules.append(r)

    def _prequel_options(self):
        options = {}
        for prequel in self.spec.prequel:
            match prequel:
                case PrequelConstruct(options=[Option(a, OptionValue(b))]):
                    options[a] = '.'.join(b)
        return options

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
        if rule.name in self._implicit_lexer_atoms:
            return None
        return self._unfold_direct_fields(rule)

    def _extract_rules_from_labeled_blocks(self):
        """ Replaces labeled blocks with "virtual types". Translates from:

        > execute_clause
        >     : EXECUTE AS clause=(CALLER | SELF | OWNER | STRING)
        >     ;

        into what we have simpler means of generation:

        < execute_clause:
        <     | EXECUTE AS clause=execute_clause_clause
        <     ;
        < execute_clause_clause:
        <     | CALLER
        <     | SELF
        <     | OWNER
        <     | STRING
        <     ;
        """
        new_rules = []

        def transform_up(node: TreeNode, stack: TransformStack) -> TreeNode:
            match node:
                case Element(labeled_element=LabeledElement(name=label, block=Block(alts, o, a)),
                             zero_or_one=zero_or_one,
                             zero_or_more=zero_or_more,
                             one_or_more=one_or_more,
                             is_non_greedy=is_non_greedy):
                    ebnf = EBNF(Block(alts, o, a),
                                zero_or_one=zero_or_one,
                                zero_or_more=zero_or_more,
                                one_or_more=one_or_more,
                                is_non_greedy=is_non_greedy)
                    parser_rule = stack.skip_levels(ParserRuleSpec)
                    virtual_name = f'{parser_rule.name}_{label}'
                    self._virtual_visitors[virtual_name] = parser_rule.name
                    new_rules.append(RuleSpec(ParserRuleSpec(
                        name=virtual_name,
                        labeled_alternatives=[LabeledAlt(Alternative([Element(ebnf=ebnf)]))]
                    )))
                    return node.replace(atom=Atom(rule_ref=RuleRef(virtual_name)), labeled_element=None)
                case _:
                    return node

        self.spec = self.spec.transform_up_with_path(transform_up)
        self.spec.rules.extend(new_rules)

    def _unfold_direct_fields(self, rule: ParserRuleSpec) -> Node:
        node = Node(rule.name)
        has_alternatives = len(rule.labeled_alternatives) > 1
        for labeled_alternative in rule.labeled_alternatives:
            alternative = labeled_alternative.alternative
            renamer = self._duplicate_field_renamer(alternative)
            for element in self._unfold_elements(alternative, zero_or_one=has_alternatives):
                self._match_element(node, element, renamer)
        return node

    def _match_element(self, node: Node, element: Element, renamer: Callable, label: str = None):
        match element:
            case Element(labeled_element=LabeledElement(name=name, atom=atom)):
                elem = element.replace(atom=atom, labeled_element=None)
                return self._match_element(node, elem, renamer, label=name)
            case Element(atom=Atom(rule_ref=RuleRef(ref=rule_ref))):
                self._add_field_to_node(node, rule_ref, renamer, element, label=label)
            case Element(atom=Atom(terminal=flag)):
                self._add_field_to_node(node, flag, renamer, element, terminal=True, label=label)
            case _:
                raise ValueError(f'unmatched: {element}')

    def _add_field_to_node(self,
                           node: Node,
                           rule_name: str,
                           renamer: Callable[[str], tuple[int, str, str]],
                           element: Element,
                           terminal: bool = False,
                           label: str = None):
        if self._skip_lexer_refs(element, rule_name):
            return
        if terminal and rule_name not in self._lexer_atoms:
            element = replace(element, zero_or_one=False)
        idx, in_context, field_name = renamer(rule_name)
        if label is not None:
            field_name = label
        node.add_field(idx,
                       in_context,
                       field_name,
                       zero_or_one=element.zero_or_one,
                       zero_or_more=element.zero_or_more,
                       one_or_more=element.one_or_more,
                       is_non_greedy=element.is_non_greedy,
                       terminal=terminal)

    def _skip_lexer_refs(self, element: Element, ref: str):
        if ref in self._punctuation:
            # sloppy (or overly complex) grammar,
            # punctuation is added implicitly.
            return True
        if "'" in ref:
            return True
        if ref in self._implicit_lexer_atoms:
            return True
        if ref in self._lexer_atoms:
            if not element.zero_or_one:
                return True
            if element.zero_or_more:
                return True
            if element.one_or_more:
                return True
        return False

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
            current_index = current_counter[name]
            if current_index >= len(renames):
                field_name = f'f{current_index:2}'
            else:
                field_name = renames[current_index]
            current_counter[name] += 1
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

    def __repr__(self):
        return f'VisitorCodeGenerator<{self.spec.decl.name} ({len(self.spec.rules)} rules)>'


def main(grammar_path: str):
    grammar_file = pathlib.Path(grammar_path)
    visitor_target = grammar_file.parent / "visitor.py"
    ast_target = grammar_file.parent / "ast.py"

    visitor_gen = VisitorCodeGenerator(grammar_file)
    visitor_gen.process_rules()

    with visitor_target.open("w") as f:
        f.write(visitor_gen.visitor_code())

    with ast_target.open("w") as f:
        f.write(visitor_gen.ast_code())

    logger.info(f'generated {visitor_target} and {ast_target} from {grammar_file}')


if __name__ == "__main__":
    run_main(main)
