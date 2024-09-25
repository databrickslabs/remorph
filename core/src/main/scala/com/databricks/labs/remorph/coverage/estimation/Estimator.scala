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

  def run(): EstimateReport = {
    val history = queryHistory.history()
    val anonymizer = new Anonymizer(planParser)
    val parsedSet = scala.collection.mutable.Set[String]()

    val reportEntries = history.queries.flatMap(processQuery(_, anonymizer, parsedSet))

    val (uniqueSuccesses, parseFailures, transpileFailures) = countReportEntries(reportEntries)

    EstimateReport(
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
      parsedSet: scala.collection.mutable.Set[String]): Option[EstimateReportRecord] = {
    planParser.parse(SourceCode(query.source, query.user + "_" + query.id)).flatMap(planParser.visit) match {
      case Failure(PARSE, errorJson) =>
        Some(
          EstimateReportRecord(
            EstimateTranspilationReport(Some(query.source), statements = 1, parsing_error = Some(errorJson)),
            EstimateAnalysisReport()))

      case Failure(PLAN, errorJson) =>
        Some(
          EstimateReportRecord(
            EstimateTranspilationReport(Some(query.source), statements = 1, transpilation_error = Some(errorJson)),
            EstimateAnalysisReport()))

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
          EstimateReportRecord(
            EstimateTranspilationReport(
              query = Some(query.source),
              statements = 1,
              parsing_error = Some("Unexpected result from parse phase")),
            EstimateAnalysisReport()))
    }
  }

  private def generateReportRecord(
      query: ExecutedQuery,
      plan: LogicalPlan,
      anonymizer: Anonymizer): EstimateReportRecord = {
    val generator = new SqlGenerator
    planParser.optimize(plan).flatMap(generator.generate) match {
      case Failure(_, errorJson) =>
        EstimateReportRecord(
          EstimateTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some(errorJson)),
          EstimateAnalysisReport(fingerprint = Some(anonymizer(query, plan))))

      case Success(_: String) =>
        val statCount = analyzer.countStatements(plan)
        EstimateReportRecord(
          EstimateTranspilationReport(
            statements = statCount,
            transpiled = 1,
            transpiled_statements = statCount,
            parsed = 1),
          EstimateAnalysisReport(fingerprint = Some(anonymizer(query, plan))))

      case _ =>
        EstimateReportRecord(
          EstimateTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some("Unexpected result from transpilation")),
          EstimateAnalysisReport(fingerprint = Some(anonymizer(query, plan))))
    }
  }

  def countReportEntries(reportEntries: Seq[EstimateReportRecord]): (Int, Int, Int) = {
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
