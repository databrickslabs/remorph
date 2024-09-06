package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TSqlCallMapper, TopPercentToLimitSubquery, TrapInsertDefaultsAction}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlErrorStrategy, TSqlLexer, TSqlParser}
import com.databricks.labs.remorph.parsers.{ProductionErrorCollector, intermediate => ir}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, ParserRuleContext}
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write

import java.io.{PrintWriter, StringWriter}

class TSqlToDatabricksTranspiler extends BaseTranspiler {
  private val astBuilder = new TSqlAstBuilder()
  private val optimizer = ir.Rules(
    ir.AlwaysUpperNameForCallFunction,
    PullLimitUpwards,
    new TopPercentToLimitSubquery,
    TrapInsertDefaultsAction)
  private val generator = new LogicalPlanGenerator(new ExpressionGenerator(new TSqlCallMapper()))

  override def parse(input: SourceCode): Result[ParserRuleContext] = {
    val inputString = CharStreams.fromString(input.source)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    parser.setErrorHandler(new TSqlErrorStrategy)
    val errListener = new ProductionErrorCollector(input.source, input.filename)
    parser.removeErrorListeners()
    parser.addErrorListener(errListener)
    val tree = parser.tSqlFile()
    if (errListener.errorCount > 0) {
      Result.Failure(stage = WorkflowStage.PARSE, errListener.errorsAsJson)
    } else {
      Result.Success(tree)
    }
  }

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  override def visit(tree: ParserRuleContext): Result[ir.LogicalPlan] = {
    try {
      val plan = astBuilder.visit(tree)
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

  override def optimize(logicalPlan: ir.LogicalPlan): Result[ir.LogicalPlan] = {
    try {
      val plan = optimizer.apply(logicalPlan)
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

  override def generate(optimizedLogicalPlan: ir.LogicalPlan): Result[String] = {
    try {
      val output = generator.generate(GeneratorContext(generator), optimizedLogicalPlan)

      // If the final result is without errors, we can return the output and discard the other generated
      // pieces.
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

}
