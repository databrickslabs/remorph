package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{KoResult, TransformationConstructors, WorkflowStage, intermediate => ir}
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator, SQL}
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}

import scala.util.control.NonFatal

// TODO: This should not be under transpilers but we have not refactored generation out of the transpiler yet
//       and it may need changes before it is considered finished anyway, such as implementing a trait
class SqlGenerator extends TransformationConstructors {

  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  def initialGeneratorContext: GeneratorContext = GeneratorContext(generator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  def generate(optimizedLogicalPlan: ir.LogicalPlan): SQL = {
    try {
      generator.generate(optimizedLogicalPlan)
    } catch {
      case NonFatal(e) =>
        lift(KoResult(WorkflowStage.GENERATE, ir.UncaughtException(e)))
    }
  }
}
