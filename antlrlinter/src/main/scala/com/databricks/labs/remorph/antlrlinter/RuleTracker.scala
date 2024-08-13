package com.databricks.labs.remorph.antlrlinter

class RuleTracker {

  private var ruleMap: Map[String, RuleDefinition] = Map()

  def addRule(rule: RuleDefinition): Unit = {
    ruleMap += (rule.getRuleName -> rule)
  }

  def getRule(ruleName: String): RuleDefinition = {
    ruleMap(ruleName)
  }

  def getRuleMap: Map[String, RuleDefinition] = {
    ruleMap
  }

  def getRuleCount: Int = {
    ruleMap.size
  }

  def getRuleNames: List[String] = {
    ruleMap.keys.toList
  }

  def getRuleDefinitions: List[RuleDefinition] = {
    ruleMap.values.toList
  }

  def getRuleDefinition(ruleName: String): RuleDefinition = {
    ruleMap(ruleName)
  }

  def getRuleRefCount(ruleName: String): Int = {
    ruleMap(ruleName).getRefCount
  }

  def getRuleLineNo(ruleName: String): Int = {
    ruleMap(ruleName).getLineNo
  }

  def getRuleWithRefCountLessThan(refCount: Int): List[RuleDefinition] = {
    ruleMap.values.filter(_.getRefCount < refCount).toList
  }

  def getRulesWithRefCountEqualTo(refCount: Int): List[RuleDefinition] = {
    ruleMap.values.filter(_.getRefCount == refCount).toList
  }

  def getUnReferencedRules: List[RuleDefinition] = {
    ruleMap.values.filter(_.getRefCount == 0).toList
  }
}
