package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator}
import com.databricks.labs.remorph.parsers.ProductionErrorCollector
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TopPercentToLimitSubquery}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlLexer, TSqlParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class TSqlToDatabricksTranspiler extends Transpiler {
  private val astBuilder = new TSqlAstBuilder()
  private val optimizer = ir.Rules(PullLimitUpwards, new TopPercentToLimitSubquery)
  private val generator = new LogicalPlanGenerator(new ExpressionGenerator())

  override def parse(input: String): ir.LogicalPlan = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    val errHandler = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val tree = parser.tSqlFile()
    astBuilder.visit(tree)
  }

  override def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan = optimizer.apply(logicalPlan)

  override def generate(optimizedLogicalPlan: ir.LogicalPlan): String =
    generator.generate(GeneratorContext(), optimizedLogicalPlan)

}
