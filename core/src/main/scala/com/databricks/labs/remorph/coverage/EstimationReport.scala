package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{EstimationStatistics, RuleScore, SqlComplexity}
import com.databricks.labs.remorph.discovery.Fingerprint
import upickle.default.{ReadWriter, macroRW}

@upickle.implicits.serializeDefaults(true)
case class EstimationReport(
    overallComplexity: EstimationStatistics,
    dialect: String, // What dialect of SQL is this a report for?
    sampleSize: Int, // How many records were used to estimate
    uniqueSuccesses: Int, // How many unique queries were successfully estimated
    parseFailures: Int,
    transpileFailures: Int,
    records: Seq[EstimationReportRecord] // The actual records - includes failures
) {

  def withRecords(newRecords: Seq[EstimationReportRecord]): EstimationReport = {
    this.copy(records = newRecords)
  }
}

object EstimationReport {
  implicit val rw: ReadWriter[EstimationReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationReportRecord(
    transpilationReport: EstimationTranspilationReport,
    analysisReport: EstimationAnalysisReport) {
  def withQueries(newQuery: String, output: Option[String]): EstimationReportRecord = {
    this.copy(transpilationReport = transpilationReport.withQueries(newQuery, output))
  }
}

object EstimationReportRecord {
  implicit val rw: ReadWriter[EstimationReportRecord] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationTranspilationReport(
    query: Option[String] = None,
    output: Option[String] = None,
    parsed: Int = 0, // 1 for success, 0 for failure
    statements: Int = 0, // number of statements parsed
    parsing_error: Option[String] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[String] = None) {

  def withQueries(newQuery: String, output: Option[String]): EstimationTranspilationReport = {
    this.copy(query = Some(newQuery), output = output)
  }
}

object EstimationTranspilationReport {
  implicit val rw: ReadWriter[EstimationTranspilationReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationAnalysisReport(
    fingerprint: Option[Fingerprint] = None,
    complexity: SqlComplexity = SqlComplexity.LOW,
    score: RuleScore)

object EstimationAnalysisReport {
  implicit val rw: ReadWriter[EstimationAnalysisReport] = macroRW
}
