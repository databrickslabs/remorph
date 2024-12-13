package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.queries.{AcceptanceTest, ExampleSource, QueryExtractor}

case class AcceptanceTestConfig(
    testFileSource: ExampleSource,
    queryExtractor: QueryExtractor,
    queryRunner: QueryRunner,
    ignoredTestNames: String => Boolean = Set.empty,
    shouldFailParse: String => Boolean = Set.empty)

class AcceptanceTestRunner(config: AcceptanceTestConfig) {

  def shouldFailParse: String => Boolean = config.shouldFailParse

  def runAcceptanceTest(acceptanceTest: AcceptanceTest): Option[ReportEntryReport] = {
    if (config.ignoredTestNames(acceptanceTest.testName)) {
      None
    } else {
      config.queryExtractor.extractQuery(acceptanceTest.inputFile).map(config.queryRunner.runQuery)
    }
  }

  def foreachTest(f: AcceptanceTest => Unit): Unit = config.testFileSource.listTests.foreach(f)
}
