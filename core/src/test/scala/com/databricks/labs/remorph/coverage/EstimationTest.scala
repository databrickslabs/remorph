package com.databricks.labs.remorph.coverage

import com.databricks.labs.remorph.coverage.estimation.{EstimationAnalyzer, Estimator}
import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory, QueryHistoryProvider}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.mockito.Mockito._
import org.scalatestplus.mockito.MockitoSugar

import java.sql.Timestamp
import java.time.Duration

class EstimationTest extends AnyFlatSpec with Matchers with MockitoSugar {

  "Estimator" should "correctly process query history" in {
    // Mock dependencies
    val mockQueryHistoryProvider = mock[QueryHistoryProvider]

    // Real dependencies
    val planParser = new SnowflakePlanParser
    val analyzer = new EstimationAnalyzer

    // Mock query history
    val mockHistory = QueryHistory(
      Seq(
        ExecutedQuery(
          "id1",
          "SELECT * FROM table1",
          new Timestamp(1725032011000L),
          Duration.ofMillis(300),
          Some("user1")),
        ExecutedQuery(
          "id2",
          "SELECT * FROM table2",
          new Timestamp(1725032011000L),
          Duration.ofMillis(300),
          Some("user2"))))
    when(mockQueryHistoryProvider.history()).thenReturn(mockHistory)

    // Create Estimator instance
    val estimator = new Estimator(mockQueryHistoryProvider, planParser, analyzer)

    // Run the estimator
    val report = estimator.run()

    // Verify the results
    report.sampleSize should be(2)
    report.uniqueSuccesses should be(2)
    report.parseFailures should be(0)
    report.transpileFailures should be(0)
  }

  it should "handle parsing errors" in {
    // Mock dependencies
    val mockQueryHistoryProvider = mock[QueryHistoryProvider]

    // Real dependencies
    val planParser = new SnowflakePlanParser
    val analyzer = new EstimationAnalyzer

    // Mock query history
    val mockHistory = QueryHistory(
      Seq(
        ExecutedQuery(
          "id1",
          "SOME GARBAGE STATEMENT",
          new Timestamp(1725032011000L),
          Duration.ofMillis(300),
          Some("user1"))))
    when(mockQueryHistoryProvider.history()).thenReturn(mockHistory)

    // Create Estimator instance
    val estimator = new Estimator(mockQueryHistoryProvider, planParser, analyzer)

    // Run the estimator
    val report = estimator.run()

    // Verify the results
    report.sampleSize should be(1)
    report.uniqueSuccesses should be(0)
    report.parseFailures should be(1)
    report.transpileFailures should be(0)
  }

  // Add more test cases as needed
}
