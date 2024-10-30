package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.intermediate.{MultipleErrors, RemorphError, SingleError}

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
    parsing_error: Option[RemorphError] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[RemorphError] = None) {
  def isSuccess: Boolean = parsing_error.isEmpty && transpilation_error.isEmpty
  def failedParseOnly: Boolean = parsing_error.isDefined && transpilation_error.isEmpty

  // Transpilation error takes precedence over parsing error as parsing errors will be
  // shown in the output. If there is a transpilation error, we should therefore show that instead.
  def errorMessage: Option[String] = transpilation_error.orElse(parsing_error).map(_.msg)
}

case class ReportEntry(header: ReportEntryHeader, report: ReportEntryReport) {

  def singleErrorJson(error: SingleError): ujson.Value.Value =
    ujson.Obj("error_type" -> error.getClass.getSimpleName, "error_message" -> error.msg)

  def errorJson(errOpt: Option[RemorphError]): ujson.Value.Value = {
    errOpt
      .map {
        case s: SingleError => singleErrorJson(s)
        case m: MultipleErrors => ujson.Arr(m.errors.map(singleErrorJson))
      }
      .getOrElse(ujson.Null)
  }

  def asJson: ujson.Value.Value = {
    ujson.Obj(
      "project" -> ujson.Str(header.project),
      "commit_hash" -> header.commit_hash.map(ujson.Str).getOrElse(ujson.Null),
      "version" -> ujson.Str(header.version),
      "timestamp" -> ujson.Str(header.timestamp),
      "source_dialect" -> ujson.Str(header.source_dialect),
      "target_dialect" -> ujson.Str(header.target_dialect),
      "file" -> ujson.Str(header.file),
      "parsed" -> ujson.Num(report.parsed),
      "statements" -> ujson.Num(report.statements),
      "parsing_error" -> errorJson(report.parsing_error),
      "transpiled" -> ujson.Num(report.transpiled),
      "transpiled_statements" -> ujson.Num(report.transpiled_statements),
      "transpilation_error" -> errorJson(report.transpilation_error))
  }
}
