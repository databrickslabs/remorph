package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.parsers.{PlanParser, intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import com.github.vertical_blank.sqlformatter.languages.Dialect
import org.antlr.v4.runtime.ParserRuleContext
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}
import org.json4s.jackson.Serialization.write

import java.io.{PrintWriter, StringWriter}
import scala.util.matching.Regex


sealed trait WorkflowStage
object WorkflowStage {
  case object PARSE extends WorkflowStage
  case object PLAN extends WorkflowStage
  case object OPTIMIZE extends WorkflowStage
  case object GENERATE extends WorkflowStage
}

trait Transpiler {
  def transpile(input: SourceCode): Result[String]
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

abstract class BaseTranspiler extends Transpiler with Formatter with Parser {

  protected val planParser: PlanParser[_]
  protected val exprGenerator = new ExpressionGenerator
  protected val optionGenerator = new OptionGenerator(exprGenerator)
  protected val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  protected def parse(input: SourceCode): Result[ParserRuleContext] = planParser.parse(input)

  protected def visit(tree: ParserRuleContext): Result[ir.LogicalPlan] = planParser.visit(tree)

  // TODO: optimizer really should be its own thing and not part of PlanParser
  // I have put it here for now until we discuss^h^h^h^h^h^h^hSerge dictates where it should go ;)
  protected def optimize(logicalPlan: ir.LogicalPlan): Result[ir.LogicalPlan] = planParser.optimize(logicalPlan)

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): Result[String] = {
    try {
      val output = generator.generate(GeneratorContext(generator), optimizedLogicalPlan)
      Result.Success(output)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result.Failure(stage = WorkflowStage.GENERATE, errorJson)
    }
  }

  override def transpile(input: SourceCode): Result[String] = {
    parse(input).flatMap(visit).flatMap(optimize).flatMap(generate)
  }
}
