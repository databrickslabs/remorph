package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

trait Transpiler {
  def transpile(input: String): String
  def parse(input: String): ir.LogicalPlan
}

abstract class BaseTranspiler extends Transpiler {

  override def parse(input: String): ir.LogicalPlan

  protected def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): String

  override def transpile(input: String): String = {
    val parsed = parse(input)
    val optimized = optimize(parsed)
    generate(optimized)
  }
}