package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
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

    "translate DELETE statements" in {
      example(
        "DELETE FROM t WHERE t.c1 > 42",
        _.deleteStatement(),
        DeleteFromTable(
          namedTable("t"),
          None,
          Some(GreaterThan(Dot(Id("t"), Id("c1")), Literal(short = Some(42)))),
          None,
          None))

      example(
        "DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2",
        _.deleteStatement(),
        DeleteFromTable(
          namedTable("t1"),
          Some(
            Join(
              namedTable("t1"),
              namedTable("t2"),
              None,
              CrossJoin,
              Seq(),
              JoinDataType(is_left_struct = false, is_right_struct = false))),
          Some(Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2")))),
          None,
          None))

      example(
        "DELETE FROM table1 AS t1 USING (SELECT * FROM table2) AS t2 WHERE t1.c1 = t2.c2",
        _.deleteStatement(),
        DeleteFromTable(
          TableAlias(namedTable("table1"), "t1", Seq()),
          Some(
            Join(
              TableAlias(namedTable("table1"), "t1", Seq()),
              SubqueryAlias(Project(namedTable("table2"), Seq(Star(None))), Id("t2"), Seq()),
              None,
              CrossJoin,
              Seq(),
              JoinDataType(is_left_struct = false, is_right_struct = false))),
          Some(Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2")))),
          None,
          None))

    }

    "translate UPDATE statements" in {
      example(
        "UPDATE t1 SET c1 = 42",
        _.updateStatement(),
        UpdateTable(namedTable("t1"), None, Seq(Assign(Id("c1"), Literal(short = Some(42)))), None, None, None))

      example(
        "UPDATE t1 SET c1 = 42 WHERE c1 < 0",
        _.updateStatement(),
        UpdateTable(
          namedTable("t1"),
          None,
          Seq(Assign(Id("c1"), Literal(short = Some(42)))),
          Some(LessThan(Id("c1"), Literal(short = Some(0)))),
          None,
          None))

      example(
        "UPDATE table1 as t1 SET c1 = c2 + t2.c2 FROM table2 as t2 WHERE t1.c3 = t2.c3",
        _.updateStatement(),
        UpdateTable(
          TableAlias(namedTable("table1"), "t1", Seq()),
          Some(crossJoin(TableAlias(namedTable("table1"), "t1", Seq()), TableAlias(namedTable("table2"), "t2", Seq()))),
          Seq(Assign(Id("c1"), Add(Id("c2"), Dot(Id("t2"), Id("c2"))))),
          Some(Equals(Dot(Id("t1"), Id("c3")), Dot(Id("t2"), Id("c3")))),
          None,
          None))

    }
  }
}
