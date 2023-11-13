from databricks.labs.remorph.parsers.base import node


@node
class ElementOption:
    left: str
    right: str


@node
class ActionBlock:
    pass


@node
class RuleRef:
    ref: str
    arg_action: ActionBlock = None
    element_options: list[ElementOption] = None


@node
class OptionValue:
    identifiers: list[str] = None
    string_literal: str = None
    action_block: ActionBlock = None
    number: int = None


@node
class Option:
    name: str
    value: OptionValue


@node
class RuleAction:
    name: str
    block: ActionBlock


@node
class CharacterRange:
    start: str
    end: str


@node
class SetElement:
    token_ref: str = None
    element_options: list[ElementOption] = None
    string_literal: str = None
    character_range: CharacterRange = None
    lexer_char_set: str = None


@node
class NotSet:
    set_element: SetElement = None
    block_set: list[SetElement] = None


@node
class Terminal:
    token_ref: str = None
    string_literal: str = None
    element_options: list[ElementOption] = None


@node
class Atom:
    rule_ref: RuleRef = None
    terminal: Terminal = None
    not_set: NotSet = None
    element_options: list[ElementOption] = None


@node
class LexerAtom:
    character_range: CharacterRange = None
    terminal: Terminal = None
    not_set: NotSet = None
    lexer_char_set: str = None
    element_options: list[ElementOption] = None


@node
class LabeledElement:
    name: str
    assign: bool = False
    plus_assign: bool = False
    atom: Atom = None
    block: 'Block' = None


@node
class EBNF:
    block: 'Block'
    zero_or_one: bool = False    # ?
    zero_or_more: bool = False   # *
    one_or_more: bool = False    # +
    is_non_greedy: bool = False  # ??


@node
class Element:
    labeled_element: LabeledElement = None
    atom: Atom = None
    ebnf: EBNF = None
    action_block: ActionBlock = None
    action_question: bool = False
    zero_or_one: bool = False    # ?
    zero_or_more: bool = False   # *
    one_or_more: bool = False    # +
    is_non_greedy: bool = False  # ??


@node
class Alternative:
    elements: list[Element]
    options: list[ElementOption] = None


@node
class Block:
    alternatives: list[Alternative]
    options: list[Option] = None
    rule_actions: list[RuleAction] = None


@node
class LexerCommandExpr:
    name: str = None
    number: int = None


@node
class LexerCommandName:
    name: str = None
    mode: bool = False


@node
class LexerCommand:
    command: LexerCommandName
    expr: LexerCommandExpr = None


@node
class LexerAlternative:
    elements: list['LexerElement']
    commands: list[LexerCommand] = None


@node
class LexerElement:
    lexer_atom: LexerAtom = None
    lexer_block: list[LexerAlternative] = None
    action_block: ActionBlock = None
    action_question: bool = False
    zero_or_one: bool = False    # ?
    zero_or_more: bool = False   # *
    one_or_more: bool = False    # +
    is_non_greedy: bool = False  # ??


@node
class LexerRuleSpec:
    token_ref: str
    options: list[Option] = None
    lexer_block: list[LexerAlternative] = None
    fragment: bool = False


@node
class LabeledAlt:
    alternative: Alternative
    identifier: str = None


@node
class RuleModifier:
    public: bool = False
    private: bool = False
    protected: bool = False
    fragment: bool = False


@node
class RulePrequel:
    options: list[Option] = None
    rule_action: RuleAction = None


@node
class ParserRuleSpec:
    name: str
    labeled_alternatives: list[LabeledAlt]
    modifiers: list[RuleModifier] = None
    arg_action_block: any = None
    returns: any = None
    locals: any = None
    prequel: list[RulePrequel] = None


@node
class RuleSpec:
    parser: ParserRuleSpec
    lexer: LexerRuleSpec


@node
class ModeSpec:
    name: str
    rules: list[LexerRuleSpec]


@node
class Names:
    names: list[str]


@node
class DelegateGrammar:
    name: str
    source: str = None


@node
class PrequelConstruct:
    options: list[Option] = None
    delegate_grammars: list[DelegateGrammar] = None
    tokens_spec: Names = None
    channels_spec: Names = None


@node
class GrammarType:
    lexer: bool = False
    parser: bool = False
    grammar: bool = False


@node
class GrammarDecl:
    name: str
    grammar_type: GrammarType


@node
class GrammarSpec:
    decl: GrammarDecl
    rules: list[RuleSpec]
    prequel: list[PrequelConstruct] = None
    mode: ModeSpec = None

del node