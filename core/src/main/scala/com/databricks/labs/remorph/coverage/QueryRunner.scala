package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.ExampleQuery
import com.databricks.labs.remorph.Result
import com.databricks.labs.remorph.WorkflowStage.PARSE
import com.databricks.labs.remorph.intermediate.UnexpectedOutput
import com.databricks.labs.remorph.transpilers._
import com.databricks.labs.remorph.utils.Strings
import upickle.default.write

trait QueryRunner extends Formatter {
  def runQuery(exampleQuery: ExampleQuery): ReportEntryReport

}

abstract class BaseQueryRunner(transpiler: Transpiler) extends QueryRunner {

  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    transpiler.transpile(SourceCode(exampleQuery.query)) match {
      case Result.Failure(PARSE, errors) =>
        ReportEntryReport(statements = 1, parsing_error = Some(write(errors.toList)))
      case Result.Failure(_, errors) =>
        // If we got past the PARSE stage, then remember to record that we parsed it correctly
        ReportEntryReport(parsed = 1, statements = 1, transpilation_error = Some(write(errors.toList)))
      case Result.Success(output) =>
        if (exampleQuery.expectedTranslation.map(format).exists(_ != format(output))) {
          val expected = exampleQuery.expectedTranslation.getOrElse("")
          ReportEntryReport(
            parsed = 1,
            statements = 1,
            transpilation_error = Some(UnexpectedOutput(format(expected), format(output))))
        } else {
          ReportEntryReport(parsed = 1, transpiled = 1, statements = 1, transpiled_statements = 1)
        }
    }
  }
}

class IsTranspiledFromSnowflakeQueryRunner extends BaseQueryRunner(new SnowflakeToDatabricksTranspiler)

class IsTranspiledFromTSqlQueryRunner extends BaseQueryRunner(new TSqlToDatabricksTranspiler)
