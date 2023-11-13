import antlr4
from antlr4.tree.Tree import TerminalNodeImpl

from databricks.labs.remorph.parsers.g4.g4ast import (
    EBNF,
    Alternative,
    Atom,
    Block,
    DelegateGrammar,
    Element,
    ElementOption,
    GrammarDecl,
    GrammarSpec,
    GrammarType,
    LabeledAlt,
    LabeledElement,
    LexerAlternative,
    LexerAtom,
    LexerCommand,
    LexerCommandExpr,
    LexerCommandName,
    LexerElement,
    LexerRuleSpec,
    ModeSpec,
    Names,
    NotSet,
    Option,
    OptionValue,
    ParserRuleSpec,
    PrequelConstruct,
    RuleAction,
    RuleModifier,
    RulePrequel,
    RuleRef,
    RuleSpec,
    SetElement,
)
from databricks.labs.remorph.parsers.g4.generated.ANTLRv4Parser import ANTLRv4Parser as g4
from databricks.labs.remorph.parsers.g4.generated.ANTLRv4ParserVisitor import ANTLRv4ParserVisitor


class AntlrAST(ANTLRv4ParserVisitor):

    def visitGrammarSpec(self, ctx: g4.GrammarSpecContext):
        grammar_decl = self._(ctx.grammarDecl())
        prequel_construct = self._(ctx.prequelConstruct())
        rules = self._(ctx.rules())
        mode_spec = self._(ctx.modeSpec())
        return GrammarSpec(grammar_decl, rules, prequel_construct, mode_spec)

    def visitGrammarDecl(self, ctx: g4.GrammarDeclContext):
        identifier = self._(ctx.identifier())
        grammar_type = self._(ctx.grammarType())
        return GrammarDecl(identifier, grammar_type)

    def visitGrammarType(self, ctx: g4.GrammarTypeContext):
        lexer = self._(ctx.LEXER())
        parser = self._(ctx.PARSER())
        grammar = self._(ctx.GRAMMAR())
        return GrammarType(lexer, parser, grammar)

    def visitPrequelConstruct(self, ctx: g4.PrequelConstructContext):
        options_spec = self._(ctx.optionsSpec())
        delegate_grammars = self._(ctx.delegateGrammars())
        tokens_spec = self._(ctx.tokensSpec())
        channels_spec = self._(ctx.channelsSpec())
        return PrequelConstruct(options_spec, delegate_grammars, tokens_spec, channels_spec)

    def visitOptionsSpec(self, ctx: g4.OptionsSpecContext):
        option_list = self.repeated(ctx, g4.OptionContext)
        return option_list

    def visitOption(self, ctx: g4.OptionContext):
        identifier = self._(ctx.identifier())
        option_value = self._(ctx.optionValue())
        return Option(identifier, option_value)

    def visitOptionValue(self, ctx: g4.OptionValueContext):
        names = self.repeated(ctx, g4.IdentifierContext)
        string_literal = self._(ctx.STRING_LITERAL())
        action_block = self._(ctx.actionBlock())
        number = self._(ctx.INT())
        return OptionValue(names, string_literal, action_block, int(number) if number is not None else None, )

    def visitDelegateGrammars(self, ctx: g4.DelegateGrammarsContext):
        return self.repeated(ctx, g4.DelegateGrammarContext)

    def visitDelegateGrammar(self, ctx: g4.DelegateGrammarContext):
        left = self._(ctx.identifier())
        right = self._(ctx.identifier())
        return DelegateGrammar(left, right)

    def visitTokensSpec(self, ctx: g4.TokensSpecContext):
        id_list = self._(ctx.idList())
        return Names(id_list)

    def visitChannelsSpec(self, ctx: g4.ChannelsSpecContext):
        id_list = self._(ctx.idList())
        return Names(id_list)

    def visitIdList(self, ctx: g4.IdListContext):
        return self.repeated(ctx, g4.IdentifierContext)

    def visitAction_(self, ctx: g4.Action_Context):
        return super().visitAction_(ctx)

    def visitActionScopeName(self, ctx: g4.ActionScopeNameContext):
        return super().visitActionScopeName(ctx)

    def visitActionBlock(self, ctx: g4.ActionBlockContext):
        return super().visitActionBlock(ctx)

    def visitArgActionBlock(self, ctx: g4.ArgActionBlockContext):
        return super().visitArgActionBlock(ctx)

    def visitModeSpec(self, ctx: g4.ModeSpecContext):
        identifier = self._(ctx.identifier())
        lexer_rule_spec_list = self.repeated(ctx, g4.LexerRuleSpecContext)
        return ModeSpec(identifier, lexer_rule_spec_list)

    def visitRules(self, ctx: g4.RulesContext):
        return self.repeated(ctx, g4.RuleSpecContext)

    def visitRuleSpec(self, ctx: g4.RuleSpecContext):
        parser_rule_spec = self._(ctx.parserRuleSpec())
        lexer_rule_spec = self._(ctx.lexerRuleSpec())
        return RuleSpec(parser_rule_spec, lexer_rule_spec)

    def visitParserRuleSpec(self, ctx: g4.ParserRuleSpecContext):
        rule_ref = self._(ctx.RULE_REF())
        rule_modifiers = self._(ctx.ruleModifiers())
        arg_action_block = self._(ctx.argActionBlock())
        rule_returns = self._(ctx.ruleReturns())
        locals_spec = self._(ctx.localsSpec())
        rule_prequel = self.repeated(ctx, g4.RulePrequelContext)
        rule_block = self._(ctx.ruleBlock())
        return ParserRuleSpec(rule_ref, rule_block, rule_modifiers, arg_action_block, rule_returns,
                              locals_spec, rule_prequel,
                              )

    def visitRulePrequel(self, ctx: g4.RulePrequelContext):
        options_spec = self._(ctx.optionsSpec())
        rule_action = self._(ctx.ruleAction())
        return RulePrequel(options_spec, rule_action)

    def visitRuleReturns(self, ctx: g4.RuleReturnsContext):
        return self._(ctx.argActionBlock())

    def visitLocalsSpec(self, ctx: g4.LocalsSpecContext):
        return self._(ctx.argActionBlock())

    def visitRuleAction(self, ctx: g4.RuleActionContext):
        identifier = self._(ctx.identifier())
        action_block = self._(ctx.actionBlock())
        return RuleAction(identifier, action_block)

    def visitRuleModifiers(self, ctx: g4.RuleModifiersContext):
        return self.repeated(ctx, g4.RuleModifierContext)

    def visitRuleModifier(self, ctx: g4.RuleModifierContext):
        # this is enum - all caps
        public = self._(ctx.PUBLIC())
        private = self._(ctx.PRIVATE())
        protected = self._(ctx.PROTECTED())
        fragment = self._(ctx.FRAGMENT())
        return RuleModifier(public, private, protected, fragment)

    def visitRuleBlock(self, ctx: g4.RuleBlockContext):
        return self._(ctx.ruleAltList())

    def visitRuleAltList(self, ctx: g4.RuleAltListContext):
        return self.repeated(ctx, g4.LabeledAltContext)

    def visitLabeledAlt(self, ctx: g4.LabeledAltContext):
        alternative = self._(ctx.alternative())
        identifier = self._(ctx.identifier())
        return LabeledAlt(alternative, identifier)

    def visitLexerRuleSpec(self, ctx: g4.LexerRuleSpecContext):
        fragment = self._(ctx.FRAGMENT())
        token_ref = self._(ctx.TOKEN_REF())
        options_spec = self._(ctx.optionsSpec())
        lexer_rule_block = self._(ctx.lexerRuleBlock())
        return LexerRuleSpec(token_ref, options_spec, lexer_rule_block, fragment is not None)

    def visitLexerRuleBlock(self, ctx: g4.LexerRuleBlockContext):
        return self._(ctx.lexerAltList())

    def visitLexerAltList(self, ctx: g4.LexerAltListContext):
        return self.repeated(ctx, g4.LexerAltContext)

    def visitLexerAlt(self, ctx: g4.LexerAltContext):
        lexer_elements = self._(ctx.lexerElements())
        lexer_commands = self._(ctx.lexerCommands())
        return LexerAlternative(lexer_elements, lexer_commands)

    def visitLexerElements(self, ctx: g4.LexerElementsContext):
        return self.repeated(ctx, g4.LexerElementContext)

    def visitLexerElement(self, ctx: g4.LexerElementContext):
        lexer_atom = self._(ctx.lexerAtom())
        lexer_block = self._(ctx.lexerBlock())
        action_block = self._(ctx.actionBlock())
        question = self._(ctx.QUESTION())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = (False, False, False, False, )
        ebnf_suffix = ctx.ebnfSuffix()
        if ebnf_suffix is not None:
            zero_or_one = self._(ebnf_suffix.PLUS()) is not None # ?
            zero_or_more = self._(ebnf_suffix.STAR()) is not None # *
            one_or_more = self._(ebnf_suffix.QUESTION(0)) is not None # +
            is_non_greedy = self._(ebnf_suffix.QUESTION(1)) is not None # ??

        return LexerElement(lexer_atom, lexer_block, action_block, question is not None, zero_or_one,
                            zero_or_more, one_or_more, is_non_greedy,
                            )

    def visitLexerBlock(self, ctx: g4.LexerBlockContext):
        return self._(ctx.lexerAltList())

    def visitLexerCommands(self, ctx: g4.LexerCommandsContext):
        return self.repeated(ctx, g4.LexerCommandContext)

    def visitLexerCommand(self, ctx: g4.LexerCommandContext):
        lexer_command = self._(ctx.lexerCommandName())
        lexer_command_expr = self._(ctx.lexerCommandExpr())
        return LexerCommand(lexer_command, lexer_command_expr)

    def visitLexerCommandName(self, ctx: g4.LexerCommandNameContext):
        identifier = self._(ctx.identifier())
        mode = self._(ctx.MODE())
        return LexerCommandName(identifier, mode is not None)

    def visitLexerCommandExpr(self, ctx: g4.LexerCommandExprContext):
        identifier = self._(ctx.identifier())
        number = self._(ctx.INT())
        return LexerCommandExpr(identifier, number)

    def visitAltList(self, ctx: g4.AltListContext):
        alt_context = self.repeated(ctx, g4.AlternativeContext)
        return alt_context

    def visitAlternative(self, ctx: g4.AlternativeContext):
        element_list = self.repeated(ctx, g4.ElementContext)
        element_options = self._(ctx.elementOptions())
        return Alternative(element_list, element_options)

    def visitElement(self, ctx: g4.ElementContext):
        labeled_element = self._(ctx.labeledElement())
        atom = self._(ctx.atom())
        ebnf = self._(ctx.ebnf())
        action_block = self._(ctx.actionBlock())
        question = self._(ctx.QUESTION())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = (False, False, False, False, )
        ebnf_suffix = ctx.ebnfSuffix()
        if ebnf_suffix is not None:
            zero_or_one = self._(ebnf_suffix.PLUS()) is not None # ?
            zero_or_more = self._(ebnf_suffix.STAR()) is not None # *
            one_or_more = self._(ebnf_suffix.QUESTION(0)) is not None # +
            is_non_greedy = self._(ebnf_suffix.QUESTION(1)) is not None # ??

        return Element(labeled_element, atom, ebnf, action_block, question is not None, zero_or_one,
                       zero_or_more, one_or_more, is_non_greedy,
                       )

    def visitLabeledElement(self, ctx: g4.LabeledElementContext):
        name = self._(ctx.identifier())
        assign = self._(ctx.ASSIGN())
        plus_assign = self._(ctx.PLUS_ASSIGN())
        atom = self._(ctx.atom())
        block = self._(ctx.block())
        return LabeledElement(name=name,
                              assign=assign is not None,
                              plus_assign=plus_assign is not None,
                              atom=atom,
                              block=block,
                              )

    def visitEbnf(self, ctx: g4.EbnfContext):
        block = self._(ctx.block())

        zero_or_one, zero_or_more, one_or_more, is_non_greedy = (False, False, False, False, )
        ebnf_suffix = self._(ctx.blockSuffix())
        if ebnf_suffix is not None:
            zero_or_one = ebnf_suffix == "?"
            zero_or_more = ebnf_suffix == "*"
            one_or_more = ebnf_suffix == "+"
            is_non_greedy = ebnf_suffix == "??"

        return EBNF(block, zero_or_one, zero_or_more, one_or_more, is_non_greedy)

    def visitLexerAtom(self, ctx: g4.LexerAtomContext):
        character_range = self._(ctx.characterRange())
        terminal = self._(ctx.terminal())
        not_set = self._(ctx.notSet())
        lexer_char_set = self._(ctx.LEXER_CHAR_SET())
        element_options = self._(ctx.elementOptions())
        return LexerAtom(character_range, terminal, not_set, lexer_char_set, element_options)

    def visitAtom(self, ctx: g4.AtomContext):
        rule_ref = self._(ctx.ruleref())
        terminal = self._(ctx.terminal())
        not_set = self._(ctx.notSet())
        element_options = self._(ctx.elementOptions())
        return Atom(rule_ref, terminal, not_set, element_options)

    def visitNotSet(self, ctx: g4.NotSetContext):
        set_element = self._(ctx.setElement())
        block_set = self._(ctx.blockSet())
        return NotSet(set_element, block_set)

    def visitBlockSet(self, ctx: g4.BlockSetContext):
        return self.repeated(ctx, g4.SetElementContext)

    def visitSetElement(self, ctx: g4.SetElementContext):
        token_ref = self._(ctx.TOKEN_REF())
        element_options = self._(ctx.elementOptions())
        string_literal = self._(ctx.STRING_LITERAL())
        character_range = self._(ctx.characterRange())
        lexer_char_set = self._(ctx.LEXER_CHAR_SET())
        return SetElement(token_ref, element_options, string_literal, character_range, lexer_char_set)

    def visitBlock(self, ctx: g4.BlockContext):
        options_spec = self._(ctx.optionsSpec())
        rule_action = self._(ctx.ruleAction())
        alt_list = self._(ctx.altList())
        return Block(alt_list, options_spec, rule_action)

    def visitRuleref(self, ctx: g4.RulerefContext):
        rule_lef = self._(ctx.RULE_REF())
        action_block = self._(ctx.argActionBlock())
        element_options = self._(ctx.elementOptions())
        return RuleRef(rule_lef, action_block, element_options)

    def visitElementOptions(self, ctx: g4.ElementOptionsContext):
        return super().visitElementOptions(ctx)

    def visitElementOption(self, ctx: g4.ElementOptionContext):
        left = self._(ctx.identifier(0))
        right = self._(ctx.identifier(1))
        return ElementOption(left, right)

    def visitIdentifier(self, ctx: g4.IdentifierContext):
        child = ctx.getChild(0)
        if not child:
            return None
        return child.getText()

    def _(self, ctx: antlr4.ParserRuleContext):
        if not ctx:
            return None
        return self.visit(ctx)

    def repeated(self, ctx: antlr4.ParserRuleContext, ctx_type: type[antlr4.ParserRuleContext]) -> list[any]:
        if not ctx:
            return []
        out = []
        for rc in ctx.getTypedRuleContexts(ctx_type):
            if not rc:
                continue
            mapped = self.visit(rc)
            if not mapped:
                continue
            out.append(mapped)
        return out

    def visitTerminal(self, ctx: TerminalNodeImpl):
        return ctx.getText()
