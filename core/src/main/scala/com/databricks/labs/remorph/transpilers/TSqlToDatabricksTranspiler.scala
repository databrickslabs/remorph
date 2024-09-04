package com.databricks.labs.remorph.transpilers

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.generators.sql.{ExpressionGenerator, LogicalPlanGenerator, OptionGenerator}
import com.databricks.labs.remorph.parsers.tsql.rules.{PullLimitUpwards, TSqlCallMapper, TopPercentToLimitSubquery, TrapInsertDefaultsAction}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlErrorStrategy, TSqlLexer, TSqlParser}
import com.databricks.labs.remorph.parsers.{ProductionErrorCollector, intermediate => ir}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write

import java.io.{PrintWriter, StringWriter}

class TSqlToDatabricksTranspiler extends BaseTranspiler {
  private val astBuilder = new TSqlAstBuilder()
  private val optimizer = ir.Rules(
    new TSqlCallMapper,
    ir.AlwaysUpperNameForCallFunction,
    PullLimitUpwards,
    new TopPercentToLimitSubquery,
    TrapInsertDefaultsAction)
  private val exprGenerator = new ExpressionGenerator
  private val optionGenerator = new OptionGenerator(exprGenerator)
  private val generator = new LogicalPlanGenerator(exprGenerator, optionGenerator)

  override def parse(input: SourceCode): Result = {
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
      Result(stage = WorkflowStage.PARSE, errorsJson = errListener.errorsAsJson, tree = Some(tree))
    } else {
      Result(stage = WorkflowStage.PARSE, tree = Some(tree))
    }
  }

  implicit val formats: Formats = Serialization.formats(NoTypeHints)

  override def visit(tree: Result): Result = {
    try {
      val plan = astBuilder.visit(tree.tree.get)
      Result(stage = WorkflowStage.PLAN, plan = Some(plan), tree = tree.tree)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result(stage = WorkflowStage.PLAN, errorsJson = errorJson, tree = tree.tree)
    }
  }

  override def optimize(logicalPlan: Result): Result = {
    try {
      val plan = optimizer.apply(logicalPlan.plan.get)
      Result(
        stage = WorkflowStage.OPTIMIZE,
        plan = logicalPlan.plan,
        optimizedPlan = Some(plan),
        tree = logicalPlan.tree)
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result(stage = WorkflowStage.OPTIMIZE, errorsJson = errorJson, plan = logicalPlan.plan, tree = logicalPlan.tree)
    }
  }

  override def generate(optimizedLogicalPlan: Result): Result = {
    try {
      val output = generator.generate(GeneratorContext(generator), optimizedLogicalPlan.optimizedPlan.get)

      // If the final result is without errors, we can return the output and discard the other generated
      // pieces.
      Result(
        stage = WorkflowStage.GENERATE,
        output = Some(output))
    } catch {
      case e: Exception =>
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        val stackTrace = sw.toString
        val errorJson = write(
          Map("exception" -> e.getClass.getSimpleName, "message" -> e.getMessage, "stackTrace" -> stackTrace))
        Result(
          stage = WorkflowStage.GENERATE,
          errorsJson = errorJson,
          plan = optimizedLogicalPlan.plan,
          tree = optimizedLogicalPlan.tree)
    }
  }

}
