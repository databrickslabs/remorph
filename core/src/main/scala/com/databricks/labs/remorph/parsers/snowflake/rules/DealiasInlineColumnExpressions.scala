package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

// SNOWFLAKE - Common Table Expression may be of the form:
// WITH
//    a AS (1),
//    b AS (2)
// SELECT ...
// CTEs like `a AS (1)` above act as columns of an anonymous table with a single row.
// In AstBuilding phase, we translate those as InlineColumnExpression. Later, in Optimizing phase, we'll combine all
// such expressions in a single table declaration (using VALUES).
private[snowflake] case class InlineColumnExpression(columnName: Id, value: Expression) extends LogicalPlan {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

class DealiasInlineColumnExpressions extends Rule[LogicalPlan] {

  override def apply(plan: LogicalPlan): LogicalPlan = plan.transform { case WithCTE(ctes, query) =>
    bundleInlineColumns(ctes, query)
  }

  private def bundleInlineColumns(plans: Seq[LogicalPlan], query: LogicalPlan): LogicalPlan = {
    val (inlineColumns, tables) = plans.foldLeft((Seq.empty[InlineColumnExpression], Seq.empty[LogicalPlan])) {
      case ((ics, tbls), i: InlineColumnExpression) => ((ics :+ i, tbls))
      case ((ics, tbls), t) => ((ics, tbls :+ t))
    }
    val columnNamesToValues = inlineColumns.map(ic => ic.columnName -> ic.value).toMap

    val fixedUpReferences = query transformUp { case p =>
      p.transformExpressionsUp {
        case Column(None, id: Id) if columnNamesToValues.contains(id) => columnNamesToValues(id)
        case id: Id if columnNamesToValues.contains(id) => columnNamesToValues(id)
      }
    }

    WithCTE(tables, fixedUpReferences)
  }

}
