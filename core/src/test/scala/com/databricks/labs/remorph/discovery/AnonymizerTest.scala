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
        "id",
        "SELECT a, b FROM c WHERE d >= 300 AND e = 'foo'",
        QuerySpec(new Timestamp(1725032011000L), Duration.ofMillis(300), Some("foo"), None))

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          "id",
          new Timestamp(1725032011000L),
          "b0b00569bfa1fe3975afc221a4a24630a0ab4ec9",
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
          "id",
          "CREATE TABLE foo (a INT, b STRING)",
          QuerySpec(new Timestamp(1725032011000L), Duration.ofMillis(300), Some("foo"), None))

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          "id",
          new Timestamp(1725032011000L),
          "828f7eb7d417310ab5c1673c96ec82c47f0231e4",
          Duration.ofMillis(300),
          "foo",
          WorkloadType.ETL,
          QueryType.DDL))
    }

    "trap an unknown query" in {
      val snow = new SnowflakePlanParser
      val anonymizer = new Anonymizer(snow)
      val query = ExecutedQuery(
        "id",
        "THIS IS UNKNOWN;",
        QuerySpec(new Timestamp(1725032011000L), Duration.ofMillis(300), Some("foo"), None))

      anonymizer.fingerprint(query) should equal(
        Fingerprint(
          "id",
          new Timestamp(1725032011000L),
          "93f60d8795c8bffa2aafe174ae8a867b42235755",
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
            "id",
            "SELECT a, b FROM c WHERE d >= 300 AND e = 'foo'",
            QuerySpec(new Timestamp(1725032011000L), Duration.ofMillis(300), Some("foo"), None)),
          ExecutedQuery(
            "id",
            "SELECT a, b FROM c WHERE d >= 931 AND e = 'bar'",
            QuerySpec(new Timestamp(1725032011001L), Duration.ofMillis(300), Some("foo"), None)),
          ExecutedQuery(
            "id",
            "SELECT a, b FROM c WHERE d >= 234 AND e = 'something very different'",
            QuerySpec(new Timestamp(1725032011002L), Duration.ofMillis(300), Some("foo"), None))))

      val fingerprints = anonymizer.apply(history)
      fingerprints.uniqueQueries should equal(1)
    }
  }
}
