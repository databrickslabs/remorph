package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage._
import com.databricks.labs.remorph.discovery.{Anonymizer, ExecutedQuery, QueryHistoryProvider}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.parsers.intermediate.LogicalPlan
import com.databricks.labs.remorph.transpilers.Result.{Failure, Success}
import com.databricks.labs.remorph.transpilers.WorkflowStage.{PARSE, PLAN}
import com.databricks.labs.remorph.transpilers.{SourceCode, SqlGenerator}
import com.typesafe.scalalogging.LazyLogging

class Estimator(queryHistory: QueryHistoryProvider, planParser: PlanParser[_], analyzer: EstimationAnalyzer)
    extends LazyLogging {

  def run(): EstimationReport = {
    val history = queryHistory.history()
    val anonymizer = new Anonymizer(planParser)
    val parsedSet = scala.collection.mutable.Set[String]()

    val reportEntries = history.queries.flatMap(processQuery(_, anonymizer, parsedSet))

    val (uniqueSuccesses, parseFailures, transpileFailures) = countReportEntries(reportEntries)

    EstimationReport(
      dialect = planParser.dialect,
      sampleSize = history.queries.size,
      uniqueSuccesses = uniqueSuccesses,
      parseFailures = parseFailures,
      transpileFailures = transpileFailures,
      records = reportEntries,
      overallComplexity = SqlComplexity.LOW // Will calculate this later
    )
  }

  private def processQuery(
      query: ExecutedQuery,
      anonymizer: Anonymizer,
      parsedSet: scala.collection.mutable.Set[String]): Option[EstimationReportRecord] = {
    planParser.parse(SourceCode(query.source, query.user + "_" + query.id)).flatMap(planParser.visit) match {
      case Failure(PARSE, errorJson) =>
        Some(
          EstimationReportRecord(
            EstimationTranspilationReport(Some(query.source), statements = 1, parsing_error = Some(errorJson)),
            EstimationAnalysisReport()))

      case Failure(PLAN, errorJson) =>
        Some(
          EstimationReportRecord(
            EstimationTranspilationReport(Some(query.source), statements = 1, transpilation_error = Some(errorJson)),
            EstimationAnalysisReport()))

      case Success(plan) =>
        val queryHash = anonymizer(plan)
        if (!parsedSet.contains(queryHash)) {
          parsedSet += queryHash
          Some(generateReportRecord(query, plan, anonymizer))
        } else {
          None
        }

      case _ =>
        Some(
          EstimationReportRecord(
            EstimationTranspilationReport(
              query = Some(query.source),
              statements = 1,
              parsing_error = Some("Unexpected result from parse phase")),
            EstimationAnalysisReport()))
    }
  }

  private def generateReportRecord(
      query: ExecutedQuery,
      plan: LogicalPlan,
      anonymizer: Anonymizer): EstimationReportRecord = {
    val generator = new SqlGenerator
    planParser.optimize(plan).flatMap(generator.generate) match {
      case Failure(_, errorJson) =>
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some(errorJson)),
          EstimationAnalysisReport(fingerprint = Some(anonymizer(query, plan))))

      case Success(_: String) =>
        val statCount = analyzer.countStatements(plan)
        EstimationReportRecord(
          EstimationTranspilationReport(
            statements = statCount,
            transpiled = 1,
            transpiled_statements = statCount,
            parsed = 1),
          EstimationAnalysisReport(fingerprint = Some(anonymizer(query, plan))))

      case _ =>
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some("Unexpected result from transpilation")),
          EstimationAnalysisReport(fingerprint = Some(anonymizer(query, plan))))
    }
  }

  def countReportEntries(reportEntries: Seq[EstimationReportRecord]): (Int, Int, Int) = {
    reportEntries.foldLeft((0, 0, 0)) { case ((uniqueSuccesses, parseFailures, transpileFailures), entry) =>
      val newUniqueSuccesses =
        if (entry.transpilationReport.parsed == 1 && entry.transpilationReport.transpiled == 1) uniqueSuccesses + 1
        else uniqueSuccesses
      val newParseFailures =
        if (entry.transpilationReport.parsing_error.isDefined) parseFailures + 1 else parseFailures
      val newTranspileFailures =
        if (entry.transpilationReport.transpilation_error.isDefined) transpileFailures + 1 else transpileFailures
      (newUniqueSuccesses, newParseFailures, newTranspileFailures)
    }
  }
}
