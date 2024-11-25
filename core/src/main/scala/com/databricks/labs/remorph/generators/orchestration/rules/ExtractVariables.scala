package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.converted.NeedsVariables
import com.databricks.labs.remorph.generators.orchestration.rules.history.QueryPlan
import com.databricks.labs.remorph.intermediate.{Rule, Variable}
import com.databricks.labs.remorph.intermediate.workflows.JobNode

class ExtractVariables extends Rule[JobNode] {
  override def apply(tree: JobNode): JobNode = tree transformUp { case q: QueryPlan =>
    val variables = q.plan.expressions
      .filter(_.isInstanceOf[Variable])
      .map { case Variable(name) => name }
    if (variables.nonEmpty) {
      NeedsVariables(q, variables)
    } else {
      q
    }
  }
}
