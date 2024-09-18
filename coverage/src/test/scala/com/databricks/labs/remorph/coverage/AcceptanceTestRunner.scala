package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.{AcceptanceTest, ExampleSource, CommentBasedQueryExtractor, NestedFiles, QueryExtractor}
import org.scalatest.flatspec.AnyFlatSpec

import java.nio.file.Paths

case class AcceptanceTestConfig(
    testFileSource: ExampleSource,
    queryExtractor: QueryExtractor,
    queryRunner: QueryRunner,
    ignoredTestNames: Set[String] = Set.empty)

abstract class AcceptanceTestRunner(config: AcceptanceTestConfig) extends AnyFlatSpec {

  private def runAcceptanceTest(acceptanceTest: AcceptanceTest): Option[ReportEntryReport] = {
    if (config.ignoredTestNames.contains(acceptanceTest.testName)) {
      None
    } else {
      config.queryExtractor.extractQuery(acceptanceTest.inputFile).map(config.queryRunner.runQuery)
    }
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
        new IsTranspiledFromSnowflakeQueryRunner,
        ignoredTestNames = Set(
          "aggregates/listagg/test_listagg_4.sql",
          "cast/test_typecasts.sql",
          "ddl/lateral_struct/test_lateral_struct_2.sql",
          "ddl/lateral_struct/test_lateral_struct_3.sql",
          "ddl/lateral_struct/test_lateral_struct_5.sql",
          "ddl/lateral_struct/test_lateral_struct_9.sql",
          "ddl/lateral_struct/test_lateral_struct_10.sql",
          "ddl/lateral_struct/test_lateral_struct_12.sql",
          "sqlglot-incorrect/test_uuid_string_2.sql",
          "test_command/test_command_2.sql",
          "test_command/test_command_3.sql",
          "test_skip_unsupported_operations/test_skip_unsupported_operations_7.sql",
          "test_skip_unsupported_operations/test_skip_unsupported_operations_9.sql",
          "test_skip_unsupported_operations/test_skip_unsupported_operations_10.sql",
          "test_skip_unsupported_operations/test_skip_unsupported_operations_11.sql")))

class TSqlAcceptanceSuite
    extends AcceptanceTestRunner(
      AcceptanceTestConfig(
        new NestedFiles(Paths.get(Option(System.getProperty("tsql.test.resources.path"))
          .getOrElse(s"${NestedFiles.projectRoot}/tests/resources/functional/tsql"))),
        new CommentBasedQueryExtractor("tsql", "databricks"),
        new IsTranspiledFromTSqlQueryRunner,
        ignoredTestNames = Set(
          "functions/test_aadbts_1.sql",
          "functions/test_aalangid1.sql",
          "functions/test_aalanguage_1.sql",
          "functions/test_aalock_timeout_1.sql",
          "functions/test_aamax_connections_1.sql",
          "functions/test_aamax_precision_1.sql",
          "functions/test_aaoptions_1.sql",
          "functions/test_aaremserver_1.sql",
          "functions/test_aaservername_1.sql",
          "functions/test_aaservicename_1.sql",
          "functions/test_aaspid_1.sql",
          "functions/test_aatextsize_1.sql",
          "functions/test_aaversion_1.sql",
          "functions/test_approx_count_distinct.sql",
          "functions/test_approx_percentile_cont_1.sql",
          "functions/test_approx_percentile_disc_1.sql",
          "functions/test_collationproperty_1.sql",
          "functions/test_grouping_1.sql",
          "functions/test_nestlevel_1.sql",
          "functions/test_percent_rank_1.sql",
          "functions/test_percentile_cont_1.sql",
          "functions/test_percentile_disc_1.sql",
          "select/test_cte_xml.sql")))
