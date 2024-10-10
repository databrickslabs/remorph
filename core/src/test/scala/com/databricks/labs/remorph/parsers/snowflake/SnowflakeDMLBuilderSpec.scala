package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate._
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeDMLBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with IRHelpers {

  override protected def astBuilder: SnowflakeDMLBuilder = vc.dmlBuilder

  "SnowflakeDMLBuilder" should {
    "translate INSERT statements" should {
      "INSERT INTO foo SELECT * FROM bar LIMIT 100" in {
        example(
          "INSERT INTO foo SELECT * FROM bar LIMIT 100",
          _.insertStatement(),
          InsertIntoTable(
            namedTable("foo"),
            None,
            Project(Limit(namedTable("bar"), Literal(100)), Seq(Star(None))),
            None,
            None,
            overwrite = false))
      }
      "INSERT OVERWRITE INTO foo SELECT * FROM bar LIMIT 100" in {
        example(
          "INSERT OVERWRITE INTO foo SELECT * FROM bar LIMIT 100",
          _.insertStatement(),
          InsertIntoTable(
            namedTable("foo"),
            None,
            Project(Limit(namedTable("bar"), Literal(100)), Seq(Star(None))),
            None,
            None,
            overwrite = true))
      }
      "INSERT INTO foo VALUES (1, 2, 3), (4, 5, 6)" in {
        example(
          "INSERT INTO foo VALUES (1, 2, 3), (4, 5, 6)",
          _.insertStatement(),
          InsertIntoTable(
            namedTable("foo"),
            None,
            Values(Seq(Seq(Literal(1), Literal(2), Literal(3)), Seq(Literal(4), Literal(5), Literal(6)))),
            None,
            None,
            overwrite = false))
      }
      "INSERT OVERWRITE INTO foo VALUES (1, 2, 3), (4, 5, 6)" in {
        example(
          "INSERT OVERWRITE INTO foo VALUES (1, 2, 3), (4, 5, 6)",
          _.insertStatement(),
          InsertIntoTable(
            namedTable("foo"),
            None,
            Values(Seq(Seq(Literal(1), Literal(2), Literal(3)), Seq(Literal(4), Literal(5), Literal(6)))),
            None,
            None,
            overwrite = true))
      }
    }

    "translate DELETE statements" should {
      "direct" in {
        example(
          "DELETE FROM t WHERE t.c1 > 42",
          _.deleteStatement(),
          DeleteFromTable(namedTable("t"), None, Some(GreaterThan(Dot(Id("t"), Id("c1")), Literal(42))), None, None))
      }

      "as merge" should {
        "DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2" in {
          example(
            "DELETE FROM t1 USING t2 WHERE t1.c1 = t2.c2",
            _.deleteStatement(),
            MergeIntoTable(
              namedTable("t1"),
              namedTable("t2"),
              Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
              matchedActions = Seq(DeleteAction(None))))
        }
        "DELETE FROM table1 AS t1 USING (SELECT * FROM table2) AS t2 WHERE t1.c1 = t2.c2" in {
          example(
            "DELETE FROM table1 AS t1 USING (SELECT * FROM table2) AS t2 WHERE t1.c1 = t2.c2",
            _.deleteStatement(),
            MergeIntoTable(
              TableAlias(namedTable("table1"), "t1", Seq()),
              SubqueryAlias(Project(namedTable("table2"), Seq(Star(None))), Id("t2"), Seq()),
              Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
              matchedActions = Seq(DeleteAction(None))))
        }
      }
    }

    "translate UPDATE statements" should {
      "UPDATE t1 SET c1 = 42" in {
        example(
          "UPDATE t1 SET c1 = 42",
          _.updateStatement(),
          UpdateTable(namedTable("t1"), None, Seq(Assign(Column(None, Id("c1")), Literal(42))), None, None, None))
      }
      "UPDATE t1 SET c1 = 42 WHERE c1 < 0" in {
        example(
          "UPDATE t1 SET c1 = 42 WHERE c1 < 0",
          _.updateStatement(),
          UpdateTable(
            namedTable("t1"),
            None,
            Seq(Assign(Column(None, Id("c1")), Literal(42))),
            Some(LessThan(Id("c1"), Literal(0))),
            None,
            None))
      }
      "UPDATE table1 as t1 SET c1 = c2 + t2.c2 FROM table2 as t2 WHERE t1.c3 = t2.c3" in {
        example(
          "UPDATE table1 as t1 SET c1 = c2 + t2.c2 FROM table2 as t2 WHERE t1.c3 = t2.c3",
          _.updateStatement(),
          UpdateTable(
            TableAlias(namedTable("table1"), "t1", Seq()),
            Some(
              crossJoin(TableAlias(namedTable("table1"), "t1", Seq()), TableAlias(namedTable("table2"), "t2", Seq()))),
            Seq(Assign(Column(None, Id("c1")), Add(Id("c2"), Dot(Id("t2"), Id("c2"))))),
            Some(Equals(Dot(Id("t1"), Id("c3")), Dot(Id("t2"), Id("c3")))),
            None,
            None))
      }
    }

    "translate MERGE statements" should {
      "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN UPDATE SET c1 = 42" in {
        example(
          "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN UPDATE SET c1 = 42",
          _.mergeStatement(),
          MergeIntoTable(
            namedTable("t1"),
            namedTable("t2"),
            Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
            matchedActions = Seq(UpdateAction(None, Seq(Assign(Column(None, Id("c1")), Literal(42)))))))
      }

      "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN DELETE" in {
        example(
          "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN DELETE",
          _.mergeStatement(),
          MergeIntoTable(
            namedTable("t1"),
            namedTable("t2"),
            Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
            matchedActions = Seq(DeleteAction(None))))
      }

      "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED AND t2.date = '01/01/2024' THEN DELETE" in {
        example(
          "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED AND t2.date = '01/01/2024' THEN DELETE",
          _.mergeStatement(),
          MergeIntoTable(
            namedTable("t1"),
            namedTable("t2"),
            Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
            matchedActions = Seq(DeleteAction(Some(Equals(Dot(Id("t2"), Id("date")), Literal("01/01/2024")))))))
      }

      "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN DELETE WHEN NOT MATCHED THEN INSERT" in {
        example(
          "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN DELETE WHEN NOT MATCHED THEN INSERT",
          _.mergeStatement(),
          MergeIntoTable(
            namedTable("t1"),
            namedTable("t2"),
            Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
            matchedActions = Seq(DeleteAction(None)),
            notMatchedActions = Seq(InsertAction(None, Seq.empty[Assign]))))
      }

      "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN UPDATE SET t1.c1 = 42" in {
        example(
          "MERGE INTO t1 USING t2 ON t1.c1 = t2.c2 WHEN MATCHED THEN UPDATE SET t1.c1 = 42",
          _.mergeStatement(),
          MergeIntoTable(
            namedTable("t1"),
            namedTable("t2"),
            Equals(Dot(Id("t1"), Id("c1")), Dot(Id("t2"), Id("c2"))),
            matchedActions =
              Seq(UpdateAction(None, Seq(Assign(Column(Some(ObjectReference(Id("t1"))), Id("c1")), Literal(42)))))))
      }

    }
  }

}
