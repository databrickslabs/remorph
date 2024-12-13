package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.WorkflowStage.{PARSE, PLAN}
import com.databricks.labs.remorph.coverage._
import com.databricks.labs.remorph.discovery.{Anonymizer, ExecutedQuery, QueryHistoryProvider}
import com.databricks.labs.remorph.intermediate.{LogicalPlan, ParsingError, TranspileFailure}
import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.{KoResult, OkResult, Optimizing, Parsing, TranspilerState}
import com.databricks.labs.remorph.transpilers.SqlGenerator
import com.typesafe.scalalogging.LazyLogging

class Estimator(queryHistory: QueryHistoryProvider, planParser: PlanParser[_], analyzer: EstimationAnalyzer)
    extends LazyLogging {

  def run(): EstimationReport = {
    val history = queryHistory.history()
    val anonymizer = new Anonymizer(planParser)
    // Hashes of either query strings or plans that we have seen before.
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

  private def processQuery(
      query: ExecutedQuery,
      anonymizer: Anonymizer,
      parsedSet: scala.collection.mutable.Set[String]): Option[EstimationReportRecord] = {

    val initialState = TranspilerState(Parsing(query.source))

    // Skip entries that have already been seen as text but for which we were unable to parse or
    // produce a plan for
    val fingerprint = anonymizer(query.source)
    if (!parsedSet.contains(fingerprint)) {
      parsedSet += fingerprint
      planParser.parse
        .flatMap(planParser.visit)
        .flatMap(plan => anonymizer(plan).map(hash => (hash, plan)))
        .runAndDiscardState(initialState) match {
        case KoResult(PARSE, error) =>
          Some(
            EstimationReportRecord(
              EstimationTranspilationReport(Some(query.source), statements = 1, parsing_error = Some(error)),
              EstimationAnalysisReport(
                score = RuleScore(ParseFailureRule(), Seq.empty),
                complexity = SqlComplexity.VERY_COMPLEX)))

        case KoResult(PLAN, error) =>
          Some(
            EstimationReportRecord(
              EstimationTranspilationReport(Some(query.source), statements = 1, transpilation_error = Some(error)),
              EstimationAnalysisReport(
                score = RuleScore(PlanFailureRule(), Seq.empty),
                complexity = SqlComplexity.VERY_COMPLEX)))

        case OkResult((queryHash, plan)) =>
          val score = analyzer.evaluateTree(plan)
          // Note that the plan hash will generally be more accurate than the query hash, hence we check here
          // as well as against the plain text
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
                parsing_error = Some(ParsingError(0, 0, "Unexpected result from parse phase", 0, "", "", ""))),
              EstimationAnalysisReport(
                score = RuleScore(UnexpectedResultRule(), Seq.empty),
                complexity = SqlComplexity.VERY_COMPLEX)))
      }
    } else {
      None
    }
  }

  private def generateReportRecord(
      query: ExecutedQuery,
      plan: LogicalPlan,
      ruleScore: RuleScore,
      anonymizer: Anonymizer): EstimationReportRecord = {
    val generator = new SqlGenerator
    val initialState = TranspilerState(Optimizing(plan, None))
    planParser.optimize(plan).flatMap(generator.generate).runAndDiscardState(initialState) match {
      case KoResult(_, error) =>
        // KoResult to transpile means that we need to increase the ruleScore as it will take some
        // time to manually investigate and fix the issue
        val tfr = RuleScore(TranspileFailureRule().plusScore(ruleScore.rule.score), Seq(ruleScore))
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error = Some(error)),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            score = tfr,
            complexity = SqlComplexity.fromScore(tfr.rule.score)))

      case OkResult(output) =>
        val newScore =
          RuleScore(SuccessfulTranspileRule().plusScore(ruleScore.rule.score), Seq(ruleScore))
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            output = Some(output),
            statements = 1,
            transpiled = 1,
            transpiled_statements = 1,
            parsed = 1),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            score = newScore,
            complexity = SqlComplexity.fromScore(newScore.rule.score)))

      case _ =>
        EstimationReportRecord(
          EstimationTranspilationReport(
            query = Some(query.source),
            statements = 1,
            parsed = 1,
            transpilation_error =
              Some(TranspileFailure(new RuntimeException("Unexpected result from transpile phase")))),
          EstimationAnalysisReport(
            fingerprint = Some(anonymizer(query, plan)),
            score = RuleScore(UnexpectedResultRule().plusScore(ruleScore.rule.score), Seq(ruleScore)),
            complexity = SqlComplexity.VERY_COMPLEX))
    }
  }

  private def countReportEntries(reportEntries: Seq[EstimationReportRecord]): (Int, Int, Int) = {
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
