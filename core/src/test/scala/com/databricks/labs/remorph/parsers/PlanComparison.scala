package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.utils.Strings
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.Assertions

trait PlanComparison {
  self: Assertions =>

  protected def comparePlans(a: ir.LogicalPlan, b: ir.LogicalPlan): Unit = {
    val expected = reorderComparisons(a)
    val actual = reorderComparisons(b)
    if (expected != actual) {
      fail(s"""
           |== FAIL: Plans do not match ===
           |${Strings.sideBySide(expected.treeString, actual.treeString).mkString("\n")}
         """.stripMargin)
    }
  }

  protected def reorderComparisons(plan: ir.LogicalPlan): ir.LogicalPlan = {
    plan transformAllExpressions {
      case ir.Equals(l, r) if l.hashCode() > r.hashCode() => ir.Equals(r, l)
      case ir.GreaterThan(l, r) if l.hashCode() > r.hashCode() => ir.LessThan(r, l)
      case ir.GreaterThanOrEqual(l, r) if l.hashCode() > r.hashCode() => ir.LessThanOrEqual(r, l)
      case ir.LessThan(l, r) if l.hashCode() > r.hashCode() => ir.GreaterThan(r, l)
      case ir.LessThanOrEqual(l, r) if l.hashCode() > r.hashCode() => ir.GreaterThanOrEqual(r, l)
    }
  }
}
