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
      overallComplexity = analyzer.summarizeComplexity(reportEntries))
  }

  // TODO: Remove hard coding of scores and record all scoring reports

  private def processQuery(
      query: ExecutedQuery,
      anonymizer: Anonymizer,
      parsedSet: scala.collection.mutable.Set[String]): Option[EstimationReportRecord] = {
    planParser.parse(SourceCode(query.source, query.user + "_" + query.id)).flatMap(planParser.visit) match {
      case Failure(PARSE, errorJson) =>
        Some(
          EstimationReportRecord(
            EstimationTranspilationReport(Some(query.source), statements = 1, parsing_error = Some(errorJson)),
            EstimationAnalysisReport(score = 1000, complexity = SqlComplexity.VERY_COMPLEX)))

      case Failure(PLAN, errorJson) =>
        Some(
          EstimationReportRecord(
            EstimationTranspilationReport(Some(query.source), statements = 1, transpilation_error = Some(errorJson)),
            EstimationAnalysisReport(score = 1000, complexity = SqlComplexity.VERY_COMPLEX)))

      case Success(plan) =>
        val queryHash = anonymizer(plan)
        // scalastyle:off println
        println(s"Query: ${query.source}")
        val sourceTextComplexity = analyzer.sourceTextComplexity(query.source)
        val score = analyzer.evaluateTree(plan) + analyzer.countStatements(
          plan) + sourceTextComplexity.textLength + sourceTextComplexity.lineCount
        // scalastyle:on println
        if (!parsedSet.contains(queryHash)) {
          parsedSet += queryHash
          Some(generateReportRecord(query, plan, score, anonymizer))
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
            EstimationAnalysisReport(score = 1000, complexity = SqlComplexity.VERY_COMPLEX)))
    }
  }

  private def generateReportRecord(
      query: ExecutedQuery,
      plan: LogicalPlan,
      score: Int,
      anonymizer: Anonymizer): EstimationReportRecord = {
    val generator = new SqlGenerator
    planParser.optimize(plan).flatMap(generator.generate) match {
      case Failure(_, errorJson) =>
        // Failure to transpile means that we need to increase the score as it will take some
        // time to manually investigate and fix the issue
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some(errorJson)),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            score = score + 100,
            complexity = SqlComplexity.fromScore(score)))

      case Success(_: String) =>
        // A successful transpilation means that we can reduce the score because the query seems
        // to be successfully translated. However, that does not mean that it scores 0 because there
        // will be some effort required to verify the translation.
        val newScore = math.max(score * 0.1, 5).toInt
        val statCount = analyzer.countStatements(plan)
        EstimationReportRecord(
          EstimationTranspilationReport(
            statements = statCount,
            transpiled = 1,
            transpiled_statements = statCount,
            parsed = 1),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            SqlComplexity.fromScore(newScore),
            newScore))

      case _ =>
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some("Unexpected result from transpilation")),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            score = 1000,
            complexity = SqlComplexity.VERY_COMPLEX))
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
