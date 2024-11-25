package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.{CommentBasedQueryExtractor, NestedFiles, WholeFileQueryExtractor}

import java.time.Instant

import io.circe.generic.auto._
import io.circe.syntax._

case class DialectCoverageTest(dialectName: String, queryRunner: QueryRunner)

case class IndividualError(description: String, nbOccurrences: Int, example: String)

case class ErrorsSummary(parseErrors: Seq[IndividualError], transpileErrors: Seq[IndividualError])

class CoverageTest extends ErrorEncoders {

  private val dialectCoverageTests = Seq(
    DialectCoverageTest("snowflake", new IsTranspiledFromSnowflakeQueryRunner),
    DialectCoverageTest("tsql", new IsTranspiledFromTSqlQueryRunner))

  private def getCurrentCommitHash: Option[String] = {
    val gitRevParse = os.proc("/usr/bin/git", "rev-parse", "--short", "HEAD").call(os.pwd)
    if (gitRevParse.exitCode == 0) {
      Some(gitRevParse.out.trim())
    } else {
      None
    }
  }

  private def timeToEpochNanos(instant: Instant) = {
    val epoch = Instant.ofEpochMilli(0)
    java.time.Duration.between(epoch, instant).toNanos
  }
  def run(sourceDir: os.Path, outputPath: os.Path, extractor: String): Unit = {

    val now = Instant.now

    val project = "remorph-core"
    val commitHash = getCurrentCommitHash

    val outputFilePath = outputPath / s"$project-coverage-${timeToEpochNanos(now)}.json"

    os.makeDir.all(outputPath)

    val reportsByDialect: Seq[(String, Seq[ReportEntry])] = dialectCoverageTests.map { t =>
      val queryExtractor = extractor match {
        case "comment" => new CommentBasedQueryExtractor(t.dialectName, "databricks")
        case "full" => new WholeFileQueryExtractor
      }

      t.dialectName -> new NestedFiles((sourceDir / t.dialectName).toNIO).listTests.flatMap { test =>
        queryExtractor
          .extractQuery(test.inputFile)
          .map { exampleQuery =>
            val runner = t.queryRunner
            val header = ReportEntryHeader(
              project = project,
              commit_hash = commitHash,
              version = "latest",
              timestamp = now.toString,
              source_dialect = t.dialectName,
              target_dialect = "databricks",
              file = os.Path(test.inputFile).relativeTo(sourceDir).toString)
            val report = runner.runQuery(exampleQuery)
            ReportEntry(header, report)
          }
          .toSeq

      }
    }

    reportsByDialect.foreach { case (dialect, reports) =>
      reports.foreach(report => os.write.append(outputFilePath, report.asJson.noSpaces + "\n"))
      val total = reports.size
      val parsed = reports.map(_.report.parsed).sum
      val transpiled = reports.map(_.report.transpiled).sum
      // scalastyle:off
      println(
        s"remorph -> $dialect: ${100d * parsed / total}% parsed ($parsed / $total)," +
          s" ${100d * transpiled / total}% transpiled ($transpiled / $total)")
    // scalastyle:on
    }

  }
}
