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
    // Assuming the subquery is a SELECT DISTINCT query
    print("--------- subquery.relation: " + subquery.relation)
    //    ScalarSubquery(subquery.relation)
    val table = subquery.relation
//    Exists(Seq(ScalarSubquery(Project(table, Seq(Id("1"))))))
    Project(table, Seq(Id("1")))
  }

}