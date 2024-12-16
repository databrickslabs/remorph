package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.{KoResult, TransformationConstructors, WorkflowStage, intermediate => ir}
import com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.generators.py.rules.{AndOrToBitwise, DotToFCol, ImportClasses, PySparkExpressions, PySparkStatements}
import org.json4s.{Formats, NoTypeHints}
import org.json4s.jackson.Serialization

import scala.util.control.NonFatal

class PySparkGenerator extends TransformationConstructors {
  private[this] val exprGenerator = new py.ExpressionGenerator
  private[this] val stmtGenerator = new py.StatementGenerator(exprGenerator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  private[this] val expressionRules = ir.Rules(new DotToFCol, new PySparkExpressions, new AndOrToBitwise)
  private[this] val statementRules = ir.Rules(new PySparkStatements(expressionRules), new ImportClasses)

  def generate(optimizedLogicalPlan: ir.LogicalPlan): py.Python = {
    try {
      val withShims = PySparkStatements(optimizedLogicalPlan)
      val statements = statementRules(withShims)
      statements.flatMap(stmtGenerator.generate)
    } catch {
      case NonFatal(e) =>
        lift(KoResult(WorkflowStage.GENERATE, ir.UncaughtException(e)))
    }
  }
}
