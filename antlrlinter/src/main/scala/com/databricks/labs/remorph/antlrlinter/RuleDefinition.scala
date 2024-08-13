package com.databricks.labs.remorph.antlrlinter

case class RuleDefinition(lineNo: Integer, ruleName: String, refCount: Integer = 0) {
  def getLineNo: Integer = lineNo
  def getRuleName: String = ruleName
  def getRefCount: Integer = refCount
}
