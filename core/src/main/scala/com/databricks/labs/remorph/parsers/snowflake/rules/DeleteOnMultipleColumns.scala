package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

class DeleteOnMultipleColumns extends Rule[LogicalPlan] {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case delete @ DeleteFromTable(target, _, Some(exists: Exists), _, _) =>
      val newSubquery = transformSubquery(target, exists)
      delete.copy(where = Some(Exists(newSubquery)))
    case delete @ DeleteFromTable(target, _, Some(Not(Exists(subquery))), _, _) =>
      val newSubquery = transformSubquery(target, Exists(subquery))
      delete.copy(where = Some(Not(Exists(newSubquery))))
  }

  private def transformSubquery(target: LogicalPlan, exists: Exists): LogicalPlan = {
    val outerTable = fetchTableName(target)
    val subqueryTable = fetchTableName(exists.relation)

    val filterExpr = exists.relation collectFirst { case Filter(_, expressions) =>
      expressions
    }

    val modifiedSubquery = replaceSourceAndTarget(filterExpr.get, outerTable, subqueryTable)
    Filter(Project(NamedTable(subqueryTable, Map(), is_streaming = false), Seq(Id("1"))), modifiedSubquery)
  }

  private def fetchTableName(plan: LogicalPlan): String = {
    plan match {
      case Project(Filter(NamedTable(name, _, _), _), _) => name
      case NamedTable(name, _, _) => name
      case _ => throw new IllegalArgumentException("Unable to fetch table name")
    }
  }

  private def replaceSourceAndTarget(expression: Expression, outerTable: String, subqueryTable: String): Expression = {
    expression transform {
      case col @ Column(Some(ObjectReference(Id("outer", _))), _) =>
        col.copy(tableNameOrAlias = Some(ObjectReference(Id(outerTable))))
      case col @ Column(Some(ObjectReference(Id("inner", _))), _) =>
        col.copy(tableNameOrAlias = Some(ObjectReference(Id(subqueryTable))))
    }
  }
}
