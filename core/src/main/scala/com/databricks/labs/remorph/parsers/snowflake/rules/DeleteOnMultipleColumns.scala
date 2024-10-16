package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

class DeleteOnMultipleColumns extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case delete @ DeleteFromTable(target, _, Some(in: In), _, _) =>
      val subquery = in
      print(s"subquery: $subquery")
      val newSubquery = transformSubquery(target, subquery)
      delete.copy(where = Some(Exists(newSubquery)))
//      delete.copy(where = newSubquery)
  }

  private def transformSubquery(target: LogicalPlan, subquery: In): LogicalPlan = {

    // fetch table name from subquery
    // create function to fetch columns from subquery(subquery.left)
    // create function to fetch columns from expression list
    // use the column names to create a where condition

    Filter(
      Project(NamedTable(subquery.left.toString, Map(), is_streaming = false), Seq(Id("1"))),
      Equals(Id("1"), Id("1")))
  }

}
