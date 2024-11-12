package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate.{LogicalPlan, ParsingErrors, PlanGenerationFailure}
import com.databricks.labs.remorph.parsers.{PlanParser, ProductionErrorCollector}
import com.databricks.labs.remorph.parsers.snowflake.rules._
import com.databricks.labs.remorph.{BuildingAst, KoResult, Parsing, Transformation, WorkflowStage, intermediate => ir}
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, Parser, TokenStream}

import scala.util.control.NonFatal

class SnowflakePlanParser extends PlanParser[SnowflakeParser] {

  private val vc = new SnowflakeVisitorCoordinator(SnowflakeParser.VOCABULARY, SnowflakeParser.ruleNames)

  override def parseLogicalPlan(parsing: Parsing): Transformation[LogicalPlan] = {
    val input = CharStreams.fromString(parsing.source)
    val lexer = new SnowflakeLexer(input)
    val tokens = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokens)
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
          ok(createPlan(tokens, tree))
        } catch {
          case NonFatal(e) =>
            lift(KoResult(stage = WorkflowStage.PLAN, PlanGenerationFailure(e)))
        }
      }

    }

  }

  private def createPlan(tokens: TokenStream, tree: ParseTree): LogicalPlan = {
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
