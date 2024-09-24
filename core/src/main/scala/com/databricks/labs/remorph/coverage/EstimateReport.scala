package com.databricks.labs.remorph.coverage

import upickle.default._

sealed trait SqlComplexity
object SqlComplexity {
  case object LOW extends SqlComplexity
  case object MEDIUM extends SqlComplexity
  case object COMPLEX extends SqlComplexity
  case object VERY_COMPLEX extends SqlComplexity

  implicit val rw: ReadWriter[SqlComplexity] = ReadWriter.merge(
    macroRW[SqlComplexity.LOW.type],
    macroRW[SqlComplexity.MEDIUM.type],
    macroRW[SqlComplexity.COMPLEX.type],
    macroRW[SqlComplexity.VERY_COMPLEX.type])
}

@upickle.implicits.serializeDefaults(true)
case class EstimateReport(
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
case class EstimateAnalysisReport(complexity: SqlComplexity = SqlComplexity.LOW)

object EstimateAnalysisReport {
  implicit val rw: ReadWriter[EstimateAnalysisReport] = macroRW
}
