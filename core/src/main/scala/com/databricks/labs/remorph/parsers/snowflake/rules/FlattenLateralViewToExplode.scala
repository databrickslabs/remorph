package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate._
import com.databricks.labs.remorph.parsers.snowflake.NamedArgumentExpression

// @see https://docs.snowflake.com/en/sql-reference/functions/flatten
class FlattenLateralViewToExplode extends Rule[LogicalPlan] with IRHelpers {
  override def apply(plan: LogicalPlan): LogicalPlan = plan transform {
    case l @ Join(
          SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", args)), _, _), id, colNames),
          right,
          _,
          _,
          _,
          _) =>
      l.copy(left = translatePosExplode(args, plan, id, colNames))
    case l @ Join(
          left,
          SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", args)), _, _), id, colNames),
          _,
          _,
          _,
          _) =>
      l.copy(right = translatePosExplode(args, plan, id, colNames))
//    case Lateral(TableFunction(CallFunction("FLATTEN", args)), _, _) =>
//      translateFlatten(args)
    case SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", args)), _, _), id, colNames) =>
      translatePosExplode(args, plan, id, colNames)
  }

  private def getFlag(named: Map[String, Expression], flagName: String): Boolean = named.get(flagName) match {
    case Some(BooleanLiteral(value)) => value
    case _ => false
  }

  private def translateFlatten(named: Map[String, Expression]): LogicalPlan = {
//    val named = args.collect { case NamedArgumentExpression(key, value) =>
//      key.toUpperCase() -> value
//    }.toMap
    val input = named("INPUT")
    val outer = getFlag(named, "OUTER")

    val lateralExplode = input.dataType match {
      case VariantType if outer => Lateral(TableFunction(VariantExplodeOuter(input)), outer = false)
      case VariantType => Lateral(TableFunction(VariantExplode(input)), outer = false)
      case _ => Lateral(TableFunction(Explode(input)), outer = outer)
    }
    lateralExplode
  }

  private def translatePosExplode(args: Seq[Expression], plan: LogicalPlan, id: Id, colNames: Seq[Id]): LogicalPlan = {
    val FLATTEN_OUTPUT_COLUMNS = Set("seq", "key", "path", "index", "value", "this")
    val lateralFlattenAliases = plan collect {
      case SubqueryAlias(Lateral(TableFunction(CallFunction("FLATTEN", _)), _, _), alias, _) => alias
    }
    val named = args.collect { case NamedArgumentExpression(key, value) =>
      key.toUpperCase() -> value
    }.toMap
    lazy val exprs = plan.expressions

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

    val input = named("INPUT")
    val outer = getFlag(named, "OUTER")

    val referencedColumns = aliasesUsingIndex(id)

    val translatedToExplode = if (referencedColumns.contains("index")) {

      SubqueryAlias(
        Lateral(TableFunction(PosExplode(input)), outer = outer, isView = true),
        id,
        referencedColumns.toSeq.map(Id(_)))

    } else {
      val lateralExp = translateFlatten(named)
      SubqueryAlias(lateralExp, id, colNames)
    }
    translatedToExplode
  }

}
