package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import org.apache.spark.sql.catalyst.parser.CatalystSqlParser

trait Transpiler {
  def transpile(input: String, skipValiation: Boolean = false): String
}

trait Validator {
  def validate(transpiledCode: String): String = {
    try {
      CatalystSqlParser.parsePlan(transpiledCode)
      transpiledCode
    } catch {
      // TODO Enhance custom messaging to support complex errors we encounter
      case e: Exception =>
        e.getMessage ++ transpiledCode
    }
  }
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

abstract class BaseTranspiler extends Transpiler with Formatter with Validator{

  protected def parse(input: String): ir.LogicalPlan

  protected def optimize(logicalPlan: ir.LogicalPlan): ir.LogicalPlan

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): String

  override def transpile(input: String, skipValidation: Boolean): String = {
    val parsed = parse(input)
    val optimized = optimize(parsed)
    val generated = generate(optimized)
    if (!skipValidation) return format(validate(generated))
    format(generated)
  }
}
