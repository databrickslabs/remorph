package com.databricks.labs.remorph.linter

case class RuleDefinition(lineNo: Int, ruleName: String, isExternal: Boolean = false)
