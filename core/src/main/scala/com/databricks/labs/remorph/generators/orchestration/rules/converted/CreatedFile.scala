package com.databricks.labs.remorph.generators.orchestration.rules.converted

import com.databricks.labs.remorph.intermediate.workflows.LeafJobNode

import java.util.Locale

case class CreatedFile(name: String, text: String) extends LeafJobNode {
  def resourceName: String = {
    val pathParts = name.split("/")
    val baseNameParts = pathParts.last.split("\\.")
    val lowerCaseName = baseNameParts.head.toLowerCase(Locale.ROOT)
    lowerCaseName.replaceAll("[^A-Za-z0-9]", "_")
  }
}
