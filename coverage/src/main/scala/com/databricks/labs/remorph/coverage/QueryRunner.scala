package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.parsers.ProductionErrorCollector
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeAstBuilder, SnowflakeLexer, SnowflakeParser}
import com.databricks.labs.remorph.parsers.tsql.{TSqlAstBuilder, TSqlLexer, TSqlParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

import scala.util.control.NonFatal

trait QueryRunner {
  def runQuery(query: String): ReportEntryReport
}

class IsResolvedAsSnowflakeQueryRunner(astBuilder: SnowflakeAstBuilder) extends QueryRunner {

  private def makeParser(input: String): SnowflakeParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    parser
  }

  override def runQuery(query: String): ReportEntryReport = {
    val parser = makeParser(query)
    val errHandler = new ProductionErrorCollector(query, "")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val report = ReportEntryReport()
    try {
      val result = astBuilder.visit(parser.snowflakeFile())

      if (result.toString.contains("Unresolved")) {
        report.copy(
          parsed = 1,
          statements = 1,
          transpilation_error = Some(s"Translated query contains unresolved bits: $result"))
      } else {
        report.copy(parsed = 1, transpiled = 1, statements = 1, transpiled_statements = 1)
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

class IsResolvedAsTSqlQueryRunner(astBuilder: TSqlAstBuilder) extends QueryRunner {

  private def makeParser(input: String): TSqlParser = {
    val inputString = CharStreams.fromString(input)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    parser
  }

  override def runQuery(query: String): ReportEntryReport = {
    val parser = makeParser(query)
    val errHandler = new ProductionErrorCollector(query, "")
    parser.removeErrorListeners()
    parser.addErrorListener(errHandler)
    val report = ReportEntryReport()
    try {
      val result = astBuilder.visit(parser.tSqlFile())

      if (result.toString.contains("Unresolved")) {
        report.copy(
          parsed = 1,
          statements = 1,
          transpilation_error = Some(s"Translated query IR has unresolved elements: $result"))
      } else {
        report.copy(parsed = 1, transpiled = 1, statements = 1, transpiled_statements = 1)
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
