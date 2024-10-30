package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.{KoResult, WorkflowStage}
import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.generators.py.rules.{AndOrToBitwise, DotToFCol, ImportClasses, PySparkExpressions, PySparkStatements}
import org.json4s.{Formats, NoTypeHints}
import org.json4s.jackson.Serialization

import scala.util.control.NonFatal

class PySparkGenerator {
  private val exprGenerator = new py.ExpressionGenerator
  private val stmtGenerator = new py.StatementGenerator(exprGenerator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  private val expressionRules = ir.Rules(new DotToFCol, new PySparkExpressions, new AndOrToBitwise)
  private val statementRules = ir.Rules(new PySparkStatements(expressionRules), new ImportClasses)

  def generate(optimizedLogicalPlan: ir.LogicalPlan): py.Python = {
    try {
      val generatorContext = GeneratorContext(new py.LogicalPlanGenerator)
      val withShims = PySparkStatements(optimizedLogicalPlan)
      val statements = statementRules(withShims)
      stmtGenerator.generate(generatorContext, statements)
    } catch {
      case NonFatal(e) =>
        KoResult(WorkflowStage.GENERATE, ir.UncaughtException(e))
    }
  }
}
