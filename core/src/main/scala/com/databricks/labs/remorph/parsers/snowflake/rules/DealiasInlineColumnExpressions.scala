package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

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
        case Column(None, id) if columnNamesToValues.contains(id) => columnNamesToValues(id)
        case id: Id if columnNamesToValues.contains(id) => columnNamesToValues(id)
      }
    }

    WithCTE(tables, fixedUpReferences)
  }

}
