package com.databricks.labs.remorph.antlrlinter

class RuleReference(lineNo: Int, charStart: Int, charEnd: Int, ruleName: String) {
  def getLineNo: Int = lineNo
  def getCharStart: Int = charStart
  def getCharEnd: Int = charEnd
  def getRuleName: String = ruleName
}
