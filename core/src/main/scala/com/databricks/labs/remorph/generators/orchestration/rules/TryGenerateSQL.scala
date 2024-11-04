package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.converted.SuccessSQL
import com.databricks.labs.remorph.{Generating, KoResult, OkResult, PartialResult}
import com.databricks.labs.remorph.generators.orchestration.rules.history.{FailedQuery, PartialQuery, QueryPlan}
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.transpilers.SqlGenerator

class TryGenerateSQL(generator: SqlGenerator) extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformDown { case n @ QueryPlan(plan, query) =>
    val state = Generating(plan, n, generator.initialGeneratorContext)
    generator.generate(plan).run(state) match {
      case OkResult((_, sql)) => SuccessSQL(query.id, sql)
      case PartialResult((_, sql), error) => PartialQuery(query, error.msg, SuccessSQL(query.id, sql))
      case KoResult(stage, error) => FailedQuery(query, error.msg, stage)
    }
  }
}
