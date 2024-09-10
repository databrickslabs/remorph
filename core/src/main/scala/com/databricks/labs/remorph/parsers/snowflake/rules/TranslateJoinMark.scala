package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{Expression, JoinMarkExpression, LogicalPlan}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
// scalastyle:off


class TranslateJoinMark extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): LogicalPlan = {
    plan.transform {
      case ir.Filter(relation, condition) =>
        condition match{
          case ir.Equals(JoinMarkExpression(x: ir.Expression), y: ir.Expression) =>
            ir.Filter(introduceLeftJoin(relation, x, y), condition)
          case ir.Equals(x: ir.Expression, JoinMarkExpression(y: ir.Expression)) =>
            ir.Filter(introduceRightJoin(relation, x, y), condition)
          // Add other cases as needed (e.g., NotEquals, GreaterThan, etc.)
        }
      case other => other
    }
  }

  private def introduceRightJoin(relation: LogicalPlan, x: Expression, y: Expression) = {

    relation
  }

  private def introduceLeftJoin(relation: LogicalPlan, x: Expression, y: Expression) = {


    relation
  }
}

