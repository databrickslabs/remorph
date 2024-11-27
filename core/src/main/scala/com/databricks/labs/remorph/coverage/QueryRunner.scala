package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.WorkflowStage.PARSE
import com.databricks.labs.remorph.intermediate.{RemorphError, UnexpectedOutput}
import com.databricks.labs.remorph.queries.ExampleQuery
import com.databricks.labs.remorph.transpilers._
import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult, PreProcessing}

trait QueryRunner extends Formatter {
  def runQuery(exampleQuery: ExampleQuery): ReportEntryReport

}

abstract class BaseQueryRunner(transpiler: Transpiler) extends QueryRunner {

  private def createReportEntryReport(
      exampleQuery: ExampleQuery,
      output: String,
      error: Option[RemorphError] = None): ReportEntryReport = {
    val expected = exampleQuery.expectedTranslation
    val parsed = if (error.isEmpty) 1 else 0
    val formattedOutput = if (exampleQuery.shouldFormat) format(output) else output
    val formattedExpected = expected.map(e => if (exampleQuery.shouldFormat) format(e) else e)

    if (formattedExpected.exists(_ != formattedOutput)) {
      ReportEntryReport(
        parsed = parsed,
        statements = 1,
        failures = Some(UnexpectedOutput(formattedExpected.get, formattedOutput)))
    } else {
      ReportEntryReport(
        parsed = parsed,
        transpiled = if (parsed == 1) 1 else 0,
        statements = 1,
        transpiled_statements = 1,
        failures = error)
    }
  }

  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    transpiler
      .transpile(PreProcessing(exampleQuery.query))
      .runAndDiscardState(PreProcessing(exampleQuery.query)) match {
      case KoResult(PARSE, error) => ReportEntryReport(statements = 1, failures = Some(error))
      case KoResult(_, error) =>
        // If we got past the PARSE stage, then remember to record that we parsed it correctly
        ReportEntryReport(parsed = 1, statements = 1, failures = Some(error))
      case PartialResult(output, error) =>
        // Even with parsing errors, we will attempt to transpile the query, and parsing errors will be recorded in
        // entry report
        createReportEntryReport(exampleQuery, output, Some(error))
      case OkResult(output) =>
        createReportEntryReport(exampleQuery, output)
    }
  }
}

class IsTranspiledFromSnowflakeQueryRunner extends BaseQueryRunner(new SnowflakeToDatabricksTranspiler)

class IsTranspiledFromTSqlQueryRunner extends BaseQueryRunner(new TSqlToDatabricksTranspiler)
