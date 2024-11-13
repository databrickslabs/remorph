package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqlDDLBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with ir.IRHelpers {

  override protected def astBuilder: TSqlParserBaseVisitor[_] = vc.astBuilder

  private def singleQueryExample(query: String, expectedAst: ir.LogicalPlan): Unit =
    example(query, _.tSqlFile(), ir.Batch(Seq(expectedAst)))

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

    "translate a CREATE TABLE with various column level constraints" in {
      singleQueryExample(
        "CREATE TABLE example_table (id INT PRIMARY KEY, name VARCHAR(50) NOT NULL, age INT CHECK (age >= 18)," +
          "email VARCHAR(100) UNIQUE, department_id INT FOREIGN KEY REFERENCES departments(id));",
        ir.CreateTableParams(
          ir.CreateTable(
            "example_table",
            None,
            None,
            None,
            ir.StructType(Seq(
              ir.StructField("id", ir.IntegerType),
              ir.StructField("name", ir.VarcharType(Some(50)), nullable = false),
              ir.StructField("age", ir.IntegerType),
              ir.StructField("email", ir.VarcharType(Some(100))),
              ir.StructField("department_id", ir.IntegerType)))),
          Map(
            "name" -> Seq.empty,
            "email" -> Seq(ir.Unique()),
            "department_id" -> Seq.empty,
            "age" -> Seq.empty,
            "id" -> Seq(ir.PrimaryKey())),
          Map(
            "name" -> Seq.empty,
            "email" -> Seq.empty,
            "department_id" -> Seq.empty,
            "age" -> Seq.empty,
            "id" -> Seq.empty),
          Seq(
            ir.CheckConstraint(ir.GreaterThanOrEqual(ir.Column(None, ir.Id("age")), ir.Literal(18, ir.IntegerType))),
            ir.ForeignKey("department_id", "departments", "id", Seq.empty)),
          Seq.empty,
          None,
          Some(Seq.empty)))
    }

    "translate a CREATE TABLE with a named NULL constraint" in {
      singleQueryExample(
        "CREATE TABLE example_table (id VARCHAR(10) CONSTRAINT c1 NOT NULL);",
        ir.CreateTableParams(
          ir.CreateTable(
            "example_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("id", ir.VarcharType(Some(10)))))),
          Map("id" -> Seq.empty),
          Map("id" -> Seq.empty),
          Seq(ir.NamedConstraint("c1", ir.CheckConstraint(ir.IsNotNull(ir.Column(None, ir.Id("id")))))),
          Seq.empty,
          None,
          Some(Seq.empty)))
    }
  }

  "translate a CREATE TABLE with unsupported table level TSQL options" in {
    singleQueryExample(
      "CREATE TABLE example_table (id INT) WITH (LEDGER = ON);",
      ir.CreateTableParams(
        ir.CreateTable("example_table", None, None, None, ir.StructType(Seq(ir.StructField("id", ir.IntegerType)))),
        Map("id" -> Seq.empty),
        Map("id" -> Seq.empty),
        Seq.empty,
        Seq.empty,
        None,
        Some(Seq(ir.OptionUnresolved("LEDGER = ON")))))

  }
}
