package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate.{LogicalPlan, ParsingErrors, PlanGenerationFailure}
import com.databricks.labs.remorph.parsers.{PlanParser, ProductionErrorCollector}
import com.databricks.labs.remorph.parsers.snowflake.rules._
import com.databricks.labs.remorph.{BuildingAst, KoResult, Parsing, Transformation, WorkflowStage, intermediate => ir}
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, Parser}

import scala.util.control.NonFatal

class SnowflakePlanParser extends PlanParser[SnowflakeParser] {

  private val vc = new SnowflakeVisitorCoordinator(SnowflakeParser.VOCABULARY, SnowflakeParser.ruleNames)

  override protected def createLexer(input: CharStream): Lexer = new SnowflakeLexer(input)
  override protected def createParser(stream: TokenStream): SnowflakeParser = new SnowflakeParser(stream)
  override protected def createTree(parser: SnowflakeParser): ParserRuleContext = parser.snowflakeFile()
  override protected def createPlan(tree: ParserRuleContext): ir.LogicalPlan = vc.astBuilder.visit(tree)
  override protected def addErrorStrategy(parser: SnowflakeParser): Unit =
    parser.setErrorHandler(new SnowflakeErrorStrategy)
    val errListener = new ProductionErrorCollector(parsing.source, parsing.filename)
    parser.removeErrorListeners()
    parser.addErrorListener(errListener)
    val tree = parser.snowflakeFile()
    if (errListener.errorCount > 0) {
      lift(KoResult(stage = WorkflowStage.PARSE, ParsingErrors(errListener.errors)))
    } else {
      update {
        case p: Parsing => BuildingAst(tree, Some(p))
        case _ => BuildingAst(tree)
      }.flatMap { _ =>
        try {
          ok(createPlan(parser, tree))
        } catch {
          case NonFatal(e) =>
            lift(KoResult(stage = WorkflowStage.PLAN, PlanGenerationFailure(e)))
        }
      }

    }

  }

  private def createPlan(parser: Parser, tree: ParseTree): LogicalPlan = {
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
      new CompactJsonAccess)
  }
}
