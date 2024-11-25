package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.intermediate.{MultipleErrors, ParsingError, RemorphError}
import io.circe.Encoder

case class ReportEntryHeader(
    project: String,
    commit_hash: Option[String],
    version: String,
    timestamp: String,
    source_dialect: String,
    target_dialect: String,
    file: String)
case class ReportEntryReport(
    parsed: Int = 0, // 1 for success, 0 for failure
    statements: Int = 0, // number of statements parsed
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    failures: Option[RemorphError] = None) {
  def isSuccess: Boolean = failures.isEmpty
  def failedParseOnly: Boolean = failures.forall {
    case _: ParsingError => true
    case m: MultipleErrors => m.errors.forall(_.isInstanceOf[ParsingError])
    case _ => true
  }

  // Transpilation error takes precedence over parsing error as parsing errors will be
  // shown in the output. If there is a transpilation error, we should therefore show that instead.
  def errorMessage: Option[String] = failures.map(_.msg)
}

case class ReportEntry(header: ReportEntryHeader, report: ReportEntryReport)

object ReportEntry extends ErrorEncoders {
  import io.circe.generic.auto._
  import io.circe.syntax._
  implicit val reportEntryEncoder: Encoder[ReportEntry] = Encoder.instance { entry =>
    val header = entry.header.asJson
    val report = entry.report.asJson
    header.deepMerge(report)
  }
}
