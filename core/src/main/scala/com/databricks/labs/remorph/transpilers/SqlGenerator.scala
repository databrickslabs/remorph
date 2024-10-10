package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.{intermediate => ir}
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write
import org.json4s.{Formats, NoTypeHints}

import java.io.{PrintWriter, StringWriter}

// TODO: This should not be under transpilers but we have not refactored generation out of the transpiler yet
//       and it may need changes before it is consider finished anyway, such as implementing a trait
class SqlGenerator {

  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  def generate(optimizedLogicalPlan: ir.LogicalPlan): Result[String] = {
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
