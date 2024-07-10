package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.IRHelpers
import com.databricks.labs.remorph.parsers.intermediate._
import org.antlr.v4.runtime.tree.ParseTreeVisitor
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeDMLBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with IRHelpers {

  override protected def astBuilder = new SnowflakeDMLBuilder

  "SnowflakeDMLBuilder" should {
    "translate INSERT statements" in {
      example(
        "INSERT INTO foo SELECT * FROM bar LIMIT 100",
        _.insertStatement(),
        InsertIntoTable(
          namedTable("foo"),
          None,
          Project(Limit(namedTable("bar"), Literal(short = Some(100))), Seq(Star(None))),
          None,
          None,
          overwrite = false))

      example(
        "INSERT OVERWRITE INTO foo SELECT * FROM bar LIMIT 100",
        _.insertStatement(),
        InsertIntoTable(
          namedTable("foo"),
          None,
          Project(Limit(namedTable("bar"), Literal(short = Some(100))), Seq(Star(None))),
          None,
          None,
          overwrite = true))

      example(
        "INSERT INTO foo VALUES (1, 2, 3), (4, 5, 6)",
        _.insertStatement(),
        InsertIntoTable(
          namedTable("foo"),
          None,
          Values(
            Seq(
              Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3))),
              Seq(Literal(short = Some(4)), Literal(short = Some(5)), Literal(short = Some(6))))),
          None,
          None,
          overwrite = false))

      example(
        "INSERT OVERWRITE INTO foo VALUES (1, 2, 3), (4, 5, 6)",
        _.insertStatement(),
        InsertIntoTable(
          namedTable("foo"),
          None,
          Values(
            Seq(
              Seq(Literal(short = Some(1)), Literal(short = Some(2)), Literal(short = Some(3))),
              Seq(Literal(short = Some(4)), Literal(short = Some(5)), Literal(short = Some(6))))),
          None,
          None,
          overwrite = true))

    }
  }
}
