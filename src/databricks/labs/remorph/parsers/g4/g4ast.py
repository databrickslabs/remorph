import functools

from dataclasses import dataclass
from databricks.labs.remorph.parsers.base import TreeNode

dataclass = functools.partial(dataclass, slots=True, match_args=True, repr=False, frozen=True)


@dataclass
class ElementOption(TreeNode):
    left: str
    right: str


@dataclass
class ActionBlock(TreeNode):
    pass


@dataclass
class RuleRef(TreeNode):
    ref: str
    arg_action: ActionBlock = None
    element_options: list[ElementOption] = None


@dataclass
class OptionValue(TreeNode):
    identifiers: list[str] = None
    string_literal: str = None
    action_block: ActionBlock = None
    number: int = None


@dataclass
class Option(TreeNode):
    name: str
    value: OptionValue


@dataclass
class RuleAction(TreeNode):
    name: str
    block: ActionBlock


@dataclass
class CharacterRange(TreeNode):
    start: str
    end: str


@dataclass
class SetElement(TreeNode):
    token_ref: str = None
    element_options: list[ElementOption] = None
    string_literal: str = None
    character_range: CharacterRange = None
    lexer_char_set: str = None


@dataclass
class NotSet(TreeNode):
    set_element: SetElement = None
    block_set: list[SetElement] = None


@dataclass
class Terminal(TreeNode):
    token_ref: str = None
    string_literal: str = None
    element_options: list[ElementOption] = None


@dataclass
class Atom(TreeNode):
    rule_ref: RuleRef = None
    terminal: Terminal = None
    not_set: NotSet = None
    element_options: list[ElementOption] = None


@dataclass
class LexerAtom(TreeNode):
    character_range: CharacterRange = None
    terminal: Terminal = None
    not_set: NotSet = None
    lexer_char_set: str = None
    element_options: list[ElementOption] = None


@dataclass
class LabeledElement(TreeNode):
    name: str
    assign: bool = False
    plus_assign: bool = False
    atom: Atom = None
    block: "Block" = None


@dataclass
class EBNF(TreeNode):
    block: "Block"
    zero_or_one: bool = False # ?
    zero_or_more: bool = False # *
    one_or_more: bool = False # +
    is_non_greedy: bool = False # ??


@dataclass
class Element(TreeNode):
    labeled_element: LabeledElement = None
    atom: Atom = None
    ebnf: EBNF = None
    action_block: ActionBlock = None
    action_question: bool = False
    zero_or_one: bool = False # ?
    zero_or_more: bool = False # *
    one_or_more: bool = False # +
    is_non_greedy: bool = False # ??


@dataclass
class Alternative(TreeNode):
    elements: list[Element]
    options: list[ElementOption] = None


@dataclass
class Block(TreeNode):
    alternatives: list[Alternative]
    options: list[Option] = None
    rule_actions: list[RuleAction] = None


@dataclass
class LexerCommandExpr(TreeNode):
    name: str = None
    number: int = None


@dataclass
class LexerCommandName(TreeNode):
    name: str = None
    mode: bool = False


@dataclass
class LexerCommand(TreeNode):
    command: LexerCommandName
    expr: LexerCommandExpr = None


@dataclass
class LexerAlternative(TreeNode):
    elements: list["LexerElement"]
    commands: list[LexerCommand] = None


@dataclass
class LexerElement(TreeNode):
    lexer_atom: LexerAtom = None
    lexer_block: list[LexerAlternative] = None
    action_block: ActionBlock = None
    action_question: bool = False
    zero_or_one: bool = False # ?
    zero_or_more: bool = False # *
    one_or_more: bool = False # +
    is_non_greedy: bool = False # ??


@dataclass
class LexerRuleSpec(TreeNode):
    token_ref: str
    options: list[Option] = None
    lexer_block: list[LexerAlternative] = None
    fragment: bool = False


@dataclass
class LabeledAlt(TreeNode):
    alternative: Alternative
    identifier: str = None


@dataclass
class RuleModifier(TreeNode):
    public: bool = False
    private: bool = False
    protected: bool = False
    fragment: bool = False


@dataclass
class RulePrequel(TreeNode):
    options: list[Option] = None
    rule_action: RuleAction = None


@dataclass
class ParserRuleSpec(TreeNode):
    name: str
    labeled_alternatives: list[LabeledAlt]
    modifiers: list[RuleModifier] = None
    arg_action_block: any = None
    returns: any = None
    locals: any = None
    prequel: list[RulePrequel] = None


@dataclass
class RuleSpec(TreeNode):
    parser: ParserRuleSpec = None
    lexer: LexerRuleSpec = None


@dataclass
class ModeSpec(TreeNode):
    name: str
    rules: list[LexerRuleSpec]


@dataclass
class Names(TreeNode):
    names: list[str]


@dataclass
class DelegateGrammar(TreeNode):
    name: str
    source: str = None


@dataclass
class PrequelConstruct(TreeNode):
    options: list[Option] = None
    delegate_grammars: list[DelegateGrammar] = None
    tokens_spec: Names = None
    channels_spec: Names = None


@dataclass
class GrammarType(TreeNode):
    lexer: bool = False
    parser: bool = False
    grammar: bool = False


@dataclass
class GrammarDecl(TreeNode):
    name: str
    grammar_type: GrammarType


@dataclass
class GrammarSpec(TreeNode):
    decl: GrammarDecl
    rules: list[RuleSpec]
    prequel: list[PrequelConstruct] = None
    mode: ModeSpec = None

