package com.databricks.labs.remorph.generators.orchestration.rules.history

import com.databricks.labs.remorph.intermediate.workflows.JobNode

case class Migration(children: Seq[JobNode]) extends JobNode
