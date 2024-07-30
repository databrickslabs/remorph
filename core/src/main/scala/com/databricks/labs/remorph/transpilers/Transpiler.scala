package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

trait Transpiler {

  def parse(input: String): ir.LogicalPlan

  def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan

  def generate(optimizedLogicalPlan: ir.LogicalPlan): String

  def transpile(input: String): String = {
    val parsed = parse(input)
    val optimized = optimize(parsed)
    generate(optimized)
  }
}
