package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeErrorStrategy, SnowflakeLexer, SnowflakeParser}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlErrorStrategy, TSqlLexer, TSqlParser}
import com.databricks.labs.remorph.parsers.{ParseException, ProductionErrorCollector}
import com.databricks.labs.remorph.transpilers.{SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler, TranspileException}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream, Parser}

import scala.util.control.NonFatal

trait QueryRunner {
  def runQuery(exampleQuery: ExampleQuery): ReportEntryReport
}

abstract class BaseParserQueryRunner[P <: Parser] extends QueryRunner {
  protected def makeParser(input: String): P
  protected def translate(parser: P): LogicalPlan

  private def showUnresolvedBits(result: LogicalPlan): String = {
    val pattern = "Unresolved[a-zA-Z]+\\([^,)]*".r
    pattern.findAllIn(result.toString).mkString(",")
  }

  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    val parser = makeParser(exampleQuery.query)
    val errHandler = new ProductionErrorCollector(exampleQuery.query, "")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val report = ReportEntryReport()
    try {
      val result = translate(parser)

      if (result.toString.contains("Unresolved")) {
        if (!exampleQuery.expectedTranslation.exists(_.exists(_.isLetter))) {
          // expected translation is empty, indicating that we expect to have Unresolved bits
          // in the output
          report.copy(parsed = 1, statements = 1)
        } else {
          report.copy(
            parsed = 1,
            statements = 1,
            parsing_error = Some(s"Translated query contains unresolved bits: ${showUnresolvedBits(result)}"))
        }
      } else {
        report.copy(parsed = 1, statements = 1)
      }
    } catch {
      case NonFatal(e) =>
        val formattedErrors = errHandler.formatErrors
        val msg = if (formattedErrors.nonEmpty) {
          formattedErrors.mkString("\n")
        } else {
          Option(e.getMessage).getOrElse(s"Unexpected exception of class ${e.getClass} was thrown")
        }
        report.copy(parsing_error = Some(msg))
    }
  }

}

class IsResolvedAsSnowflakeQueryRunner(astBuilder: SnowflakeAstBuilder) extends BaseParserQueryRunner[SnowflakeParser] {

  override protected def makeParser(input: String): SnowflakeParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    parser.setErrorHandler(new SnowflakeErrorStrategy)
    parser
  }

  override protected def translate(parser: SnowflakeParser): LogicalPlan = astBuilder.visit(parser.snowflakeFile())

}

class IsResolvedAsTSqlQueryRunner(astBuilder: TSqlAstBuilder) extends BaseParserQueryRunner[TSqlParser] {

  override protected def makeParser(input: String): TSqlParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    parser.setErrorHandler(new TSqlErrorStrategy)
    parser
  }

  override protected def translate(parser: TSqlParser): LogicalPlan = astBuilder.visit(parser.tSqlFile())

}

class IsTranspiledFromSnowflakeQueryRunner extends QueryRunner {

  val snowflakeTranspiler = new SnowflakeToDatabricksTranspiler
  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    try {
      val transpiled = snowflakeTranspiler.transpile(exampleQuery.query)
      if (exampleQuery.expectedTranslation.exists(_ != transpiled)) {
        ReportEntryReport(
          parsed = 1,
          transpiled = 1,
          statements = 1,
          transpilation_error = Some(s"Unexpected output $transpiled"))
      } else {
        ReportEntryReport(parsed = 1, transpiled = 1, statements = 1)
      }
    } catch {
      case ParseException(msg) =>
        ReportEntryReport(statements = 1, parsing_error = Some(msg))
      case TranspileException(msg) =>
        ReportEntryReport(statements = 1, parsed = 1, transpilation_error = Some(msg))
      case NonFatal(e) =>
        ReportEntryReport(parsing_error = Some(e.getMessage))
    }
  }
}

class IsTranspiledFromTSqlQueryRunner extends QueryRunner {

  val tsqlTranspiler = new TSqlToDatabricksTranspiler
  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    try {
      val transpiled = tsqlTranspiler.transpile(exampleQuery.query)
      if (exampleQuery.expectedTranslation.exists(_ != transpiled)) {
        ReportEntryReport(
          parsed = 1,
          transpiled = 1,
          statements = 1,
          transpilation_error = Some(s"Unexpected output $transpiled"))
      } else {
        ReportEntryReport(parsed = 1, transpiled = 1, statements = 1)
      }
    } catch {
      case ParseException(msg) =>
        ReportEntryReport(statements = 1, parsing_error = Some(msg))
      case TranspileException(msg) =>
        ReportEntryReport(statements = 1, parsed = 1, transpilation_error = Some(msg))
      case NonFatal(e) =>
        ReportEntryReport(parsing_error = Some(e.getMessage))
    }
  }
}
