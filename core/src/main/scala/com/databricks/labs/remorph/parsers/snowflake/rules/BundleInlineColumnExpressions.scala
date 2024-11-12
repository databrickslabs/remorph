package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._

class BundleInlineColumnExpressions extends Rule[LogicalPlan] {

  private val inlineBundleTable = "INLINE_BUNDLE"

  override def apply(plan: LogicalPlan): LogicalPlan = plan.transform { case WithCTE(ctes, query) =>
    bundleInlineColumns(ctes, query)
  }

  private def bundleInlineColumns(plans: Seq[LogicalPlan], query: LogicalPlan): LogicalPlan = {
    val (inlineColumns, tables) = plans.foldLeft((Seq.empty[InlineColumnExpression], Seq.empty[LogicalPlan])) {
      case ((ics, tbls), i: InlineColumnExpression) => ((ics :+ i, tbls))
      case ((ics, tbls), t) => ((ics, tbls :+ t))
    }
    val columnNames = inlineColumns.map(_.columnName)
    val columnValues = inlineColumns.map(_.value)
    val bundledCtes =
      SubqueryAlias(Project(Values(Seq(columnValues)), Seq(Star())), Id(inlineBundleTable), columnNames) +:
        tables

    val fixedUpReferences = query transformUp { case p =>
      p.transformExpressionsUp {
        case Column(None, id) if columnNames.contains(id) => Column(Some(ObjectReference(Id(inlineBundleTable))), id)
        case id if columnNames.contains(id) => Dot(Id(inlineBundleTable), id)
      }
    }

    val updatedQuery = fixedUpReferences match {
      case Project(lp, cols) =>
        Project(
          Join(
            NamedTable(inlineBundleTable),
            lp,
            None,
            InnerJoin,
            Seq.empty,
            JoinDataType(is_left_struct = false, is_right_struct = false)),
          cols)
    }

    WithCTE(bundledCtes, updatedQuery)
  }

}
