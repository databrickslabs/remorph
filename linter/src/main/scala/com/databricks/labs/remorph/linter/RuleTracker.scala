package com.databricks.labs.remorph.linter

import ujson._

class RuleTracker {

  private var ruleDefMap: Map[String, RuleDefinition] = Map()
  private var ruleRefMap: Map[String, List[RuleReference]] = Map()
  private var orphanedRuleDefs: List[RuleDefinition] = List()
  private var undefinedRules: List[RuleReference] = List()

  // Definition handling
  def addRuleDef(rule: RuleDefinition): Unit = {
    ruleDefMap += (rule.ruleName -> rule)
  }

  def getRuleDef(ruleName: String): RuleDefinition = {
    ruleDefMap(ruleName)
  }

  def getRuleMap: Map[String, RuleDefinition] = {
    ruleDefMap
  }

  def getRuleDefCount: Int = {
    ruleDefMap.size
  }

  def getRuleDefNames: List[String] = {
    ruleDefMap.keys.toList
  }

  def getRuleDefinitions: List[RuleDefinition] = {
    ruleDefMap.values.toList
  }

  def getRuleDefinition(ruleName: String): RuleDefinition = {
    ruleDefMap(ruleName)
  }

  /**
   * How many times the rule definition is referenced in the grammar
   * @param ruleName
   *   the name of the rule
   * @return
   */
  def getRuleDefRefCount(ruleName: String): Int = {
    ruleRefMap.get(ruleName).map(_.size).getOrElse(0)
  }

  def getRuleDefLineNo(ruleName: String): Int = {
    ruleDefMap.get(ruleName).map(_.lineNo).getOrElse(-1)
  }

  // Reference handling

  def addRuleRef(ruleRef: RuleReference): Unit = {
    val name = ruleRef.ruleName
    ruleRefMap += (name -> (ruleRef :: ruleRefMap.getOrElse(name, Nil)))
  }

  def getRuleRefs(ruleName: String): List[RuleReference] = {
    ruleRefMap(ruleName)
  }

  def getRuleRefCount(ruleName: String): Int = {
    ruleRefMap.get(ruleName).map(_.size).getOrElse(0)
  }

  def getRuleRefsByCondition(condition: RuleReference => Boolean): List[RuleReference] = {
    ruleRefMap.values.flatten.filter(condition).toList
  }

  // Reconciliation
  // This is where we reconcile the rule definitions with the references to discover
  // undefined and unreferenced rules

  def reconcileRules(): OrphanedRuleSummary = {
    orphanedRuleDefs = ruleDefMap.values.filterNot(rule => ruleRefMap.contains(rule.ruleName) || rule.isExternal).toList
    undefinedRules = ruleRefMap.values.flatten.filterNot(ref => ruleDefMap.contains(ref.ruleName)).toList
    OrphanedRuleSummary(orphanedRuleDefs, undefinedRules)
  }

  def getOrphanedRuleDefs: List[RuleDefinition] = orphanedRuleDefs
  def getUndefinedRules: List[RuleReference] = undefinedRules
}

case class OrphanedRuleSummary(orphanedRuleDef: List[RuleDefinition], undefinedRules: List[RuleReference]) {
  def toJSON: Obj = {
    val orphanedRuleDefJson = orphanedRuleDef.map { rule =>
      Obj("lineNo" -> rule.lineNo, "ruleName" -> rule.ruleName)
    }

    val undefinedRulesJson = undefinedRules.map { rule =>
      Obj(
        "lineNo" -> rule.lineNo,
        "charStart" -> rule.charStart,
        "charEnd" -> rule.charEnd,
        "ruleName" -> rule.ruleName)
    }

    Obj(
      "orphanCount" -> orphanedRuleDef.size,
      "undefinedRuleCount" -> undefinedRules.size,
      "orphanedRuleDef" -> orphanedRuleDefJson,
      "undefinedRules" -> undefinedRulesJson)
  }

  def hasIssues: Boolean = orphanedRuleDef.nonEmpty || undefinedRules.nonEmpty
}
