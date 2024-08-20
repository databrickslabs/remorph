package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import com.github.vertical_blank.sqlformatter.languages.Dialect

trait Transpiler {
  def transpile(input: String): String
}

trait Formatter {
  private val sqlFormat = FormatConfig
    .builder()
    .indent("  ")
    .uppercase(true)
    .maxColumnLength(100)
    .build()

  def format(input: String): String = SqlFormatter.of(Dialect.SparkSql) format (input, sqlFormat)
}

abstract class BaseTranspiler extends Transpiler with Formatter {

  protected def parse(input: String): ir.LogicalPlan

  protected def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): String

  override def transpile(input: String): String = {
    val parsed = parse(input)
    val optimized = optimize(parsed)
    val generated = generate(optimized)
    format(generated)
  }
}
