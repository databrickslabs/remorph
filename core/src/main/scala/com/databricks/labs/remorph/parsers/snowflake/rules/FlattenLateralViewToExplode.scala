package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.NamedArgumentExpression

// @see https://docs.snowflake.com/en/sql-reference/functions/flatten
class FlattenLateralViewToExplode extends Rule[LogicalPlan] with IRHelpers {
  private val FLATTEN_OUTPUT_COLUMNS = Set("seq", "key", "path", "index", "value", "this")

  override def apply(plan: LogicalPlan): LogicalPlan = {

    val lateralFlattenAliases = plan collect {
      case SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", _)), _), alias, _) => alias
    }

    lazy val exprs = plan.nestedExpressions

    // If the query makes use of the `index` column of FLATTEN's result, we will have to translate
    // it to POSEXPLODE.
    val aliasesUsingIndex = lateralFlattenAliases.map { id =>
      id -> FLATTEN_OUTPUT_COLUMNS.filter { col =>
        exprs.exists(_.find {
          case Dot(x, Id(c, false)) => x == id && c.equalsIgnoreCase(col)
          case Column(Some(r), Id(c, false)) => r.head == id && c.equalsIgnoreCase(col)
          case _ => false
        }.nonEmpty)
      }
    }.toMap

    val translatedToExplode = plan transform {
      case SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", args)), _), id, colNames) =>
        val named = args.collect { case NamedArgumentExpression(key, value) =>
          key.toUpperCase() -> value
        }.toMap
        val input = named("INPUT")
        // val path = named.get("PATH").orElse(Some(Literal("")))
        val outer = getFlag(named, "OUTER")
        // val recursive = getFlag(named, "RECURSIVE")
        // val mode = named.get("MODE").orElse(Some(Literal("BOTH")))
        val referencedColumns = aliasesUsingIndex(id)

        if (referencedColumns.contains("index")) {
          SubqueryAlias(
            Lateral(TableFunction(PosExplode(input)), outer = outer),
            id,
            referencedColumns.toSeq.map(Id(_)))
        } else { SubqueryAlias(Lateral(TableFunction(Explode(input)), outer = outer), id, colNames) }

    }

    translatedToExplode transformAllExpressions { case JsonAccess(json, path) =>
      JsonAccess(fixupReference(json, lateralFlattenAliases), path)
    }
  }

  private def getFlag(named: Map[String, Expression], flagName: String): Boolean = named.get(flagName) match {
    case Some(BooleanLiteral(value)) => value
    case _ => false
  }

  private def fixupReference(ref: Expression, aliasesNeedingFixup: Seq[Id]): Expression = ref match {
    case Dot(id, Id("value", false)) if aliasesNeedingFixup.contains(id) => id
    case x => x
  }
}
