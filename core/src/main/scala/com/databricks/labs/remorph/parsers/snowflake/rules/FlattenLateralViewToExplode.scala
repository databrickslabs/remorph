package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.NamedArgumentExpression

// @see https://docs.snowflake.com/en/sql-reference/functions/flatten
class FlattenLateralViewToExplode extends Rule[LogicalPlan] with IRHelpers {

  private val FLATTEN_OUTPUT_COLUMNS = Set("seq", "key", "path", "index", "value", "this")

  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case j: Join if isLateralFlatten(j.left) => j.copy(left = translatePosExplode(plan, j.left))
    case j: Join if isLateralFlatten(j.right) => j.copy(right = translatePosExplode(plan, j.right))
    case p if isLateralFlatten(p) => translatePosExplode(plan, p)
  }

  private def isLateralFlatten(plan: LogicalPlan): Boolean = plan match {
    case SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", _)), _, _), _, _) => true
    case _ => false
  }

  private def translatePosExplode(plan: LogicalPlan, lateralFlatten: LogicalPlan): LogicalPlan = {
    val SubqueryAlias(Lateral(TableFunction(CallFunction(_, args)), _, _), id, colNames) = lateralFlatten
    val named = args.collect { case NamedArgumentExpression(key, value) =>
      key.toUpperCase() -> value
    }.toMap

    val exprs = plan.expressions

    // FLATTEN produces a table with several columns (that we materialize as FLATTEN_OUTPUT_COLUMNS).
    // We retain only the columns that are actually referenced elsewhere in the query.
    val flattenOutputReferencedColumns = FLATTEN_OUTPUT_COLUMNS.filter { col =>
      exprs.exists(_.find {
        case Dot(x, Id(c, false)) => x == id && c.equalsIgnoreCase(col)
        case Column(Some(r), Id(c, false)) => r.head == id && c.equalsIgnoreCase(col)
        case _ => false
      }.isDefined)
    }

    val input = named("INPUT")
    val outer = getFlag(named, "OUTER")

    // If the `index` column of FLATTEN's output is referenced elsewhere in the query, we need to translate that
    // call to FLATTEN to POSEXPLODE (so that we get the actual index of each produced row).
    if (flattenOutputReferencedColumns.contains("index")) {
      // TODO: What if we need the `index` of FLATTEN-ing something that translates to a VARIANT?
      // VARIANT_EXPLODE outputs a POS column, we need to add a test case for that.
      SubqueryAlias(
        Lateral(TableFunction(PosExplode(input)), outer = outer, isView = true),
        id,
        flattenOutputReferencedColumns.toSeq.map(Id(_)))
    } else {
      val translated = input.dataType match {
        case VariantType if outer => Lateral(TableFunction(VariantExplodeOuter(input)), outer = false)
        case VariantType => Lateral(TableFunction(VariantExplode(input)), outer = false)
        case _ => Lateral(TableFunction(Explode(input)), outer = outer)
      }
      SubqueryAlias(translated, id, colNames)
    }
  }

  private def getFlag(named: Map[String, Expression], flagName: String): Boolean = named.get(flagName) match {
    case Some(BooleanLiteral(value)) => value
    case _ => false
  }

}
