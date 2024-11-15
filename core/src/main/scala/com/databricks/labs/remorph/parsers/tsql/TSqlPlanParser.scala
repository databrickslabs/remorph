package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.parsers.{AntlrPlanParser, PlanParser, ProductionErrorCollector}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TSqlCallMapper, TopPercentToLimitSubquery, TrapInsertDefaultsAction}
import com.databricks.labs.remorph.{Parsing, Transformation, intermediate => ir}
import org.antlr.v4.runtime._
import org.antlr.v4.runtime.tree.ParseTree

class TSqlPlanParser extends PlanParser with AntlrPlanParser {

  val vc = new TSqlVisitorCoordinator(TSqlParser.VOCABULARY, TSqlParser.ruleNames)

  override def parseLogicalPlan(parsing: Parsing): Transformation[LogicalPlan] = {
    val input = CharStreams.fromString(parsing.source)
    val lexer = new TSqlLexer(input)
    val tokens = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokens)
    parser.setErrorHandler(new TSqlErrorStrategy)
    val errListener = setErrorListener(parser, new ProductionErrorCollector(parsing.source, parsing.filename))
    val tree = parser.tSqlFile()
    generatePlan(tree, () => createPlan(tokens, tree), errListener)
  }

  private def createPlan(tokens: CommonTokenStream, tree: ParseTree): LogicalPlan = {
    val plan = vc.astBuilder.visit(tree)
    plan
  }

  def dialect: String = "tsql"

  // TODO: Note that this is not the correct place for the optimizer, but it is here for now
  override protected def createOptimizer: ir.Rules[ir.LogicalPlan] = {
    ir.Rules(
      new TSqlCallMapper,
      ir.AlwaysUpperNameForCallFunction,
      PullLimitUpwards,
      new TopPercentToLimitSubquery,
      TrapInsertDefaultsAction)
  }

}
