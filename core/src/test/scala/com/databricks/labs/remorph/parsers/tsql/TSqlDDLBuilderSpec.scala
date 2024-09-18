package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.{Batch, IRHelpers, LogicalPlan}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlDDLBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = new TSqlAstBuilder

//  private def example(query: String, expectedAst: LogicalPlan): Unit =
//    example(query, _.tSqlFile(), expectedAst)

  private def singleQueryExample(query: String, expectedAst: LogicalPlan): Unit =
    example(query, _.tSqlFile(), Batch(Seq(expectedAst)))

  "tsql DDL visitor" should {

    "translate a simple CREATE TABLE" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT, b VARCHAR(10))",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Seq.empty,
          Seq.empty,
          None,
          Some(Seq.empty)))
    }

    "translate a CREATE TABLE with a primary key, foreign key and a Unique column" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT PRIMARY KEY, b VARCHAR(10) UNIQUE, FOREIGN KEY (b) REFERENCES other_table(b))",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map("a" -> Seq(ir.PrimaryKey()), "b" -> Seq(ir.Unique())),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Seq(ir.ForeignKey("b", "other_table", "b", Seq.empty)),
          Seq.empty,
          None,
          Some(Seq.empty)))
    }

    "translate a CREATE TABLE with a CHECK constraint and column options" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT SPARSE, b VARCHAR(10), CONSTRAINT c1 CHECK (a > 0))",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Map("a" -> Seq(ir.OptionUnresolved("Unsupported Option: SPARSE")), "b" -> Seq.empty),
          Seq(
            ir.NamedConstraint(
              "c1",
              ir.CheckConstraint(ir.GreaterThan(ir.Column(None, ir.Id("a")), ir.Literal(0, ir.IntegerType))))),
          Seq.empty,
          None,
          Some(Seq.empty)))
    }

    "translate a CREATE TABLE with a DEFAULT constraint" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT DEFAULT 0, b VARCHAR(10) DEFAULT 'foo')",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map(
            "a" -> Seq(ir.DefaultValueConstraint(ir.Literal(0, ir.IntegerType))),
            "b" -> Seq(ir.DefaultValueConstraint(ir.Literal("foo", ir.StringType)))),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Seq.empty,
          Seq.empty,
          None,
          Some(Seq.empty)))
    }

    "translate a CREATE TABLE with a complex FK constraint" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT, b VARCHAR(10), CONSTRAINT c1 FOREIGN KEY (a, b) REFERENCES other_table(c, d))",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Seq(ir.NamedConstraint("c1", ir.ForeignKey("a, b", "other_table", "c, d", Seq.empty))),
          Seq.empty,
          None,
          Some(Seq.empty)))
    }
  }
}
