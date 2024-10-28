package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.{KoResult, WorkflowStage}
import com.databricks.labs.remorph.generators.GeneratorContext
import org.json4s.{Formats, NoTypeHints}
import org.json4s.jackson.Serialization
import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.generators.py.{ExpressionGenerator, Python, StatementGenerator}
import com.databricks.labs.remorph.generators.py.rules.{ImportClasses, PySparkExpressions, PySparkStatements}

import scala.util.control.NonFatal

class PySparkGenerator {
  private val exprGenerator = new ExpressionGenerator
  private val generator = new StatementGenerator

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  private def optimizer: ir.Rules[ir.LogicalPlan] = {
    val expressions = new PySparkExpressions
    ir.Rules(expressions, new PySparkStatements(expressions), new ImportClasses)
  }

  def generate(optimizedLogicalPlan: ir.LogicalPlan): Python = {
    try {
      generator.generate(GeneratorContext(generator), optimizedLogicalPlan)
    } catch {
      case NonFatal(e) =>
        KoResult(WorkflowStage.GENERATE, ir.UncaughtException(e))
    }
  }
}
