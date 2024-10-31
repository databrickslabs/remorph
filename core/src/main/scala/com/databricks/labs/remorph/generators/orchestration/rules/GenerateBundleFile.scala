package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.generators.orchestration.rules.converted.InformationFile
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.databricks.labs.remorph.intermediate.workflows.jobs.JobSettings
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory

class GenerateBundleFile extends Rule[JobNode] {
  private val mapper = new ObjectMapper(new YAMLFactory());
  override def apply(tree: JobNode): JobNode = tree transform { case j: JobSettings =>
    // TODO: this is nowhere near a valid bundle file, but we need to start somewhere
    val yml = mapper.writeValueAsString(j.toCreate)
    InformationFile("databricks.yml", yml)
  }
}
