package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate._
import com.databricks.labs.remorph.intermediate.procedures.SetVariable
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeCommandBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeCommandBuilder = vc.commandBuilder

  "translate Declare to CreateVariable Expression" should {
    "X NUMBER DEFAULT 0;" in {
      example(
        "X NUMBER DEFAULT 0;",
        _.declareElement(),
        CreateVariable(name = Id("X"), dataType = DecimalType(38, 0), defaultExpr = Some(Literal(0)), replace = false))
    }
    "select_statement VARCHAR;" in {
      example(
        "select_statement VARCHAR;",
        _.declareElement(),
        CreateVariable(name = Id("select_statement"), dataType = StringType, defaultExpr = None, replace = false))
    }
    "price NUMBER(13,2) DEFAULT 111.50;" in {
      example(
        "price NUMBER(13,2) DEFAULT 111.50;",
        _.declareElement(),
        CreateVariable(
          name = Id("price"),
          dataType = DecimalType(Some(13), Some(2)),
          defaultExpr = Some(Literal(111.5f)),
          replace = false))
    }
    "query_statement RESULTSET := (SELECT col1 FROM some_table);" in {
      example(
        "query_statement RESULTSET := (SELECT col1 FROM some_table);",
        _.declareElement(),
        CreateVariable(
          name = Id("query_statement"),
          dataType = StructType(Seq()),
          defaultExpr = Some(
            ScalarSubquery(
              Project(NamedTable("some_table", Map(), is_streaming = false), Seq(Id("col1", caseSensitive = false))))),
          replace = false))
    }
  }

  "translate Let to SetVariable expressions" should {
    "LET X := 1;" in {
      example("LET X := 1;", _.let(), SetVariable(name = Id("X"), dataType = None, value = Literal(1)))
    }
    "LET select_statement := 'SELECT * FROM table WHERE id = ' || id;" in {
      example(
        "LET select_statement := 'SELECT * FROM table WHERE id = ' || id;",
        _.let(),
        SetVariable(
          name = Id("select_statement"),
          dataType = None,
          value = Concat(Seq(Literal("SELECT * FROM table WHERE id = "), Id("id")))))
    }
    "LET price NUMBER(13,2) DEFAULT 111.50;" in {
      example(
        "LET price NUMBER(13,2) DEFAULT 111.50;",
        _.let(),
        SetVariable(name = Id("price"), dataType = Some(DecimalType(Some(13), Some(2))), value = Literal(111.5f)))
    }
    "LET price NUMBER(13,2) := 121.55;" in {
      example(
        "LET price NUMBER(13,2) := 121.55;",
        _.let(),
        SetVariable(name = Id("price"), dataType = Some(DecimalType(Some(13), Some(2))), value = Literal(121.55f)))
    }
    "LET query_statement RESULTSET := (SELECT col1 FROM some_table);" in {
      example(
        "LET query_statement RESULTSET := (SELECT col1 FROM some_table);",
        _.let(),
        SetVariable(
          name = Id("query_statement"),
          dataType = Some(StructType(Seq(StructField("col1", UnresolvedType)))),
          value = ScalarSubquery(
            Project(NamedTable("some_table", Map(), is_streaming = false), Seq(Id("col1", caseSensitive = false))))))
    }
  }

}
