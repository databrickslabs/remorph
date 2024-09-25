package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.discovery.Fingerprint
import com.databricks.labs.remorph.coverage.estimation.SqlComplexity
import upickle.default.{ReadWriter, macroRW}

@upickle.implicits.serializeDefaults(true)
case class EstimateReport(
    dialect: String, // What dialect of SQL is this a report for?
    sampleSize: Int, // How many records were used to estimate
    uniqueSuccesses: Int, // How many unique queries were successfully estimated
    parseFailures: Int,
    transpileFailures: Int,
    records: Seq[EstimateReportRecord], // The actual records - includes failures
    overallComplexity: SqlComplexity = SqlComplexity.LOW)

object EstimateReport {
  implicit val rw: ReadWriter[EstimateReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimateReportRecord(
    transpilationReport: EstimateTranspilationReport,
    analysisReport: EstimateAnalysisReport)

object EstimateReportRecord {
  implicit val rw: ReadWriter[EstimateReportRecord] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimateTranspilationReport(
    query: Option[String] = None,
    parsed: Int = 0, // 1 for success, 0 for failure
    statements: Int = 0, // number of statements parsed
    parsing_error: Option[String] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[String] = None)

object EstimateTranspilationReport {
  implicit val rw: ReadWriter[EstimateTranspilationReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimateAnalysisReport(
    fingerprint: Option[Fingerprint] = None,
    complexity: SqlComplexity = SqlComplexity.LOW)

object EstimateAnalysisReport {
  implicit val rw: ReadWriter[EstimateAnalysisReport] = macroRW
}
