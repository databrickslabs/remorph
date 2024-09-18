package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.{Batch, IRHelpers, LogicalPlan}
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class TSqkDDLBuilderSpec extends AnyWordSpec with TSqlParserTestCommon with Matchers with IRHelpers {

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

    "translate a CREATE TABLE with a primary key" in {
      singleQueryExample(
        "CREATE TABLE some_table (a INT PRIMARY KEY, b VARCHAR(10))",
        ir.CreateTableParams(
          ir.CreateTable(
            "some_table",
            None,
            None,
            None,
            ir.StructType(Seq(ir.StructField("a", ir.IntegerType), ir.StructField("b", ir.VarcharType(Some(10)))))),
          Map("a" -> Seq(ir.PrimaryKey(Seq.empty, None)), "b" -> Seq.empty),
          Map("a" -> Seq.empty, "b" -> Seq.empty),
          Seq.empty,
          Seq.empty,
          None,
          Some(Seq.empty)))
    }
  }
}
