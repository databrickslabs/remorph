package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.parsers.snowflake.rules._
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeLexer, SnowflakeParser}
import com.databricks.labs.remorph.parsers.{ProductionErrorCollector, intermediate => ir}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class SnowflakeToDatabricksTranspiler extends BaseTranspiler {

  private val astBuilder = new SnowflakeAstBuilder
  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)
  private val optimizer =
    ir.Rules(
      new SnowflakeCallMapper,
      ir.AlwaysUpperNameForCallFunction,
      new UpdateToMerge,
      new CastParseJsonToFromJson(generator),
      new TranslateWithinGroup,
      new FlattenLateralViewToExplode(),
      new FlattenNestedConcat)

  override def parse(input: String): ir.LogicalPlan = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val errHandler = new ProductionErrorCollector(input, "-- test string --")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val tree = parser.snowflakeFile()
    astBuilder.visit(tree)
  }

  override def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan = optimizer.apply(logicalPlan)

  override def generate(optimizedLogicalPlan: ir.LogicalPlan): String =
    generator.generate(GeneratorContext(generator), optimizedLogicalPlan)

}
