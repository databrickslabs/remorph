package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig

trait Transpiler {
  def transpile(input: String): String
  def parse(input: String): ir.LogicalPlan
}

trait Formatter {
  private val sqlFormat = FormatConfig
    .builder()
    .indent("  ")
    .uppercase(true)
    .maxColumnLength(100)
    .build()

  def format(input: String): String = SqlFormatter.format(input, sqlFormat)
}

abstract class BaseTranspiler extends Transpiler with Formatter {

  override def parse(input: String): ir.LogicalPlan

  protected def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): String

  override def transpile(input: String): String = {
    val parsed = parse(input)
    val optimized = optimize(parsed)
    val generated = generate(optimized)
    format(generated)
  }
}
