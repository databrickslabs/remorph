package com.databricks.labs.remorph.coverage

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
    parsing_error: Option[String] = None,
    transpiled: Int = 0, // 1 for success, 0 for failure
    transpiled_statements: Int = 0, // number of statements transpiled
    transpilation_error: Option[String] = None) {
  def isSuccess: Boolean = parsing_error.isEmpty && transpilation_error.isEmpty
  def errorMessage: Option[String] = parsing_error.orElse(transpilation_error)
}

case class ReportEntry(header: ReportEntryHeader, report: ReportEntryReport) {

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
      "parsing_error" -> report.parsing_error.map(ujson.Str).getOrElse(ujson.Null),
      "transpiled" -> ujson.Num(report.transpiled),
      "transpiled_statements" -> ujson.Num(report.transpiled_statements),
      "transpilation_error" -> report.transpilation_error.map(ujson.Str).getOrElse(ujson.Null))
  }
}
