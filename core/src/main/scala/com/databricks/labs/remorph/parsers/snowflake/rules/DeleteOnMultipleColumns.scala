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
    print("--------- subquery.left: " + subquery.left)
    print("--------- subquery.other: " + subquery.other)

    val sourceColumns = subquery.left match {
      case ExprList(cols) => cols
      case _ => Seq()
    }
    print("--------- subqueryColumns: " + sourceColumns)
//    val table = target
    // fetch table name from In subquery
    // fetch column names from subquery(subquery.left)
    // fetch column from expression list
    // use the column names to create a where condition

    Filter(
      Project(NamedTable(subquery.left.toString, Map(), is_streaming = false), Seq(Id("1"))),
      Equals(Id("1"), Id("1")))
  }

  private def createWhereCondition(sourceCols: Seq[Expression],
                                   targetCols: Seq[Expression],
                                   sourceTable: NamedTable,
                                   targetTable: NamedTable): Equals = {
    // create a where condition using the column names
    // for now, just return a dummy condition
    // traverse the sourceCols and create a where condition
    // And(Equals(Id("a"), Id("b")), Equals(Id("b"), Id("a"))))
    sourceCols.map(col => Id(col.toString))
    Equals(Id("1"), Id("1"))
  }

}
