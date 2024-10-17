package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.ExampleQuery
import com.databricks.labs.remorph.Result
import com.databricks.labs.remorph.WorkflowStage.PARSE
import com.databricks.labs.remorph.intermediate.UnexpectedOutput
import com.databricks.labs.remorph.transpilers._

trait QueryRunner extends Formatter {
  def runQuery(exampleQuery: ExampleQuery): ReportEntryReport

}

abstract class BaseQueryRunner(transpiler: Transpiler) extends QueryRunner {

  override def runQuery(exampleQuery: ExampleQuery): ReportEntryReport = {
    transpiler.transpile(SourceCode(exampleQuery.query)) match {
      case Result.Failure(PARSE, error) => ReportEntryReport(statements = 1, parsing_error = Some(error))
      case Result.Failure(_, error) =>
        // If we got past the PARSE stage, then remember to record that we parsed it correctly
        ReportEntryReport(parsed = 1, statements = 1, transpilation_error = Some(error))
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
