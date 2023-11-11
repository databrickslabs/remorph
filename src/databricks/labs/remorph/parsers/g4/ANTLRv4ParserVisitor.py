# Generated from antlr4/g4/ANTLRv4Parser.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .ANTLRv4Parser import ANTLRv4Parser
else:
    from ANTLRv4Parser import ANTLRv4Parser


# This class defines a complete generic visitor for a parse tree produced by ANTLRv4Parser.

class ANTLRv4ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ANTLRv4Parser#grammarSpec.
    def visitGrammarSpec(self, ctx: ANTLRv4Parser.GrammarSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#grammarDecl.
    def visitGrammarDecl(self, ctx: ANTLRv4Parser.GrammarDeclContext):
        ctx.identifier()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#grammarType.
    def visitGrammarType(self, ctx: ANTLRv4Parser.GrammarTypeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#prequelConstruct.
    def visitPrequelConstruct(self, ctx: ANTLRv4Parser.PrequelConstructContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#optionsSpec.
    def visitOptionsSpec(self, ctx: ANTLRv4Parser.OptionsSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#option.
    def visitOption(self, ctx: ANTLRv4Parser.OptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#optionValue.
    def visitOptionValue(self, ctx: ANTLRv4Parser.OptionValueContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#delegateGrammars.
    def visitDelegateGrammars(self, ctx: ANTLRv4Parser.DelegateGrammarsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#delegateGrammar.
    def visitDelegateGrammar(self, ctx: ANTLRv4Parser.DelegateGrammarContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#tokensSpec.
    def visitTokensSpec(self, ctx: ANTLRv4Parser.TokensSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#channelsSpec.
    def visitChannelsSpec(self, ctx: ANTLRv4Parser.ChannelsSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#idList.
    def visitIdList(self, ctx: ANTLRv4Parser.IdListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#action_.
    def visitAction_(self, ctx: ANTLRv4Parser.Action_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#actionScopeName.
    def visitActionScopeName(self, ctx: ANTLRv4Parser.ActionScopeNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#actionBlock.
    def visitActionBlock(self, ctx: ANTLRv4Parser.ActionBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#argActionBlock.
    def visitArgActionBlock(self, ctx: ANTLRv4Parser.ArgActionBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#modeSpec.
    def visitModeSpec(self, ctx: ANTLRv4Parser.ModeSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#rules.
    def visitRules(self, ctx: ANTLRv4Parser.RulesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleSpec.
    def visitRuleSpec(self, ctx: ANTLRv4Parser.RuleSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#parserRuleSpec.
    def visitParserRuleSpec(self, ctx: ANTLRv4Parser.ParserRuleSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#exceptionGroup.
    def visitExceptionGroup(self, ctx: ANTLRv4Parser.ExceptionGroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#exceptionHandler.
    def visitExceptionHandler(self, ctx: ANTLRv4Parser.ExceptionHandlerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#finallyClause.
    def visitFinallyClause(self, ctx: ANTLRv4Parser.FinallyClauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#rulePrequel.
    def visitRulePrequel(self, ctx: ANTLRv4Parser.RulePrequelContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleReturns.
    def visitRuleReturns(self, ctx: ANTLRv4Parser.RuleReturnsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#throwsSpec.
    def visitThrowsSpec(self, ctx: ANTLRv4Parser.ThrowsSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#localsSpec.
    def visitLocalsSpec(self, ctx: ANTLRv4Parser.LocalsSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleAction.
    def visitRuleAction(self, ctx: ANTLRv4Parser.RuleActionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleModifiers.
    def visitRuleModifiers(self, ctx: ANTLRv4Parser.RuleModifiersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleModifier.
    def visitRuleModifier(self, ctx: ANTLRv4Parser.RuleModifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleBlock.
    def visitRuleBlock(self, ctx: ANTLRv4Parser.RuleBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleAltList.
    def visitRuleAltList(self, ctx: ANTLRv4Parser.RuleAltListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#labeledAlt.
    def visitLabeledAlt(self, ctx: ANTLRv4Parser.LabeledAltContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerRuleSpec.
    def visitLexerRuleSpec(self, ctx: ANTLRv4Parser.LexerRuleSpecContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerRuleBlock.
    def visitLexerRuleBlock(self, ctx: ANTLRv4Parser.LexerRuleBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerAltList.
    def visitLexerAltList(self, ctx: ANTLRv4Parser.LexerAltListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerAlt.
    def visitLexerAlt(self, ctx: ANTLRv4Parser.LexerAltContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerElements.
    def visitLexerElements(self, ctx: ANTLRv4Parser.LexerElementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerElement.
    def visitLexerElement(self, ctx: ANTLRv4Parser.LexerElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerBlock.
    def visitLexerBlock(self, ctx: ANTLRv4Parser.LexerBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerCommands.
    def visitLexerCommands(self, ctx: ANTLRv4Parser.LexerCommandsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerCommand.
    def visitLexerCommand(self, ctx: ANTLRv4Parser.LexerCommandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerCommandName.
    def visitLexerCommandName(self, ctx: ANTLRv4Parser.LexerCommandNameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerCommandExpr.
    def visitLexerCommandExpr(self, ctx: ANTLRv4Parser.LexerCommandExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#altList.
    def visitAltList(self, ctx: ANTLRv4Parser.AltListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#alternative.
    def visitAlternative(self, ctx: ANTLRv4Parser.AlternativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#element.
    def visitElement(self, ctx: ANTLRv4Parser.ElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#labeledElement.
    def visitLabeledElement(self, ctx: ANTLRv4Parser.LabeledElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ebnf.
    def visitEbnf(self, ctx: ANTLRv4Parser.EbnfContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#blockSuffix.
    def visitBlockSuffix(self, ctx: ANTLRv4Parser.BlockSuffixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ebnfSuffix.
    def visitEbnfSuffix(self, ctx: ANTLRv4Parser.EbnfSuffixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#lexerAtom.
    def visitLexerAtom(self, ctx: ANTLRv4Parser.LexerAtomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#atom.
    def visitAtom(self, ctx: ANTLRv4Parser.AtomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#notSet.
    def visitNotSet(self, ctx: ANTLRv4Parser.NotSetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#blockSet.
    def visitBlockSet(self, ctx: ANTLRv4Parser.BlockSetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#setElement.
    def visitSetElement(self, ctx: ANTLRv4Parser.SetElementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#block.
    def visitBlock(self, ctx: ANTLRv4Parser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#ruleref.
    def visitRuleref(self, ctx: ANTLRv4Parser.RulerefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#characterRange.
    def visitCharacterRange(self, ctx: ANTLRv4Parser.CharacterRangeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#terminal.
    def visitTerminal(self, ctx: ANTLRv4Parser.TerminalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#elementOptions.
    def visitElementOptions(self, ctx: ANTLRv4Parser.ElementOptionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#elementOption.
    def visitElementOption(self, ctx: ANTLRv4Parser.ElementOptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ANTLRv4Parser#identifier.
    def visitIdentifier(self, ctx: ANTLRv4Parser.IdentifierContext):
        return self.visitChildren(ctx)


del ANTLRv4Parser
