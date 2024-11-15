package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate.LogicalPlan
import com.databricks.labs.remorph.parsers.{AntlrPlanParser, PlanParser, ProductionErrorCollector}
import com.databricks.labs.remorph.parsers.snowflake.rules._
import com.databricks.labs.remorph.{Parsing, Transformation, intermediate => ir}
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

class SnowflakePlanParser extends PlanParser with AntlrPlanParser {

  private val vc = new SnowflakeVisitorCoordinator(SnowflakeParser.VOCABULARY, SnowflakeParser.ruleNames)

  override def parseLogicalPlan(parsing: Parsing): Transformation[LogicalPlan] = {
    val input = CharStreams.fromString(parsing.source)
    val lexer = new SnowflakeLexer(input)
    val tokens = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokens)
    parser.setErrorHandler(new SnowflakeErrorStrategy)
    val errListener = setErrorListener(parser, new ProductionErrorCollector(parsing.source, parsing.filename))
    val tree = parser.snowflakeFile()
    generatePlan(tree, () => createPlan(tokens, tree), errListener)
  }

  private def createPlan(tokens: CommonTokenStream, tree: ParseTree): LogicalPlan = {
    val plan = vc.astBuilder.visit(tree)
    plan
  }

  def dialect: String = "snowflake"

  // TODO: Note that this is not the correct place for the optimizer, but it is here for now
  override protected def createOptimizer: ir.Rules[ir.LogicalPlan] = {
    ir.Rules(
      new ConvertFractionalSecond,
      new FlattenLateralViewToExplode(),
      new SnowflakeCallMapper,
      ir.AlwaysUpperNameForCallFunction,
      new UpdateToMerge,
      new CastParseJsonToFromJson,
      new TranslateWithinGroup,
      new FlattenNestedConcat,
      new CompactJsonAccess,
      new DealiasInlineColumnExpressions)
  }
}
