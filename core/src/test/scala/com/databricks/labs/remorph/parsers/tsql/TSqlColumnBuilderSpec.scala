package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlColumnBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlColumnBuilder

  "TSqlColumnBuilder" should {

    "translate a simple column" in {
      example("a", _.selectListElem(), Column("a"))
      example("#a", _.selectListElem(), Column("#a"))
      example("[a]", _.selectListElem(), Column("[a]"))
      example("\"a\"", _.selectListElem(), Column("\"a\""))
      example("RAW", _.selectListElem(), Column("RAW"))
    }

    "translate a column with a table" in {
      example("table_x.a", _.selectListElem(), Column("table_x.a"))
    }

    "translate a column with a schema" in {
      example("schema1.table_x.a", _.selectListElem(), Column("schema1.table_x.a"))
    }

    "translate a column with a database" in {
      example("database1.schema1.table_x.a", _.selectListElem(), Column("database1.schema1.table_x.a"))
    }

    "translate a column with a server" in {
      example("server1..schema1.table_x.a", _.fullColumnName(), Column("server1..schema1.table_x.a"))
    }

    "translate a column without a table reference" in {
      example("a", _.fullColumnName(), Column("a"))
    }

    "translate a list of elements" in {
      example("a, b, c", _.selectList(), ExpressionList(Seq(Column("a"), Column("b"), Column("c"))))
    }

    "translate search conditions" in {
      example("a = b", _.searchCondition(), Equals(Column("a"), Column("b")))
      example("a > b", _.searchCondition(), GreaterThan(Column("a"), Column("b")))
      example("a < b", _.searchCondition(), LesserThan(Column("a"), Column("b")))
      example("a >= b", _.searchCondition(), GreaterThanOrEqual(Column("a"), Column("b")))
      example("a <= b", _.searchCondition(), LesserThanOrEqual(Column("a"), Column("b")))
      example("a > = b", _.searchCondition(), GreaterThanOrEqual(Column("a"), Column("b")))
      example("a <  = b", _.searchCondition(), LesserThanOrEqual(Column("a"), Column("b")))
      example("a <> b", _.searchCondition(), NotEquals(Column("a"), Column("b")))
      example("NOT a = b", _.searchCondition(), Not(Equals(Column("a"), Column("b"))))
      example(
        "a = b AND c = e",
        _.searchCondition(),
        And(Equals(Column("a"), Column("b")), Equals(Column("c"), Column("e"))))
      example(
        "a = b OR c = e",
        _.searchCondition(),
        Or(Equals(Column("a"), Column("b")), Equals(Column("c"), Column("e"))))
      example(
        "a = b AND c = x OR e = f",
        _.searchCondition(),
        Or(And(Equals(Column("a"), Column("b")), Equals(Column("c"), Column("x"))), Equals(Column("e"), Column("f"))))
      example(
        "a = b AND (c = x OR e = f)",
        _.searchCondition(),
        And(Equals(Column("a"), Column("b")), Or(Equals(Column("c"), Column("x")), Equals(Column("e"), Column("f")))))
    }
  }
}
