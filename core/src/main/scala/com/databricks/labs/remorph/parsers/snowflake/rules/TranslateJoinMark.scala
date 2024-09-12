package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{LogicalPlan, _}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
// scalastyle:off

class TranslateJoinMark extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): LogicalPlan = {
    transformJoinMarkPlan2(plan)
  }



  private def transformJoinMarkPlan2(plan: LogicalPlan): LogicalPlan = {

    plan.transform {
      case ir.Filter(relation, condition) =>
        val joinMarkCollection = collectJoinMarks(plan)
        println(joinMarkCollection.size)
        def transformCondition(cond: ir.Expression): LogicalPlan = cond match {

          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            createRightOuterJoin(relation, cond,joinMarkCollection)
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            createLeftOuterJoin(relation, cond)
         /* case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Literal) =>
            relation*/
          case ir.And(left:ir.Expression, right:ir.Expression) =>
            //TODO: handle and condition
             transformCondition(left)
             transformCondition(right)
            relation

          case _ => relation
        }
        transformCondition(condition)

      case other => other
    }
  }


  private def collectJoinMarks(plan: LogicalPlan): scala.collection.mutable.Set[ir.Expression] = {
    val joinMarkCollection = scala.collection.mutable.Set[ir.Expression]()

    plan.collect {
      case ir.Filter(relation, condition) =>
        def transformCondition(cond: ir.Expression): Unit = cond match {
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Literal) =>
            joinMarkCollection += cond
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            joinMarkCollection += cond
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            joinMarkCollection += cond
          case ir.And(left, right) =>
            transformCondition(left)
            transformCondition(right)
          case _ =>
        }
        transformCondition(condition)
    }

    joinMarkCollection
  }


  private def createRightOuterJoin(relation: LogicalPlan, condition: Expression,andExpressions:scala.collection.mutable.Set[ir.Expression]) = {

    var derivedAnd: Option[ir.Expression] = None
    andExpressions.foreach {
      case ex @ ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Literal) =>
        derivedAnd = derivedAnd match {
          case Some(existing) => Some(ir.And(existing, ex))
          case None => Some(ir.And(ex, condition))
        }
    }

    ir.Join(
      relation.asInstanceOf[Join].left,
      relation.asInstanceOf[Join].right,
      Some(derivedAnd.get),
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
