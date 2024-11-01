package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.{Generating, KoResult, OkResult, PartialResult}
import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.orchestration.rules.converted.SuccessPy
import com.databricks.labs.remorph.generators.orchestration.rules.history.{FailedQuery, PartialQuery, QueryPlan}
import com.databricks.labs.remorph.generators.py.LogicalPlanGenerator
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.transpilers.PySparkGenerator

class TryGeneratePythonNotebook(generator: PySparkGenerator) extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformDown { case n @ QueryPlan(plan, query) =>
    val state = Generating(plan, n, GeneratorContext(new LogicalPlanGenerator))
    generator.generate(plan).run(state) match {
      case OkResult((_, sql)) => SuccessPy(query.id, sql)
      case PartialResult((_, sql), error) => PartialQuery(query, error.msg, SuccessPy(query.id, sql))
      case KoResult(stage, error) => FailedQuery(query, error.msg, stage)
    }
  }
}
