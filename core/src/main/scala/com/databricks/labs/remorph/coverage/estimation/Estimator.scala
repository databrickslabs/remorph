package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.connections.SnowflakeConnectionFactory
import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.coverage.{EstimateAnalysisReport, EstimateReport, EstimateReportRecord, EstimateTranspilationReport, SqlComplexity}
import com.databricks.labs.remorph.discovery.{Anonymizer, SnowflakeQueryHistory}
import com.databricks.labs.remorph.parsers.intermediate.{Literal, UnresolvedType}
import com.databricks.labs.remorph.parsers.{PlanParser, intermediate => ir}
import com.databricks.labs.remorph.transpilers.Result.{Failure, Success}
import com.databricks.labs.remorph.transpilers.WorkflowStage.{PARSE, PLAN}
import com.databricks.labs.remorph.transpilers.{SourceCode, SqlGenerator}
import com.typesafe.scalalogging.LazyLogging
import os.Path
import upickle.default._

import java.time.Instant

class Estimator extends LazyLogging {
  private val placeholder = Literal("?", UnresolvedType)

  def run(outputDir: Path, dialect: String, planParser: PlanParser[_], consoleReport: Boolean = true): Unit = {

    val env = new EnvGetter
    val now = Instant.now
    os.makeDir.all(outputDir)
    val resultPath = outputDir / s"${dialect}_${now.getEpochSecond}.json"

    val conn = dialect match {
      case "snowflake" =>
        val connFactory = new SnowflakeConnectionFactory(env)
        connFactory.newConnection()
      case _ => throw new IllegalArgumentException(s"Unsupported dialect: $dialect")
    }
    try {
      val snow = new SnowflakeQueryHistory(conn)
      val history = snow.history()

      val anonymizer = new Anonymizer(planParser)

      // We keep a set of fingerprints to track unique queries, so that we can report on the number of unique queries
      // and not skew results by counting the same query with slightly different parameters multiple times.
      var parsedSet: Set[String] = Set.empty

      // Note that empty system queries are pre-filtered by the issued SQL query
      val reportEntries = history.queries
        .collect { case query =>
          val result =
            planParser.parse(SourceCode(query.source, query.user + "_" + query.id)).flatMap(planParser.visit)

          result match {
            case Failure(PARSE, errorJson) =>
              EstimateReportRecord(
                EstimateTranspilationReport(Some(query.source), statements = 1, parsing_error = Some(errorJson)),
                EstimateAnalysisReport())

            case Failure(PLAN, errorJson) =>
              EstimateReportRecord(
                EstimateTranspilationReport(Some(query.source), statements = 1, transpilation_error = Some(errorJson)),
                EstimateAnalysisReport())

            case Success(plan) =>
              val erasedLiterals = plan transformAllExpressions { case _: Literal => placeholder }
              val fingerprint = anonymizer.apply(query, erasedLiterals)
              if (!parsedSet.contains(fingerprint.fingerprint)) {
                parsedSet += fingerprint.fingerprint

                val generator = new SqlGenerator
                val genResult = planParser.optimize(plan).flatMap(generator.generate)

                genResult match {
                  case Failure(_, errorJson) =>
                    EstimateReportRecord(
                      EstimateTranspilationReport(
                        query = Some(query.source),
                        statements = 1,
                        parsed = 1,
                        transpilation_error = Some(errorJson)),
                      EstimateAnalysisReport(fingerprint = Some(fingerprint)))

                  case Success(_: String) =>
                    val statCount = countStatements(plan)
                    EstimateReportRecord(
                      EstimateTranspilationReport(
                        statements = statCount,
                        transpiled = 1,
                        transpiled_statements = statCount,
                        parsed = 1),
                      EstimateAnalysisReport(fingerprint = Some(fingerprint)))

                  case _ =>
                    EstimateReportRecord(
                      EstimateTranspilationReport(
                        query = Some(query.source),
                        statements = 1,
                        parsed = 1,
                        transpilation_error = Some("Unexpected result from transpilation")),
                      EstimateAnalysisReport(Some(fingerprint)))
                }
              } else {
                // Empty report will be filtered out as it means it was a duplicate
                EstimateReportRecord(EstimateTranspilationReport(), EstimateAnalysisReport())
              }
            case _ =>
              EstimateReportRecord(
                EstimateTranspilationReport(
                  query = Some(query.source),
                  statements = 1,
                  parsing_error = Some("Unexpected result from parse phase")),
                EstimateAnalysisReport())
          }
        }
        .filter(_.transpilationReport.statements > 0)

      val (uniqueSuccesses, parseFailures, transpileFailures) = reportEntries.foldLeft((0, 0, 0)) {
        case ((uniqueSuccesses, parseFailures, transpileFailures), entry) =>
          val newUniqueSuccesses =
            if (entry.transpilationReport.parsed == 1 && entry.transpilationReport.transpiled == 1) uniqueSuccesses + 1
            else uniqueSuccesses
          val newParseFailures =
            if (entry.transpilationReport.parsing_error.isDefined) parseFailures + 1 else parseFailures
          val newTranspileFailures =
            if (entry.transpilationReport.transpilation_error.isDefined) transpileFailures + 1 else transpileFailures
          (newUniqueSuccesses, newParseFailures, newTranspileFailures)
      }

      val report = EstimateReport(
        sampleSize = history.queries.size,
        uniqueSuccesses = uniqueSuccesses,
        parseFailures = parseFailures,
        transpileFailures = transpileFailures,
        records = reportEntries,
        overallComplexity = SqlComplexity.LOW // Will calculate this later
      )

      val jsonReport: String = write(report, indent = 4)
      os.write(resultPath, jsonReport)

      if (consoleReport) {
        // scalastyle:off println
        println(s"Sample size        : ${history.queries.size}")
        println(s"Unique successes   : $uniqueSuccesses")
        println(s"Parse failures     : $parseFailures")
        println(s"Transpile failures : $transpileFailures")
        println(s"Parsed query count : ${report.uniqueSuccesses}")
        println(s"Overall complexity : ${report.overallComplexity}")
        println(s"Report written to  : $resultPath")
        println()
        // scalastyle:on println
      }
    } finally {
      conn.close()
    }
  }

  // TODO: Probably needs to go into a plan analyzer class, along with SqlComplexity
  private def countStatements(plan: ir.TreeNode[_]): Int = {
    try {
      plan
        .collect {
          case b: ir.Batch if b.output != null =>
            b.output.size
          case b: ir.Batch =>
            logger.warn(s"Unexpected batch with no children: $b")
            0
          case _: ir.ScalarSubquery =>
            1
          case _ => 0
        }
        .sum
        .max(1)
    } catch {
      case e: Exception =>
        // Some of our IR does not seem to be fully formed and does not traverse correctly, throwing
        // an NPEs or Unsupported operation in the process.
        // We catch this here and return 1 as a fallback, but we will need to investigate
        // these and fix them either in the next PR which implements complexity analysis or in a separate PR
        // that just fixes IR generation. (Or I could be using this incorrectly somehow)
        logger.warn(s"Error counting statements: $e")
        1
    }
  }
}
