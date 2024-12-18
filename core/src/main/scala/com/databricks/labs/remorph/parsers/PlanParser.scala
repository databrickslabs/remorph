package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.intermediate.{ParsingErrors, PlanGenerationFailure}
import com.databricks.labs.remorph.{BuildingAst, KoResult, OkResult, Optimizing, Parsing, PartialResult, Transformation, TransformationConstructors, WorkflowStage, intermediate => ir}
import org.antlr.v4.runtime._
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}

import scala.util.control.NonFatal

trait PlanParser[P <: Parser] extends TransformationConstructors {

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  protected def createLexer(input: CharStream): Lexer
  protected def createParser(stream: TokenStream): P
  protected def createTree(parser: P): ParserRuleContext
  protected def createPlan(tree: ParserRuleContext): ir.LogicalPlan
  protected def addErrorStrategy(parser: P): Unit
  def dialect: String

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  protected def createOptimizer: ir.Rules[ir.LogicalPlan]

  /**
   * Parse the input source code into a Parse tree
   * @return Returns a parse tree on success otherwise a description of the errors
   */
  def parse: Transformation[ParserRuleContext] = {

    getCurrentPhase.flatMap {
      case Parsing(source, filename, _, _) =>
        val inputString = CharStreams.fromString(source)
        val lexer = createLexer(inputString)
        val tokenStream = new CommonTokenStream(lexer)
        val parser = createParser(tokenStream)
        addErrorStrategy(parser)
        val errListener = new ProductionErrorCollector(source, filename)
        parser.removeErrorListeners()
        parser.addErrorListener(errListener)
        val tree = createTree(parser)
        if (errListener.errorCount > 0) {
          lift(PartialResult(tree, ParsingErrors(errListener.errors)))
        } else {
          lift(OkResult(tree))
        }
      case other => ko(WorkflowStage.PARSE, ir.IncoherentState(other, classOf[Parsing]))
    }
  }

  /**
   * Visit the parse tree and create a logical plan
   * @param tree The parse tree
   * @return Returns a logical plan on success otherwise a description of the errors
   */
  def visit(tree: ParserRuleContext): Transformation[ir.LogicalPlan] = {
    updatePhase {
      case p: Parsing => BuildingAst(tree, Some(p))
      case _ => BuildingAst(tree)
    }.flatMap { _ =>
      try {
        ok(createPlan(tree))
      } catch {
        case NonFatal(e) =>
          lift(KoResult(stage = WorkflowStage.PLAN, PlanGenerationFailure(e)))
      }
    }
  }

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  /**
   * Optimize the logical plan
   *
   * @param logicalPlan The logical plan
   * @return Returns an optimized logical plan on success otherwise a description of the errors
   */
  def optimize(logicalPlan: ir.LogicalPlan): Transformation[ir.LogicalPlan] = {
    updatePhase {
      case b: BuildingAst => Optimizing(logicalPlan, Some(b))
      case _ => Optimizing(logicalPlan)
    }.flatMap { _ =>
      createOptimizer.apply(logicalPlan)
    }
  }
}
