package com.databricks.labs.remorph.antlrlinter

case class RuleDefinition(lineNo: Int, ruleName: String) {
  def getLineNo: Int = lineNo
  def getRuleName: String = ruleName
}
