package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.LogicalPlanGenerator
import com.databricks.labs.remorph.parsers.ProductionErrorCollector
import com.databricks.labs.remorph.parsers.intermediate.Rules
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TopPercentToLimitSubquery}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlLexer, TSqlParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class TSqlToDatabricksTranspiler extends Transpiler {
  val astBuilder = new TSqlAstBuilder()
  private val optimizer = Rules(PullLimitUpwards, new TopPercentToLimitSubquery)

  override def transpile(input: String): String = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    val errHandler = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val tree = parser.tSqlFile()
    val logicalPlan = astBuilder.visit(tree)
    val optimizedPlan = optimizer.apply(logicalPlan)
    val generator = new LogicalPlanGenerator
    generator.generate(GeneratorContext(), optimizedPlan)
  }
}
