package com.databricks.labs.remorph.coverage
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeAstBuilder
import mainargs._

import java.time.Instant

object Main {

  implicit object PathRead extends TokensReader.Simple[os.Path] {
    def shortName: String = "path"
    def read(strs: Seq[String]): Either[String, os.Path] = Right(os.Path(strs.head, os.pwd))
  }

  @main
  def run(
      @arg(short = 'i', doc = "Source path of test queries")
      sourceDir: os.Path,
      @arg(short = 'o', doc = "Report output path")
      outputPath: os.Path,
      @arg(short = 's', doc = "Start comment")
      startComment: Option[String],
      @arg(short = 'e', doc = "End comment")
      endComment: Option[String],
      @arg(short = 'd', doc = "Source dialect")
      sourceDialect: Option[String],
      @arg(short = 't', doc = "Target dialect")
      targetDialect: Option[String]): Unit = {
    val testSource = new NestedFiles(sourceDir.toNIO)
    val CommentBasedQueryExtractor = new CommentBasedQueryExtractor(
      startComment.getOrElse("-- snowflake sql:"),
      endComment.getOrElse("-- databricks sql:"))
    testSource.listTests.foreach { test =>
      val q = CommentBasedQueryExtractor.extractQuery(test.inputFile)
      val runner = new IsResolvedAsSnowflakeQueryRunner(new SnowflakeAstBuilder)
      val header = ReportEntryHeader(
        project = "remorph-core",
        commit_hash = None,
        version = "latest",
        timestamp = Instant.now.toString,
        source_dialect = sourceDialect.getOrElse("snowflake"),
        target_dialect = targetDialect.getOrElse("databricks"),
        file = test.inputFile.toString)
      val report = runner.runQuery(q)
      val reportEntryJson = ReportEntry(header, report).asJson
      os.write.append(outputPath, ujson.write(reportEntryJson, indent = -1) + "\n")
    }
  }

  def main(args: Array[String]): Unit = ParserForMethods(this).runOrExit(args)
}
