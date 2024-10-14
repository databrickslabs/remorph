package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.snowflake.rules._
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.{CharStream, Lexer, ParserRuleContext, TokenStream}

class SnowflakePlanParser extends PlanParser[SnowflakeParser] {

  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  private val vc = new SnowflakeVisitorCoordinator(SnowflakeParser.VOCABULARY, SnowflakeParser.ruleNames)

  override protected def createLexer(input: CharStream): Lexer = new SnowflakeLexer(input)
  override protected def createParser(stream: TokenStream): SnowflakeParser = new SnowflakeParser(stream)
  override protected def createTree(parser: SnowflakeParser): ParserRuleContext = parser.snowflakeFile()
  override protected def createPlan(tree: ParserRuleContext): ir.LogicalPlan = vc.astBuilder.visit(tree)
  override protected def addErrorStrategy(parser: SnowflakeParser): Unit =
    parser.setErrorHandler(new SnowflakeErrorStrategy)
  def dialect: String = "snowflake"

  // TODO: Note that this is not the correct place for the optimizer, but it is here for now
  override protected def createOptimizer: ir.Rules[ir.LogicalPlan] = {
    ir.Rules(
      new ConvertFractionalSecond,
      new FlattenLateralViewToExplode(),
      new SnowflakeCallMapper,
      ir.AlwaysUpperNameForCallFunction,
      new UpdateToMerge,
      new CastParseJsonToFromJson(generator),
      new TranslateWithinGroup,
      new FlattenNestedConcat,
      new CompactJsonAccess,
      new DeleteOnMultipleColumns)
  }
}
