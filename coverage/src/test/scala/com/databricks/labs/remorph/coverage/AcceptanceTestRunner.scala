package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeAstBuilder
import com.databricks.labs.remorph.parsers.tsql.TSqlAstBuilder
import org.scalatest.flatspec.AnyFlatSpec

import java.nio.file.Paths

case class AcceptanceTestConfig(
    testFileSource: AcceptanceTestSource,
    queryExtractor: QueryExtractor,
    queryRunner: QueryRunner)

abstract class AcceptanceTestRunner(config: AcceptanceTestConfig) extends AnyFlatSpec {

  private def runAcceptanceTest(acceptanceTest: AcceptanceTest) = {
    val q = config.queryExtractor.extractQuery(acceptanceTest.inputFile)
    config.queryRunner.runQuery(q)
  }

  config.testFileSource.listTests.foreach { test =>
    registerTest(test.testName) {
      val report = runAcceptanceTest(test)
      if (report.isSuccess) {
        succeed
      } else {
        fail(report.errorMessage.getOrElse(""))
      }
    }
  }
}

class SnowflakeAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get(Option(System.getProperty("snowflake.test.resources.path"))
          .getOrElse("../tests/resources/functional/snowflake"))),
        new CommentBasedQueryExtractor("snowflake"),
        new IsResolvedAsSnowflakeQueryRunner(new SnowflakeAstBuilder)))

class TSqlAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get(Option(System.getProperty("tsql.test.resources.path"))
          .getOrElse("../tests/resources/functional/tsql"))),
        new CommentBasedQueryExtractor("tsql"),
        new IsResolvedAsTSqlQueryRunner(new TSqlAstBuilder)))
