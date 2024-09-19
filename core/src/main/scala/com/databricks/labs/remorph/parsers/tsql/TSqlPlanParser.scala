package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{PlanParser, intermediate => ir}
import com.databricks.labs.remorph.parsers.intermediate.{LogicalPlan, Rules}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TSqlCallMapper, TopPercentToLimitSubquery, TrapInsertDefaultsAction}
import org.antlr.v4.runtime.{CharStream, ParserRuleContext, TokenSource, TokenStream}

class TSqlPlanParser extends PlanParser[TSqlParser] {

  private val astBuilder = new TSqlAstBuilder()

  override protected def createLexer(input: CharStream): TokenSource = new TSqlLexer(input)
  override protected def createParser(stream: TokenStream): TSqlParser = new TSqlParser(stream)
  override protected def createTree(parser: TSqlParser): ParserRuleContext = parser.tSqlFile()
  override protected def createPlan(tree: ParserRuleContext): LogicalPlan = astBuilder.visit(tree)

  // TODO: Note that this is not the correct place for the optimizer, but it is here for now
  override protected def createOptimizer: Rules[LogicalPlan] = {
    ir.Rules(
      new TSqlCallMapper,
      ir.AlwaysUpperNameForCallFunction,
      PullLimitUpwards,
      new TopPercentToLimitSubquery,
      TrapInsertDefaultsAction)
  }

}
