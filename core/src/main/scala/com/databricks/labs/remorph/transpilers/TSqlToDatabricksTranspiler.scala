package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TopPercentToLimitSubquery, TrapInsertDefaultsAction}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlErrorStrategy, TSqlLexer, TSqlParser}
import com.databricks.labs.remorph.parsers.{ProductionErrorCollector, intermediate => ir}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class TSqlToDatabricksTranspiler extends BaseTranspiler {
  private val astBuilder = new TSqlAstBuilder()
  private val optimizer = ir.Rules(PullLimitUpwards, new TopPercentToLimitSubquery, TrapInsertDefaultsAction)
  private val generator = new LogicalPlanGenerator(new ExpressionGenerator())

  override def parse(input: String): ir.LogicalPlan = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    parser.setErrorHandler(new TSqlErrorStrategy)
    val errListener = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errListener)
    val tree = parser.tSqlFile()
    astBuilder.visit(tree)
  }

  override def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan = optimizer.apply(logicalPlan)

  override def generate(optimizedLogicalPlan: ir.LogicalPlan): String =
    generator.generate(GeneratorContext(), optimizedLogicalPlan)

}
