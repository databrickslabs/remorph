package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.{AcceptanceTest, ExampleSource, CommentBasedQueryExtractor, NestedFiles, QueryExtractor}
import org.scalatest.flatspec.AnyFlatSpec

import java.nio.file.Paths

case class AcceptanceTestConfig(testFileSource: ExampleSource, queryExtractor: QueryExtractor, queryRunner: QueryRunner)

abstract class AcceptanceTestRunner(config: AcceptanceTestConfig) extends AnyFlatSpec {

  private def runAcceptanceTest(acceptanceTest: AcceptanceTest): Option[ReportEntryReport] = {
    config.queryExtractor.extractQuery(acceptanceTest.inputFile).map(config.queryRunner.runQuery)
  }

  config.testFileSource.listTests.foreach { test =>
    registerTest(test.testName) {
      runAcceptanceTest(test) match {
        case None => pending
        case Some(r) if r.isSuccess => succeed
        case Some(report) => fail(report.errorMessage.getOrElse(""))
      }
    }
  }
}

class SnowflakeAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get(Option(System.getProperty("snowflake.test.resources.path"))
          .getOrElse(s"${NestedFiles.projectRoot}/tests/resources/functional/snowflake"))),
        new CommentBasedQueryExtractor("snowflake", "databricks"),
        new IsTranspiledFromSnowflakeQueryRunner))

class TSqlAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get(Option(System.getProperty("tsql.test.resources.path"))
          .getOrElse(s"${NestedFiles.projectRoot}/tests/resources/functional/tsql"))),
        new CommentBasedQueryExtractor("tsql", "databricks"),
        new IsTranspiledFromTSqlQueryRunner))
