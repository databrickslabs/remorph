package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.{CommentBasedQueryExtractor, NestedFiles, WholeFileQueryExtractor}

import java.time.Instant

class CoverageTest {

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
  def run(sourceDir: os.Path, outputPath: os.Path, extractor: String, dialect: String): Unit = {

    val now = Instant.now

    val dialectFullName = dialect match {
      case "Snow" => "snowflake"
      case "Tsql" => "tsql"
    }
    val project = "remorph-core"
    val commitHash = getCurrentCommitHash
    val testSource = new NestedFiles(sourceDir.toNIO)
    val queryExtractor = extractor match {
      case "comment" => new CommentBasedQueryExtractor(dialectFullName, "databricks")
      case "full" => new WholeFileQueryExtractor
    }
    val queryRunner = dialect match {
      case "Snow" => new IsTranspiledFromSnowflakeQueryRunner
      case "Tsql" => new IsTranspiledFromTSqlQueryRunner
    }

    val outputFilePath = outputPath / s"$project-$dialect-databricks-${timeToEpochNanos(now)}.json"

    os.makeDir.all(outputPath)

    testSource.listTests.foreach { test =>
      queryExtractor.extractQuery(test.inputFile).foreach { exampleQuery =>
        val runner = queryRunner
        val header = ReportEntryHeader(
          project = project,
          commit_hash = commitHash,
          version = "latest",
          timestamp = now.toString,
          source_dialect = dialect,
          target_dialect = "databricks",
          file = os.Path(test.inputFile).relativeTo(sourceDir).toString)
        val report = runner.runQuery(exampleQuery)
        val reportEntryJson = ReportEntry(header, report).asJson
        os.write.append(outputFilePath, ujson.write(reportEntryJson, indent = -1) + "\n")
      }
    }
  }
}
