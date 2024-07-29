package com.databricks.labs.remorph.coverage
import mainargs._

import java.time.Instant

object Main {

  implicit object PathRead extends TokensReader.Simple[os.Path] {
    def shortName: String = "path"
    def read(strs: Seq[String]): Either[String, os.Path] = Right(os.Path(strs.head, os.pwd))
  }

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
  @main
  def run(
      @arg(short = 'i', doc = "Source path of test queries")
      sourceDir: os.Path,
      @arg(short = 'o', doc = "Report output path")
      outputPath: os.Path,
      @arg(short = 'x', doc = "Query extractor")
      extractor: String,
      @arg(short = 's', doc = "Start comment")
      startComment: Option[String],
      @arg(short = 'e', doc = "End comment")
      endComment: Option[String],
      @arg(short = 'd', doc = "Source dialect")
      sourceDialect: String,
      @arg(short = 't', doc = "Target dialect")
      targetDialect: String = "databricks"): Unit = {

    val now = Instant.now

    val project = "remorph-core"
    val commitHash = getCurrentCommitHash
    val testSource = new NestedFiles(sourceDir.toNIO)
    val queryExtractor = extractor match {
      case "comment" => new DialectNameCommentBasedQueryExtractor(sourceDialect, targetDialect)
      case "full" => new WholeFileQueryExtractor
    }
    val queryRunner = sourceDialect match {
      case "Snow" => new IsTranspiledFromSnowflakeQueryRunner
      case "Tsql" => new IsTranspiledFromTSqlQueryRunner
    }

    val outputFilePath = outputPath / s"$project-$sourceDialect-$targetDialect-${timeToEpochNanos(now)}.json"

    os.makeDir.all(outputPath)

    testSource.listTests.foreach { test =>
      queryExtractor.extractQuery(test.inputFile).foreach { exampleQuery =>
        val runner = queryRunner
        val header = ReportEntryHeader(
          project = project,
          commit_hash = commitHash,
          version = "latest",
          timestamp = now.toString,
          source_dialect = sourceDialect,
          target_dialect = targetDialect,
          file = os.Path(test.inputFile).relativeTo(sourceDir).toString)
        val report = runner.runQuery(exampleQuery)
        val reportEntryJson = ReportEntry(header, report).asJson
        os.write.append(outputFilePath, ujson.write(reportEntryJson, indent = -1) + "\n")
      }
    }
    // scalastyle:off
    println(s"Successfully produced coverage report in $outputFilePath")
    // scalastyle:on
  }

  def main(args: Array[String]): Unit = ParserForMethods(this).runOrExit(args)
}
