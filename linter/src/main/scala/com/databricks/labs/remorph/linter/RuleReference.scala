package com.databricks.labs.remorph.linter

case class RuleReference(lineNo: Int, charStart: Int, charEnd: Int, ruleName: String) {}
