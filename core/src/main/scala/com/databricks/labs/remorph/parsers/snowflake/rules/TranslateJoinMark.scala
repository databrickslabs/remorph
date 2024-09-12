package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{LogicalPlan, _}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
// scalastyle:off

class TranslateJoinMark extends ir.Rule[ir.LogicalPlan] {

  override def apply(plan: ir.LogicalPlan): LogicalPlan = {
    transformJoinMarkPlan2(plan)
  }



  private def transformJoinMarkPlan2(plan: LogicalPlan): LogicalPlan = {

    val joinMarkCollection = collectJoinMarks(plan)
    println(joinMarkCollection.size)

    plan.transform {
      case ir.Filter(relation, condition) =>
        def transformCondition(cond: ir.Expression): LogicalPlan = cond match {
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Literal) =>
            relation
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            createRightOuterJoin(relation, cond)
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            createLeftOuterJoin(relation, cond)
         // case ir.And(left, right) =>
            //t1.a(+) = t2.a AND t1.b(+) = t2.b
            //Transform left -> (+) or without JM t2.sal(+) = 100   t2.sal = 100

            //accumulate join markers and apply to the relation
           //  transformCondition(relation,left)
            // transformCondition(relation,right)



          case _ => relation
        }
        transformCondition(condition)

      case other => other
    }
  }
  // scalastyle:off
/*  private def transformJoinMarkPlan(plan: LogicalPlan):LogicalPlan = {
    plan.transform {
      case ir.Filter(relation, condition) =>
        condition match {

          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            createRightOuterJoin(relation, condition)
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            createLeftOuterJoin(relation, condition)

          case _ => relation
          // Add other cases as needed (e.g., NotEquals, GreaterThan, etc.)
        }
      case other => other
    }
  }*/

  private def collectJoinMarks(plan: LogicalPlan): scala.collection.mutable.ArrayBuffer[ir.Expression] = {
    val joinMarkCollection = scala.collection.mutable.ArrayBuffer[ir.Expression]()

    plan.collect {
      case ir.Filter(relation, condition) =>
        def transformCondition(cond: ir.Expression): Unit = cond match {
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Literal) =>
            joinMarkCollection += condition
          case ir.Equals(JoinMarkExpression(left: ir.Expression), right: ir.Expression) =>
            joinMarkCollection += condition
          case ir.Equals(left: ir.Expression, JoinMarkExpression(right: ir.Expression)) =>
            joinMarkCollection += condition
          case ir.And(left, right) =>
            transformCondition(left)
            transformCondition(right)
          case _ =>
        }
        transformCondition(condition)
    }

    joinMarkCollection
  }





  private def createRightOuterJoin(relation: LogicalPlan, condition: Expression,andCond: Option[Expression]=None) = {

    val join_condition = condition.transform({ case JoinMarkExpression(left: ir.Expression) =>
      left
    })
   val join_con =  if(andCond.isDefined){
     ir.And(join_condition,andCond.get)
    }else {
      join_condition
    }



    ir.Join(
      relation.asInstanceOf[Join].left,
      relation.asInstanceOf[Join].right,
      Some(join_con),
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
