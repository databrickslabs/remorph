import pathlib

import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.g4 import parse_file, ANTLRv4ParserVisitor
from databricks.labs.remorph.parsers.g4.generated.ANTLRv4Parser import ANTLRv4Parser
from databricks.labs.remorph.parsers.g4.g4ast import *


class AntlrAST(ANTLRv4ParserVisitor):
    def visitGrammarSpec(self, ctx: ANTLRv4Parser.GrammarSpecContext):
        grammar_decl = self._(ctx.grammarDecl())
        prequel_construct = self._(ctx.prequelConstruct())
        rules = self._(ctx.rules())
        mode_spec = self._(ctx.modeSpec())
        return GrammarSpec(grammar_decl, rules, prequel_construct, mode_spec)

    def visitGrammarDecl(self, ctx: ANTLRv4Parser.GrammarDeclContext):
        identifier = self._(ctx.identifier())
        grammar_type = self._(ctx.grammarType())
        return GrammarDecl(identifier, grammar_type)

    def visitGrammarType(self, ctx: ANTLRv4Parser.GrammarTypeContext):
        lexer = self._(ctx.LEXER())
        parser = self._(ctx.PARSER())
        grammar = self._(ctx.GRAMMAR())
        return GrammarType(lexer, parser, grammar)

    def visitPrequelConstruct(self, ctx: ANTLRv4Parser.PrequelConstructContext):
        options_spec = self._(ctx.optionsSpec())
        delegate_grammars = self._(ctx.delegateGrammars())
        tokens_spec = self._(ctx.tokensSpec())
        channels_spec = self._(ctx.channelsSpec())
        return PrequelConstruct(options_spec, delegate_grammars, tokens_spec, channels_spec)

    def visitOptionsSpec(self, ctx: ANTLRv4Parser.OptionsSpecContext):
        option_list = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.OptionContext)]
        return option_list

    def visitOption(self, ctx: ANTLRv4Parser.OptionContext):
        identifier = self._(ctx.identifier())
        option_value = self._(ctx.optionValue())
        return Option(identifier, option_value)

    def visitOptionValue(self, ctx: ANTLRv4Parser.OptionValueContext):
        names = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)]
        string_literal = self._(ctx.STRING_LITERAL())
        action_block = self._(ctx.actionBlock())
        number = self._(ctx.INT())
        return OptionValue(names, string_literal, action_block, int(number) if number is not None else None)

    def visitDelegateGrammars(self, ctx: ANTLRv4Parser.DelegateGrammarsContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.DelegateGrammarContext)]

    def visitDelegateGrammar(self, ctx: ANTLRv4Parser.DelegateGrammarContext):
        left = self._(ctx.identifier())
        right = self._(ctx.identifier())
        return DelegateGrammar(left, right)

    def visitTokensSpec(self, ctx: ANTLRv4Parser.TokensSpecContext):
        id_list = self._(ctx.idList())
        return Names(id_list)

    def visitChannelsSpec(self, ctx: ANTLRv4Parser.ChannelsSpecContext):
        id_list = self._(ctx.idList())
        return Names(id_list)

    def visitIdList(self, ctx: ANTLRv4Parser.IdListContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)]

    def visitAction_(self, ctx: ANTLRv4Parser.Action_Context):
        return super().visitAction_(ctx)

    def visitActionScopeName(self, ctx: ANTLRv4Parser.ActionScopeNameContext):
        return super().visitActionScopeName(ctx)

    def visitActionBlock(self, ctx: ANTLRv4Parser.ActionBlockContext):
        return super().visitActionBlock(ctx)

    def visitArgActionBlock(self, ctx: ANTLRv4Parser.ArgActionBlockContext):
        return super().visitArgActionBlock(ctx)

    def visitModeSpec(self, ctx: ANTLRv4Parser.ModeSpecContext):
        identifier = self._(ctx.identifier())
        lexer_rule_spec_list = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.LexerRuleSpecContext)]
        return ModeSpec(identifier, lexer_rule_spec_list)

    def visitRules(self, ctx: ANTLRv4Parser.RulesContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.RuleSpecContext)]

    def visitRuleSpec(self, ctx: ANTLRv4Parser.RuleSpecContext):
        parser_rule_spec = self._(ctx.parserRuleSpec())
        lexer_rule_spec = self._(ctx.lexerRuleSpec())
        return RuleSpec(parser_rule_spec, lexer_rule_spec)

    def visitParserRuleSpec(self, ctx: ANTLRv4Parser.ParserRuleSpecContext):
        rule_ref = self._(ctx.RULE_REF())
        rule_modifiers = self._(ctx.ruleModifiers())
        arg_action_block = self._(ctx.argActionBlock())
        rule_returns = self._(ctx.ruleReturns())
        locals_spec = self._(ctx.localsSpec())
        rule_prequel = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.RulePrequelContext)]
        rule_block = self._(ctx.ruleBlock())
        return ParserRuleSpec(rule_ref, rule_block, rule_modifiers, arg_action_block, rule_returns, locals_spec, rule_prequel)

    def visitRulePrequel(self, ctx: ANTLRv4Parser.RulePrequelContext):
        options_spec = self._(ctx.optionsSpec())
        rule_action = self._(ctx.ruleAction())
        return RulePrequel(options_spec, rule_action)

    def visitRuleReturns(self, ctx: ANTLRv4Parser.RuleReturnsContext):
        return self._(ctx.argActionBlock())

    def visitLocalsSpec(self, ctx: ANTLRv4Parser.LocalsSpecContext):
        return self._(ctx.argActionBlock())

    def visitRuleAction(self, ctx: ANTLRv4Parser.RuleActionContext):
        identifier = self._(ctx.identifier())
        action_block = self._(ctx.actionBlock())
        return RuleAction(identifier, action_block)

    def visitRuleModifiers(self, ctx: ANTLRv4Parser.RuleModifiersContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.RuleModifierContext)]

    def visitRuleModifier(self, ctx: ANTLRv4Parser.RuleModifierContext):
        # this is enum - all caps
        public = self._(ctx.PUBLIC())
        private = self._(ctx.PRIVATE())
        protected = self._(ctx.PROTECTED())
        fragment = self._(ctx.FRAGMENT())
        return RuleModifier(public, private, protected, fragment)

    def visitRuleBlock(self, ctx: ANTLRv4Parser.RuleBlockContext):
        return self._(ctx.ruleAltList())

    def visitRuleAltList(self, ctx: ANTLRv4Parser.RuleAltListContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.LabeledAltContext)]

    def visitLabeledAlt(self, ctx: ANTLRv4Parser.LabeledAltContext):
        alternative = self._(ctx.alternative())
        identifier = self._(ctx.identifier())
        return LabeledAlt(alternative, identifier)

    def visitLexerRuleSpec(self, ctx: ANTLRv4Parser.LexerRuleSpecContext):
        fragment = self._(ctx.FRAGMENT())
        token_ref = self._(ctx.TOKEN_REF())
        options_spec = self._(ctx.optionsSpec())
        lexer_rule_block = self._(ctx.lexerRuleBlock())
        return LexerRuleSpec(token_ref, options_spec, lexer_rule_block, fragment is not None)

    def visitLexerRuleBlock(self, ctx: ANTLRv4Parser.LexerRuleBlockContext):
        return self._(ctx.lexerAltList())

    def visitLexerAltList(self, ctx: ANTLRv4Parser.LexerAltListContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.LexerAltContext)]

    def visitLexerAlt(self, ctx: ANTLRv4Parser.LexerAltContext):
        lexer_elements = self._(ctx.lexerElements())
        lexer_commands = self._(ctx.lexerCommands())
        return LexerAlternative(lexer_elements, lexer_commands)

    def visitLexerElements(self, ctx: ANTLRv4Parser.LexerElementsContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.LexerElementContext)]

    def visitLexerElement(self, ctx: ANTLRv4Parser.LexerElementContext):
        lexer_atom = self._(ctx.lexerAtom())
        lexer_block = self._(ctx.lexerBlock())
        action_block = self._(ctx.actionBlock())
        question = self._(ctx.QUESTION())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = False, False, False, False
        ebnf_suffix = ctx.ebnfSuffix()
        if ebnf_suffix is not None:
            zero_or_one = self._(ebnf_suffix.PLUS()) is not None         # ?
            zero_or_more = self._(ebnf_suffix.STAR()) is not None        # *
            one_or_more = self._(ebnf_suffix.QUESTION(0)) is not None    # +
            is_non_greedy = self._(ebnf_suffix.QUESTION(1)) is not None  # ??

        return LexerElement(lexer_atom, lexer_block, action_block, question is not None,
                            zero_or_one, zero_or_more, one_or_more, is_non_greedy)

    def visitLexerBlock(self, ctx: ANTLRv4Parser.LexerBlockContext):
        return self._(ctx.lexerAltList())

    def visitLexerCommands(self, ctx: ANTLRv4Parser.LexerCommandsContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.LexerCommandContext)]

    def visitLexerCommand(self, ctx: ANTLRv4Parser.LexerCommandContext):
        lexer_command = self._(ctx.lexerCommandName())
        lexer_command_expr = self._(ctx.lexerCommandExpr())
        return LexerCommand(lexer_command, lexer_command_expr)

    def visitLexerCommandName(self, ctx: ANTLRv4Parser.LexerCommandNameContext):
        identifier = self._(ctx.identifier())
        mode = self._(ctx.MODE())
        return LexerCommandName(identifier, mode is not None)

    def visitLexerCommandExpr(self, ctx: ANTLRv4Parser.LexerCommandExprContext):
        identifier = self._(ctx.identifier())
        number = self._(ctx.INT())
        return LexerCommandExpr(identifier, number)

    def visitAltList(self, ctx: ANTLRv4Parser.AltListContext):
        alt_context = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.AlternativeContext)]
        return alt_context

    def visitAlternative(self, ctx: ANTLRv4Parser.AlternativeContext):
        element_list = [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.ElementContext)]
        element_options = self._(ctx.elementOptions())
        return Alternative(element_list, element_options)

    def visitElement(self, ctx: ANTLRv4Parser.ElementContext):
        labeled_element = self._(ctx.labeledElement())
        atom = self._(ctx.atom())
        ebnf = self._(ctx.ebnf())
        action_block = self._(ctx.actionBlock())
        question = self._(ctx.QUESTION())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = False, False, False, False
        ebnf_suffix = ctx.ebnfSuffix()
        if ebnf_suffix is not None:
            zero_or_one = self._(ebnf_suffix.PLUS()) is not None         # ?
            zero_or_more = self._(ebnf_suffix.STAR()) is not None        # *
            one_or_more = self._(ebnf_suffix.QUESTION(0)) is not None    # +
            is_non_greedy = self._(ebnf_suffix.QUESTION(1)) is not None  # ??

        return Element(labeled_element, atom, ebnf, action_block, question is not None,
                       zero_or_one, zero_or_more, one_or_more, is_non_greedy)

    def visitLabeledElement(self, ctx: ANTLRv4Parser.LabeledElementContext):
        name = self._(ctx.identifier())
        assign = self._(ctx.ASSIGN())
        plus_assign = self._(ctx.PLUS_ASSIGN())
        atom = self._(ctx.atom())
        block = self._(ctx.block())
        return LabeledElement(
            name=name,
            assign=assign is not None,
            plus_assign=plus_assign is not None,
            atom=atom,
            block=block)

    def visitEbnf(self, ctx: ANTLRv4Parser.EbnfContext):
        block = self._(ctx.block())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = False, False, False, False
        ebnf_suffix = self._(ctx.blockSuffix())
        if ebnf_suffix is not None:
            zero_or_one = ebnf_suffix == '?'
            zero_or_more = ebnf_suffix == '*'
            one_or_more = ebnf_suffix == '+'
            is_non_greedy = ebnf_suffix == '??'

        return EBNF(block, zero_or_one, zero_or_more, one_or_more, is_non_greedy)

    def visitLexerAtom(self, ctx: ANTLRv4Parser.LexerAtomContext):
        character_range = self._(ctx.characterRange())
        terminal = self._(ctx.terminal())
        not_set = self._(ctx.notSet())
        lexer_char_set = self._(ctx.LEXER_CHAR_SET())
        element_options = self._(ctx.elementOptions())
        return LexerAtom(character_range, terminal, not_set, lexer_char_set, element_options)

    def visitAtom(self, ctx: ANTLRv4Parser.AtomContext):
        rule_ref = self._(ctx.ruleref())
        terminal = self._(ctx.terminal())
        not_set = self._(ctx.notSet())
        element_options = self._(ctx.elementOptions())
        return Atom(rule_ref, terminal, not_set, element_options)

    def visitNotSet(self, ctx: ANTLRv4Parser.NotSetContext):
        set_element = self._(ctx.setElement())
        block_set = self._(ctx.blockSet())
        return NotSet(set_element, block_set)

    def visitBlockSet(self, ctx: ANTLRv4Parser.BlockSetContext):
        return [self._(_) for _ in ctx.getTypedRuleContexts(ANTLRv4Parser.SetElementContext)]

    def visitSetElement(self, ctx: ANTLRv4Parser.SetElementContext):
        token_ref = self._(ctx.TOKEN_REF())
        element_options = self._(ctx.elementOptions())
        string_literal = self._(ctx.STRING_LITERAL())
        character_range = self._(ctx.characterRange())
        lexer_char_set = self._(ctx.LEXER_CHAR_SET())
        return SetElement(token_ref, element_options, string_literal, character_range, lexer_char_set)

    def visitBlock(self, ctx: ANTLRv4Parser.BlockContext):
        options_spec = self._(ctx.optionsSpec())
        rule_action = self._(ctx.ruleAction())
        alt_list = self._(ctx.altList())
        return Block(alt_list, options_spec, rule_action)

    def visitRuleref(self, ctx: ANTLRv4Parser.RulerefContext):
        rule_lef = self._(ctx.RULE_REF())
        action_block = self._(ctx.argActionBlock())
        element_options = self._(ctx.elementOptions())
        return RuleRef(rule_lef, action_block, element_options)

    def visitElementOptions(self, ctx: ANTLRv4Parser.ElementOptionsContext):
        return super().visitElementOptions(ctx)

    def visitElementOption(self, ctx: ANTLRv4Parser.ElementOptionContext):
        left = self._(ctx.identifier(0))
        right = self._(ctx.identifier(1))
        return ElementOption(left, right)

    def visitIdentifier(self, ctx: ANTLRv4Parser.IdentifierContext):
        child = ctx.getChild(0)
        if not child:
            return None
        return child.getText()

    def _(self, ctx: antlr4.ParserRuleContext):
        if not ctx:
            return None
        return self.visit(ctx)

    def visitTerminal(self, ctx: TerminalNodeImpl):
        return ctx.getText()


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

    def visitTerminal(self, ctx: TerminalNodeImpl):
        return ctx.getText()
'''

    def parser_name(self):
        return f'{self.spec.decl.name}Parser'

    def rules(self):
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
    pg = parse_file(grammar_file)

    gen = AntlrAST()
    grammar_spec = pg.accept(gen)

    visitor_gen = VisitorCodeGenerator(grammar_spec, 'proto')

    visitor_gen.rules()

    with (grammar_file.parent / 'visitor.py').open('w') as f:
        f.write(visitor_gen.visitor_code())

    with (grammar_file.parent / 'ast.py').open('w') as f:
        f.write(visitor_gen.ast_code())
    print(1)

