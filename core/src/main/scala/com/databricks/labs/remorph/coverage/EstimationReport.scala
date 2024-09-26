package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{SqlComplexity, EstimationStatistics}
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
)

object EstimationReport {
  implicit val rw: ReadWriter[EstimationReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationReportRecord(
    transpilationReport: EstimationTranspilationReport,
    analysisReport: EstimationAnalysisReport)

object EstimationReportRecord {
  implicit val rw: ReadWriter[EstimationReportRecord] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationTranspilationReport(
    query: Option[String] = None,
    parsed: Int = 0, // 1 for success, 0 for failure
    statements: Int = 0, // number of statements parsed
    parsing_error: Option[String] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[String] = None)

object EstimationTranspilationReport {
  implicit val rw: ReadWriter[EstimationTranspilationReport] = macroRW
}

@upickle.implicits.serializeDefaults(true)
case class EstimationAnalysisReport(
    fingerprint: Option[Fingerprint] = None,
    complexity: SqlComplexity = SqlComplexity.LOW,
    score: Int = 10)

object EstimationAnalysisReport {
  implicit val rw: ReadWriter[EstimationAnalysisReport] = macroRW
}
