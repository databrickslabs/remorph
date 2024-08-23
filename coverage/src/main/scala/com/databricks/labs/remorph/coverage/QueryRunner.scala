package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.parsers.ParseException
import com.databricks.labs.remorph.queries.ExampleQuery
import com.databricks.labs.remorph.transpilers.{Formatter, SnowflakeToDatabricksTranspiler, TSqlToDatabricksTranspiler, TranspileException}
import com.databricks.labs.remorph.utils.Strings

import scala.util.control.NonFatal

trait QueryRunner extends Formatter {
  def runQuery(exampleQuery: ExampleQuery): ReportEntryReport

  protected def compareQueries(expected: String, actual: String): String = {
    s"""
       |=== Unexpected output (expected vs actual) ===
       |${Strings.sideBySide(format(expected), format(actual)).mkString("\n")}
       |""".stripMargin
  }
}

class IsTranspiledFromSnowflakeQueryRunner extends QueryRunner {
  val snowflakeTranspiler = new SnowflakeToDatabricksTranspiler
  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    try {
      val transpiled = snowflakeTranspiler.transpile(exampleQuery.query)
      if (exampleQuery.expectedTranslation.map(format).exists(_ != transpiled)) {
        val expected = exampleQuery.expectedTranslation.getOrElse("")
        ReportEntryReport(
          parsed = 1,
          transpiled = 1,
          statements = 1,
          transpilation_error = Some(compareQueries(expected, transpiled)))
      } else {
        ReportEntryReport(parsed = 1, transpiled = 1, statements = 1)
      }
    } catch {
      case ParseException(msg) =>
        ReportEntryReport(statements = 1, parsing_error = Some(msg))
      case TranspileException(msg) =>
        ReportEntryReport(statements = 1, parsed = 1, transpilation_error = Some(msg))
      case NonFatal(e) =>
        ReportEntryReport(parsing_error = Some(s"${e.getClass.getSimpleName}: ${e.getMessage}"))
    }
  }
}

class IsTranspiledFromTSqlQueryRunner extends QueryRunner {
  val tsqlTranspiler = new TSqlToDatabricksTranspiler
  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    try {
      val transpiled = tsqlTranspiler.transpile(exampleQuery.query)
      if (exampleQuery.expectedTranslation.map(format).exists(_ != transpiled)) {
        val expected = exampleQuery.expectedTranslation.getOrElse("")
        ReportEntryReport(
          parsed = 1,
          transpiled = 1,
          statements = 1,
          transpilation_error = Some(compareQueries(expected, transpiled)))
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
