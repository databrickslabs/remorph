package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import com.github.vertical_blank.sqlformatter.languages.Dialect
import org.antlr.v4.runtime.ParserRuleContext

import scala.util.matching.Regex

sealed trait WorkflowStage
object WorkflowStage {
  case object PARSE extends WorkflowStage
  case object PLAN extends WorkflowStage
  case object OPTIMIZE extends WorkflowStage
  case object GENERATE extends WorkflowStage
}

case class Result(
    stage: WorkflowStage = WorkflowStage.PARSE,
    errorsJson: String = "",
    tree: Option[ParserRuleContext] = None,
    plan: Option[ir.LogicalPlan] = None,
    optimizedPlan: Option[ir.LogicalPlan] = None,
    output: Option[String] = None) {

  def inError(): Boolean = errorsJson.nonEmpty
}

trait Transpiler {
  def transpile(input: SourceCode): Result
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

  protected def parse(input: SourceCode): Result
  protected def toParseTree(input: SourceCode): Result = {
    val parsed = parse(input)
    if (parsed.inError()) parsed
    else Result(stage = WorkflowStage.PARSE, tree = parsed.tree)
  }
  protected def visit(tree: Result): Result
  protected def toPlan(input: SourceCode): Result = {
    val parsed = parse(input)
    val visited = processStage(parsed, r => visit(parsed))
    if (visited.inError()) visited
    else Result(stage = WorkflowStage.PLAN, plan = visited.plan, tree = visited.tree)
  }

  protected def optimize(logicalPlan: Result): Result

  protected def toOptimizedPlan(input: SourceCode): Result = {
    val parsed = parse(input)
    val visited = processStage(parsed, r => visit(parsed))
    val optimized = processStage(visited, r => optimize(visited))
    if (optimized.inError()) optimized
    else Result(stage = WorkflowStage.OPTIMIZE, optimizedPlan = optimized.optimizedPlan)
  }

  protected def generate(optimizedLogicalPlan: Result): Result

  def processStage(currentResult: Result, nextStage: Result => Result): Result = {
    if (currentResult.inError()) currentResult
    else nextStage(currentResult)
  }

  override def transpile(input: SourceCode): Result = {

    val parsed = parse(input)
    val visited = processStage(parsed, r => visit(parsed))
    val optimized = processStage(visited, r => optimize(visited))
    val generated = processStage(optimized, r => generate(optimized))

    if (generated.inError()) generated
    else Result(stage = WorkflowStage.GENERATE, output = Some(format(generated.output.get)))
  }
}
