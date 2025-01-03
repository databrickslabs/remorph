package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.converted.SuccessSQL
import com.databricks.labs.remorph.Transformation
import com.databricks.labs.remorph.generators.orchestration.rules.history.QueryPlan
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.transpilers.SqlGenerator

class TryGenerateSQL(generator: SqlGenerator) extends Rule[JobNode] {
  override def apply(tree: JobNode): Transformation[JobNode] = tree transformDown { case QueryPlan(plan, query) =>
    generator.generate(plan).map(sql => SuccessSQL(query.id, sql))
  }
}
