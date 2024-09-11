package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{Expression, Join, JoinMarkExpression, LogicalPlan}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
// scalastyle:off

class TranslateJoinMark extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): LogicalPlan = {
    plan.transform {
      case ir.Filter(relation, condition) =>
        condition match {
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            createRightOuterJoin(relation, condition)
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            createLeftOuterJoin(relation, condition)

          // Add other cases as needed (e.g., NotEquals, GreaterThan, etc.)
        }
      case other => other
    }
  }

  private def createRightOuterJoin(relation: LogicalPlan, condition: Expression) = {

    val join_condition = condition.transform({ case JoinMarkExpression(left: ir.Expression) =>
      left
    })

    ir.Join(
      relation.asInstanceOf[Join].left,
      relation.asInstanceOf[Join].right,
      Some(join_condition),
      ir.RightOuterJoin,
      Seq(),
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))

  }

  private def createLeftOuterJoin(relation: LogicalPlan, condition: Expression): ir.Join = {

    val join_condition = condition.transform({ case JoinMarkExpression(left: ir.Expression) =>
      left
    })

    ir.Join(
      relation.asInstanceOf[Join].left,
      relation.asInstanceOf[Join].right,
      Some(join_condition),
      ir.LeftOuterJoin,
      Seq(),
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

}
