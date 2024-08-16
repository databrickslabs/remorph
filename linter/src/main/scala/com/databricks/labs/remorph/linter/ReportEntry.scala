package com.databricks.labs.remorph.linter

case class ReportEntryHeader(
    project: String,
    commit_hash: Option[String],
    version: String,
    timestamp: String,
    file: String)

case class ReportEntry(header: ReportEntryHeader, report: OrphanedRuleSummary) {

  def asJson: ujson.Value.Value = {
    ujson.Obj(
      "project" -> ujson.Str(header.project),
      "commit_hash" -> header.commit_hash.map(ujson.Str).getOrElse(ujson.Null),
      "version" -> ujson.Str(header.version),
      "timestamp" -> ujson.Str(header.timestamp),
      "file" -> ujson.Str(header.file),
      "orphans" -> report.toJSON)
  }
}
