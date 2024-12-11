package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.{Transformation, TransformationConstructors}

abstract class Rule[T <: TreeNode[_]] {
  val ruleName: String = {
    val className = getClass.getName
    if (className endsWith "$") className.dropRight(1) else className
  }

  def apply(tree: T): Transformation[T]
}

case class Rules[T <: TreeNode[_]](rules: Rule[T]*) extends Rule[T] with TransformationConstructors {
  def apply(tree: T): Transformation[T] = {
    rules.foldLeft(ok(tree)) { case (p, rule) => p.flatMap(rule.apply) }
  }
}

// We use UPPERCASE convention to refer to function names in the codebase,
// but it is not a requirement in the transpiled code. This rule is used to
// enforce the convention.
object AlwaysUpperNameForCallFunction extends Rule[LogicalPlan] with TransformationConstructors {
  def apply(plan: LogicalPlan): Transformation[LogicalPlan] = plan transformAllExpressions {
    case CallFunction(name, args) =>
      ok(CallFunction(name.toUpperCase(), args))
  }
}
