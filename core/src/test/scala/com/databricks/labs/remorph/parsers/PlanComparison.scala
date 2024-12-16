package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.utils.Strings
import com.databricks.labs.remorph.{Transformation, TransformationConstructors, TranspilerState, intermediate => ir}
import org.scalatest.Assertions

trait PlanComparison extends TransformationConstructors {
  self: Assertions =>

  protected def comparePlans(actual: Transformation[ir.LogicalPlan], expected: ir.LogicalPlan): Unit = {
    actual
      .flatMap(reorderComparisons)
      .flatMap { act =>
        reorderComparisons(expected).map { exp =>
          if (exp != act) {
            fail(s"""
                  |== FAIL: Plans do not match (expected vs actual) ===
                  |${Strings.sideBySide(pretty(exp), pretty(act)).mkString("\n")}
         """.stripMargin)
          }
        }
      }
      .runAndDiscardState(TranspilerState())
  }

  private def pretty(x: Any): String = pprint.apply(x, width = 40).plainText

  protected def eraseExprIds(plan: ir.LogicalPlan): Transformation[ir.LogicalPlan] = {
    val exprId = ir.ExprId(0)
    plan transformAllExpressions { case ir.AttributeReference(name, dt, nullable, _, qualifier) =>
      ok(ir.AttributeReference(name, dt, nullable, exprId, qualifier))
    }
  }

  protected def reorderComparisons(plan: ir.LogicalPlan): Transformation[ir.LogicalPlan] = {
    eraseExprIds(plan).flatMap(_.transformAllExpressions {
      case ir.Equals(l, r) if l.hashCode() > r.hashCode() => ok(ir.Equals(r, l))
      case ir.GreaterThan(l, r) if l.hashCode() > r.hashCode() => ok(ir.LessThan(r, l))
      case ir.GreaterThanOrEqual(l, r) if l.hashCode() > r.hashCode() => ok(ir.LessThanOrEqual(r, l))
      case ir.LessThan(l, r) if l.hashCode() > r.hashCode() => ok(ir.GreaterThan(r, l))
      case ir.LessThanOrEqual(l, r) if l.hashCode() > r.hashCode() => ok(ir.GreaterThanOrEqual(r, l))
    })
  }
}
