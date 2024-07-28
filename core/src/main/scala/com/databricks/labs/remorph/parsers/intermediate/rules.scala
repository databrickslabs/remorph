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