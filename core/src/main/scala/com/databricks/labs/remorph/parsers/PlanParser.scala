package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.{Result, SourceCode, WorkflowStage}
import org.antlr.v4.runtime.{CharStream, CharStreams, CommonTokenStream, Parser, ParserRuleContext, TokenSource, TokenStream}
import org.json4s.jackson.Serialization
import org.json4s.{Formats, NoTypeHints}
import org.json4s.jackson.Serialization.write

import java.io.{PrintWriter, StringWriter}

trait PlanParser[P <: Parser] {

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  protected def createLexer(input: CharStream): TokenSource
  protected def createParser(stream: TokenStream): P
  protected def createTree(parser: P): ParserRuleContext
  protected def createPlan(tree: ParserRuleContext): ir.LogicalPlan
  protected def addErrorStrategy(parser: P): Unit
  def dialect: String

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  protected def createOptimizer: ir.Rules[ir.LogicalPlan]

  /**
   * Parse the input source code into a Parse tree
   * @param input The source code with filename
   * @return Returns a parse tree on success otherwise a description of the errors
   */
  def parse(input: SourceCode): Result[ParserRuleContext] = {
    val inputString = CharStreams.fromString(input.source)
    val tokenStream = new CommonTokenStream(createLexer(inputString))
    val parser = createParser(tokenStream)
    addErrorStrategy(parser)
    val errListener = new ProductionErrorCollector(input.source, input.filename)
    parser.removeErrorListeners()
    parser.addErrorListener(errListener)
    val tree = createTree(parser)
    // TODO: Should we return the error listener, or perhaps the collection of errors and not JSON at this stage?
    if (errListener.errorCount > 0) {
      Result.Failure(stage = WorkflowStage.PARSE, errListener.errorsAsJson)
    } else {
      Result.Success(tree)
    }
  }

  /**
   * Visit the parse tree and create a logical plan
   * @param tree The parse tree
   * @return Returns a logical plan on success otherwise a description of the errors
   */
  def visit(tree: ParserRuleContext): Result[ir.LogicalPlan] = {
    try {
      val plan = createPlan(tree)
      Result.Success(plan)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result.Failure(stage = WorkflowStage.PLAN, errorJson)
    }
  }

  // TODO: This is probably not where the optimizer should be as this is a Plan "Parser" - it is here for now
  /**
   * Optimize the logical plan
   *
   * @param plan The logical plan
   * @return Returns an optimized logical plan on success otherwise a description of the errors
   */
  def optimize(logicalPlan: ir.LogicalPlan): Result[ir.LogicalPlan] = {
    try {
      val plan = createOptimizer.apply(logicalPlan)
      Result.Success(plan)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result.Failure(stage = WorkflowStage.OPTIMIZE, errorJson)
    }
  }

}
