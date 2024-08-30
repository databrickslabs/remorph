package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import com.github.vertical_blank.sqlformatter.languages.Dialect
import scala.util.matching.Regex

trait Transpiler {
  def transpile(input: String): String
}

class Sed(rules: (String, String)*) {
  private val compiledRules: Seq[(Regex, String)] = rules.map { case (regex, replace) =>
    (regex.r, replace)
  }

  def apply(src: String): String = {
    compiledRules.foldLeft(src) { (currentSrc, rule) =>
      val (regex, replace) = rule
      regex.replaceAllIn(currentSrc, replace)
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

  private val formatter = SqlFormatter.of(Dialect.SparkSql)

  // sometimes we cannot just ignore legacy SQLGlot formatter and have to add hacks
  private val hacks = new Sed("EXISTS\\(" -> s"EXISTS (")

  def format(input: String): String = {
    val pretty = formatter.format(input, sqlFormat)
    hacks.apply(pretty)
  }
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
