package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.ExampleQuery
import com.databricks.labs.remorph.transpilers.WorkflowStage.PARSE
import com.databricks.labs.remorph.transpilers.{Formatter, SnowflakeToDatabricksTranspiler, SourceCode, TSqlToDatabricksTranspiler}
import com.databricks.labs.remorph.utils.Strings

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
  private val snowflakeTranspiler = new SnowflakeToDatabricksTranspiler

  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    val transpiled = snowflakeTranspiler.transpile(SourceCode(exampleQuery.query))
    if (transpiled.inError()) {
      if (transpiled.stage == PARSE) {
        ReportEntryReport(statements = 1, parsing_error = Some(transpiled.errorsJson))
      } else {
        ReportEntryReport(statements = 1, transpilation_error = Some(transpiled.errorsJson))
      }
    } else if (exampleQuery.expectedTranslation.map(format).exists(_ != transpiled.output.getOrElse(""))) {
      val expected = exampleQuery.expectedTranslation.getOrElse("")
      ReportEntryReport(
        parsed = 1,
        transpiled = 1,
        statements = 1,
        transpilation_error = Some(compareQueries(expected, transpiled.output.getOrElse(""))))
    } else {
      ReportEntryReport(parsed = 1, transpiled = 1, statements = 1)
    }
  }
}

class IsTranspiledFromTSqlQueryRunner extends QueryRunner {
  private val tsqlTranspiler = new TSqlToDatabricksTranspiler
  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    val transpiled = tsqlTranspiler.transpile(SourceCode(exampleQuery.query))
    if (transpiled.inError()) {
      if (transpiled.stage == PARSE) {
        ReportEntryReport(statements = 1, parsing_error = Some(transpiled.errorsJson))
      } else {
        ReportEntryReport(statements = 1, transpilation_error = Some(transpiled.errorsJson))
      }
    } else if (exampleQuery.expectedTranslation.map(format).exists(_ != transpiled.output.getOrElse(""))) {
      val expected = exampleQuery.expectedTranslation.getOrElse("")
      ReportEntryReport(
        parsed = 1,
        transpiled = 1,
        statements = 1,
        transpilation_error = Some(compareQueries(expected, transpiled.output.getOrElse(""))))
    } else {
      ReportEntryReport(parsed = 1, transpiled = 1, statements = 1)
    }
  }
}
