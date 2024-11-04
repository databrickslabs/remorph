package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.bundles.Schema
import com.databricks.labs.remorph.generators.orchestration.rules.history.{Migration, QueryPlan}
import com.databricks.labs.remorph.intermediate.{NamedTable, Rule}
import com.databricks.labs.remorph.intermediate.workflows.JobNode

class DefineSchemas extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformUp { case Migration(children) =>
    var schemas = Seq[Schema]()
    children foreach {
      case QueryPlan(plan, _) =>
        plan foreach {
          case NamedTable(unparsedName, _, _) =>
            val parts = unparsedName.split("\\.")
            if (parts.size == 1) {
              schemas +:= Schema("main", "default")
            } else {
              schemas +:= Schema("main", parts(0))
            }
          case _ => // noop
        }
      case _ => // noop
    }
    schemas = schemas.distinct.sortBy(_.name)
    Migration(schemas ++ children)
  }
}
