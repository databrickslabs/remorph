package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.intermediate.TranspileFailure
import com.databricks.labs.remorph.{BuildingAst, KoResult, Optimizing, Parsing, Transformation, TransformationConstructors, WorkflowStage, intermediate => ir}
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}

import scala.util.control.NonFatal

trait PlanParser extends TransformationConstructors {

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  def parseLogicalPlan(parsing: Parsing): Transformation[ir.LogicalPlan]
  def dialect: String

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  protected def createOptimizer: ir.Rules[ir.LogicalPlan]

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  /**
   * Optimize the logical plan
   *
   * @param logicalPlan The logical plan
   * @return Returns an optimized logical plan on success otherwise a description of the errors
   */
  def optimize(logicalPlan: ir.LogicalPlan): Transformation[ir.LogicalPlan] = {
    update {
      case b: BuildingAst => Optimizing(logicalPlan, Some(b))
      case _ => Optimizing(logicalPlan)
    }.flatMap { _ =>
      try {
        ok(createOptimizer.apply(logicalPlan))
      } catch {
        case NonFatal(e) =>
          lift(KoResult(stage = WorkflowStage.OPTIMIZE, TranspileFailure(e)))
      }
    }
  }
}
