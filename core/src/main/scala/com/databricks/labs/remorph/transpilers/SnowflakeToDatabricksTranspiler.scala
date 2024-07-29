package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.LogicalPlanGenerator
import com.databricks.labs.remorph.parsers.ProductionErrorCollector
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeLexer, SnowflakeParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class SnowflakeToDatabricksTranspiler extends Transpiler {

  val astBuilder = new SnowflakeAstBuilder

  override def transpile(input: String): String = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val errHandler = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val tree = parser.snowflakeFile()
    val logicalPlan = astBuilder.visit(tree)
    val generator = new LogicalPlanGenerator
    generator.generate(GeneratorContext(), logicalPlan)
  }
}
