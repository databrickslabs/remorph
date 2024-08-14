package com.databricks.labs.remorph.linter

class OrphanedRule(ruleTracker: RuleTracker) extends ANTLRv4ParserBaseListener {

  /**
   * Records that a rule has been defined in the parser
   */
  override def enterParserRuleSpec(ctx: ANTLRv4Parser.ParserRuleSpecContext): Unit = {

    val ruleSymbol = ctx.RULE_REF().getSymbol
    val ruleDefinition = new RuleDefinition(ruleSymbol.getLine, ruleSymbol.getText)
    ruleTracker.addRuleDef(ruleDefinition)
  }

  /**
   * Records that a rule has been referenced in the parser
   */
  override def enterRuleref(ctx: ANTLRv4Parser.RulerefContext): Unit = {
    val ruleReference =
      new RuleReference(ctx.start.getLine, ctx.start.getCharPositionInLine, ctx.stop.getCharPositionInLine, ctx.getText)
    ruleTracker.addRuleRef(ruleReference)
  }
}
