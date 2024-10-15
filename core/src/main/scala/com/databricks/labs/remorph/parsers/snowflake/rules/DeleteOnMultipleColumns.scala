package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._


class DeleteOnMultipleColumns extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case delete @ DeleteFromTable(target, _, Some(exists: Exists), _, _) =>
      val subquery = exists
      print(s"subquery: $subquery")
      val newSubquery = transformSubquery(target, subquery)
      delete.copy(where = Some(Exists(newSubquery)))
//      delete.copy(where = newSubquery)
  }

  private def transformSubquery(target: LogicalPlan, subquery: Exists): LogicalPlan = {
    print("--------- subquery.relation: " + subquery.relation)
//    val table = target
    Filter(Project(NamedTable(subquery.relation.toString, Map(), is_streaming = false), Seq(Id("1")))
      , Equals(Id("1"), Id("1")))
  }

//  private def createWhereCondition(source): LogicalPlan = {
//
//  }

}