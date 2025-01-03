package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{EstimationStatistics, RuleScore, SqlComplexity}
import com.databricks.labs.remorph.discovery.Fingerprint
import com.databricks.labs.remorph.intermediate.RemorphError

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

case class EstimationReportRecord(
    transpilationReport: EstimationTranspilationReport,
    analysisReport: EstimationAnalysisReport) {
  def withQueries(newQuery: String, output: Option[String]): EstimationReportRecord = {
    this.copy(transpilationReport = transpilationReport.withQueries(newQuery, output))
  }
}

case class EstimationTranspilationReport(
    query: Option[String] = None,
    output: Option[String] = None,
    parsed: Int = 0, // 1 for success, 0 for failure
    statements: Int = 0, // number of statements parsed
    parsing_error: Option[RemorphError] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[RemorphError] = None) {

  def withQueries(newQuery: String, output: Option[String]): EstimationTranspilationReport = {
    this.copy(query = Some(newQuery), output = output)
  }
}

case class EstimationAnalysisReport(
    fingerprint: Option[Fingerprint] = None,
    complexity: SqlComplexity = SqlComplexity.LOW,
    score: RuleScore)
