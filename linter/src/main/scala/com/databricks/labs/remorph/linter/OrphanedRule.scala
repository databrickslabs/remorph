package com.databricks.labs.remorph.linter

import org.antlr.v4.runtime.tree.Trees
import org.antlr.v4.runtime.ParserRuleContext

import scala.jdk.CollectionConverters._

class OrphanedRule(ruleTracker: RuleTracker) extends ANTLRv4ParserBaseListener {

  /**
   * Checks if a rule or any of its children contains EOF as a terminal node. Rules ending in EOF are entry point rules
   * called externally and may not be referenced in the grammar, only defined. They are not reported as orphaned.
   *
   * @param ctx
   *   the parser context to search within
   * @return
   */
  private def containsEOF(ctx: ParserRuleContext): Boolean = {
    val x = Trees.findAllNodes(ctx, ANTLRv4Parser.TOKEN_REF, true).asScala
    x.foreach { node =>
      if (node.getText == "EOF") {
        return true
      }
    }
    false
  }

  /**
   * Records that a rule has been defined in the parser and whether it contains EOF
   */
  override def enterParserRuleSpec(ctx: ANTLRv4Parser.ParserRuleSpecContext): Unit = {
    val ruleSymbol = ctx.RULE_REF().getSymbol
    ruleTracker.addRuleDef(RuleDefinition(ruleSymbol.getLine, ruleSymbol.getText, containsEOF(ctx)))
  }

  /**
   * Records that a rule has been referenced in the parser
   */
  override def enterRuleref(ctx: ANTLRv4Parser.RulerefContext): Unit = {
    val ruleReference =
      new RuleReference(
        ctx.start.getLine,
        ctx.start.getCharPositionInLine,
        ctx.stop.getCharPositionInLine + ctx.getText.length,
        ctx.getText)
    ruleTracker.addRuleRef(ruleReference)
  }
}
