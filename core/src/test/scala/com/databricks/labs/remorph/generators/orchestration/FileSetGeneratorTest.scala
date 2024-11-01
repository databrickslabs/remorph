package com.databricks.labs.remorph.generators.orchestration

import com.databricks.labs.remorph.discovery.{ExecutedQuery, QueryHistory}
import com.databricks.labs.remorph.generators.orchestration.rules.history.RawMigration
import com.databricks.labs.remorph.parsers.snowflake.SnowflakePlanParser
import com.databricks.labs.remorph.transpilers.{PySparkGenerator, SqlGenerator}
import com.databricks.labs.remorph.{Init, KoResult, OkResult, PartialResult}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import java.sql.Timestamp
import java.time.Duration

class FileSetGeneratorTest extends AnyWordSpec with Matchers {
  private val parser = new SnowflakePlanParser()
  private val sqlGen = new SqlGenerator
  private val pyGen = new PySparkGenerator
  private val queryHistory = QueryHistory(
    Seq(
      ExecutedQuery(
        "query1",
        s"""INSERT INTO schema1.table1 SELECT col1, col2
           |FROM schema2.table2 AS t2 INNER JOIN schema1.table3 AS t3 ON t2.id = t3.id
           |""".stripMargin,
        new Timestamp(System.currentTimeMillis()),
        Duration.ofSeconds(30),
        Some("user1")),
      ExecutedQuery(
        "query3",
        "SELECT * FROM schema2.table3 AS t3 JOIN schema2.table4 AS t4 ON t3.id = t4.id",
        new Timestamp(System.currentTimeMillis()),
        Duration.ofSeconds(60),
        Some("user3"))))

  "FileSetGenerator" should {
    "work" in {
      new FileSetGenerator(parser, sqlGen, pyGen).generate(RawMigration(queryHistory)).run(Init) match {
        case OkResult((_, fileSet)) =>
          fileSet.getFile("notebooks/query1.sql").get shouldBe
            s"""INSERT INTO
               |  schema1.table1
               |SELECT
               |  col1,
               |  col2
               |FROM
               |  schema2.table2 AS t2
               |  INNER JOIN schema1.table3 AS t3 ON t2.id = t3.id;""".stripMargin
          fileSet.getFile("notebooks/query3.sql").get shouldBe
            s"""SELECT
               |  *
               |FROM
               |  schema2.table3 AS t3
               |  JOIN schema2.table4 AS t4 ON t3.id = t4.id;""".stripMargin
          fileSet.getFile("databricks.yml").get shouldBe
            s"""---
               |bundle:
               |  name: "remorphed"
               |targets:
               |  dev:
               |    mode: "development"
               |    default: true
               |  prod:
               |    mode: "production"
               |resources:
               |  jobs:
               |    migrated_via_remorph:
               |      name: "[$${bundle.target}] Migrated via Remorph"
               |      tags:
               |        generator: "remorph"
               |      tasks:
               |      - notebook_task:
               |          notebook_path: "notebooks/query1.sql"
               |          warehouse_id: "__DEFAULT_WAREHOUSE_ID__"
               |        task_key: "query1"
               |      - notebook_task:
               |          notebook_path: "notebooks/query3.sql"
               |          warehouse_id: "__DEFAULT_WAREHOUSE_ID__"
               |        task_key: "query3"
               |  schemas:
               |    schema2:
               |      catalog_name: "main"
               |      name: "schema2"
               |    schema1:
               |      catalog_name: "main"
               |      name: "schema1"
               |""".stripMargin
        case PartialResult(_, error) => fail(error.msg)
        case KoResult(_, error) => fail(error.msg)
      }
    }
  }
}
