package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import java.sql.Timestamp
import java.time.Duration

class AnonymizerTest extends AnyWordSpec with Matchers {
  "Anonymizer" should {
    "work in happy path" in {
      val snow = new SnowflakePlanParser
      val anonymizer = new Anonymizer(snow)
      val query = ExecutedQuery(
        new Timestamp(1725032011000L),
        "SELECT a, b FROM c WHERE d >= 300 AND e = 'foo'",
        Duration.ofMillis(300),
        "foo")

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          new Timestamp(1725032011000L),
          "4e1ebb6993509ec6bb977224ecec02fc9bb6f118",
          Duration.ofMillis(300),
          "foo",
          WorkloadType.SQL_SERVING,
          QueryType.DML))
    }

    "work in happy path with DDL" in {
      val snow = new SnowflakePlanParser
      val anonymizer = new Anonymizer(snow)
      val query =
        ExecutedQuery(
          new Timestamp(1725032011000L),
          "CREATE TABLE foo (a INT, b STRING)",
          Duration.ofMillis(300),
          "foo")

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          new Timestamp(1725032011000L),
          "828f7eb7d417310ab5c1673c96ec82c47f0231e4",
          Duration.ofMillis(300),
          "foo",
          WorkloadType.ETL,
          QueryType.DDL))
    }

    "unknown query" in {
      val snow = new SnowflakePlanParser
      val anonymizer = new Anonymizer(snow)
      val query = ExecutedQuery(new Timestamp(1725032011000L), "THIS IS UNKNOWN;", Duration.ofMillis(300), "foo")

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          new Timestamp(1725032011000L),
          // Changed hash value since query results in set of ir.UnresolvedCommand as part of otherCommand
          "3cb7865cbb724d921629971dbc0e971624a6c3e2",
          Duration.ofMillis(300),
          "foo",
          WorkloadType.OTHER,
          QueryType.OTHER))
    }
  }

  "Fingerprints" should {
    "work" in {
      val snow = new SnowflakePlanParser
      val anonymizer = new Anonymizer(snow)
      val history = QueryHistory(
        Seq(
          ExecutedQuery(
            new Timestamp(1725032011000L),
            "SELECT a, b FROM c WHERE d >= 300 AND e = 'foo'",
            Duration.ofMillis(300),
            "foo"),
          ExecutedQuery(
            new Timestamp(1725032011001L),
            "SELECT a, b FROM c WHERE d >= 931 AND e = 'bar'",
            Duration.ofMillis(300),
            "foo"),
          ExecutedQuery(
            new Timestamp(1725032011002L),
            "SELECT a, b FROM c WHERE d >= 234 AND e = 'something very different'",
            Duration.ofMillis(300),
            "foo")))

      val fingerprints = anonymizer.apply(history)
      fingerprints.uniqueQueries should equal(1)
    }
  }
}
