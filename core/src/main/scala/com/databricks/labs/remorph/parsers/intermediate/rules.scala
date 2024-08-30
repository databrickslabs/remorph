package com.databricks.labs.remorph.parsers.intermediate

abstract class Rule[T <: TreeNode[_]] {
  val ruleName: String = {
    val className = getClass.getName
    if (className endsWith "$") className.dropRight(1) else className
  }

  def apply(plan: T): T
}

case class Rules[T <: TreeNode[_]](rules: Rule[T]*) extends Rule[T] {
  def apply(plan: T): T = {
    rules.foldLeft(plan) { case (p, rule) => rule(p) }
  }
}

// We use UPPERCASE convention to refer to function names in the codebase,
// but it is not a requirement in the transpiled code. This rule is used to
// enforce the convention.
object AlwaysUpperNameForCallFunction extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan transformAllExpressions { case CallFunction(name, args) =>
    CallFunction(name.toUpperCase(), args)
  }
}
