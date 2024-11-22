package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.preprocessors.jinga.JingaProcessor
import com.databricks.labs.remorph.preprocessors.jinja.JinjaProcessor
import com.databricks.labs.remorph.{Generating, Optimizing, Parsing, PreProcessing, Transformation, TransformationConstructors, intermediate => ir}
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.core.FormatConfig
import com.github.vertical_blank.sqlformatter.languages.Dialect
import org.antlr.v4.runtime.ParserRuleContext
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}

import scala.util.matching.Regex

trait Transpiler {
  def transpile(input: PreProcessing): Transformation[String]
}

class Sed(rules: (String, String)*) {
  private[this] val compiledRules: Seq[(Regex, String)] = rules.map { case (regex, replace) =>
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
  private[this] val sqlFormat = FormatConfig
    .builder()
    .indent("  ")
    .uppercase(true)
    .maxColumnLength(100)
    .build()

  private[this] val formatter = SqlFormatter.of(Dialect.SparkSql)

  // sometimes we cannot just ignore legacy SQLGlot formatter and have to add hacks
  private[this] val hacks = new Sed("EXISTS\\(" -> s"EXISTS (")

  def format(input: String): String = {
    val pretty = formatter.format(input, sqlFormat)
    hacks.apply(pretty)
  }
}

abstract class BaseTranspiler extends Transpiler with Formatter with TransformationConstructors {

  protected val planParser: PlanParser[_]
  private[this] val generator = new SqlGenerator
  private[this] val jinjaProcessor = new JinjaProcessor

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  protected def pre(input: PreProcessing): Transformation[Parsing] = jinjaProcessor.pre(input)

  protected def parse(input: Parsing): Transformation[ParserRuleContext] = planParser.parse(input)

  protected def visit(tree: ParserRuleContext): Transformation[ir.LogicalPlan] = planParser.visit(tree)

  // TODO: optimizer really should be its own thing and not part of PlanParser
  // I have put it here for now until we discuss^h^h^h^h^h^h^hSerge dictates where it should go ;)
  protected def optimize(logicalPlan: ir.LogicalPlan): Transformation[ir.LogicalPlan] =
    planParser.optimize(logicalPlan)

  protected def generate(optimizedLogicalPlan: ir.LogicalPlan): Transformation[String] = {
    update {
      case o: Optimizing =>
        Generating(
          optimizedPlan = optimizedLogicalPlan,
          currentNode = optimizedLogicalPlan,
          ctx = generator.initialGeneratorContext,
          previousPhase = Some(o))
      case _ =>
        Generating(
          optimizedPlan = optimizedLogicalPlan,
          currentNode = optimizedLogicalPlan,
          ctx = generator.initialGeneratorContext,
          previousPhase = None)
    }.flatMap { _ =>
      generator.generate(optimizedLogicalPlan)
    }
  }

  protected def post(input: String): Transformation[String] = jinjaProcessor.post(input)

  override def transpile(input: PreProcessing): Transformation[String] = {
    set(input)
      .flatMap(_ => pre(input))
      .flatMap(parse)
      .flatMap(visit)
      .flatMap(optimize)
      .flatMap(generate)
      .flatMap(post)
  }
}
