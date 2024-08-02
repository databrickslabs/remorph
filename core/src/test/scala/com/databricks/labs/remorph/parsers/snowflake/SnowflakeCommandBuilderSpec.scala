package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

class SnowflakeCommandBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeCommandBuilder =
    new SnowflakeCommandBuilder

  "translate Declare to CreateVariable Expression" in {
    example(
      "X NUMBER DEFAULT 0;",
      _.declareStatement(),
      CreateVariable(
        name = Id("X"),
        dataType = DecimalType(None, None),
        defaultExpr = Some(Literal(short = Some(0))),
        replace = false))

    example(
      "select_statement VARCHAR;",
      _.declareStatement(),
      CreateVariable(name = Id("select_statement"), dataType = VarCharType(None), defaultExpr = None, replace = false))

    example(
      "price NUMBER(13,2) DEFAULT 111.50;",
      _.declareStatement(),
      CreateVariable(
        name = Id("price"),
        dataType = DecimalType(Some(13), Some(2)),
        defaultExpr = Some(Literal(float = Some(111.5f))),
        replace = false))

    example(
      "query_statement RESULTSET := (SELECT col1 FROM some_table);",
      _.declareStatement(),
      CreateVariable(
        name = Id("query_statement"),
        dataType = StructType(),
        defaultExpr = Some(
          ScalarSubquery(
            Project(
              NamedTable("some_table", Map(), is_streaming = false),
              Seq(Column(None, Id("col1", caseSensitive = false)))))),
        replace = false))

  }

  "translate Let to SetVariable expressions" in {
    example("LET X := 1;", _.let(), SetVariable(name = Id("X"), dataType = None, value = Literal(short = Some(1))))

    example(
      "select_statement := 'SELECT * FROM table WHERE id = ' || id;",
      _.let(),
      SetVariable(
        name = Id("select_statement"),
        dataType = None,
        value = Concat(Seq(Literal(string = Some("SELECT * FROM table WHERE id = ")), Id("id")))))

    example(
      "LET price NUMBER(13,2) DEFAULT 111.50;",
      _.let(),
      SetVariable(
        name = Id("price"),
        dataType = Some(DecimalType(Some(13), Some(2))),
        value = Literal(float = Some(111.5f))))

    example(
      "LET price NUMBER(13,2) := 121.55;",
      _.let(),
      SetVariable(
        name = Id("price"),
        dataType = Some(DecimalType(Some(13), Some(2))),
        value = Literal(float = Some(121.55f))))

    example(
      "LET query_statement RESULTSET := (SELECT col1 FROM some_table);",
      _.let(),
      SetVariable(
        name = Id("query_statement"),
        dataType = Some(StructType()),
        value = ScalarSubquery(
          Project(
            NamedTable("some_table", Map(), is_streaming = false),
            Seq(Column(None, Id("col1", caseSensitive = false)))))))

  }

}
