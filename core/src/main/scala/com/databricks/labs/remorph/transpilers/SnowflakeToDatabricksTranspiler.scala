package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write
import org.json4s.{Formats, NoTypeHints}

import java.io.{PrintWriter, StringWriter}

class SnowflakeToDatabricksTranspiler extends BaseTranspiler {

  private val planParser = new SnowflakePlanParser
  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  override def parse(input: SourceCode): Result[ParserRuleContext] = {
    planParser.parse(input)
  }

  override def visit(tree: ParserRuleContext): Result[ir.LogicalPlan] = {
    planParser.visit(tree)
  }

  override def optimize(logicalPlan: ir.LogicalPlan): Result[ir.LogicalPlan] = {
    planParser.optimize(logicalPlan)
  }

  override def generate(optimizedLogicalPlan: ir.LogicalPlan): Result[String] = {
    try {
      val output = generator.generate(GeneratorContext(generator), optimizedLogicalPlan)
      Result.Success(output)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result.Failure(stage = WorkflowStage.GENERATE, errorJson)
    }
  }

}
