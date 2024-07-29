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
      "x number default 0;",
      _.declareStatement(),
      CreateVariable(
        name = "x",
        dataType = DecimalType(None, None),
        defaultExpr = Some(Literal(short = Some(0))),
        replace = false))

    example(
      "select_statement varchar;",
      _.declareStatement(),
      CreateVariable(name = "select_statement", dataType = VarCharType(None), defaultExpr = None, replace = false))

  }

  "translate Let to SetVariable expressions" in {
    example("LET X := 1;", _.let(), SetVariable(name = "X", dataType = None, value = Literal(short = Some(1))))

    example(
      "select_statement := 'select * from table where id = ' || id;",
      _.let(),
      SetVariable(
        name = "select_statement",
        dataType = None,
        value = Concat(Seq(Literal(string = Some("select * from table where id = ")), Id("id")))))

    example(
      "let price number(13,2) default 111.50;",
      _.let(),
      SetVariable(
        name = "price",
        dataType = Some(DecimalType(Some(13), Some(2))),
        value = Literal(float = Some(111.5f))))

    example(
      "let price number(13,2) := 121.55;",
      _.let(),
      SetVariable(
        name = "price",
        dataType = Some(DecimalType(Some(13), Some(2))),
        value = Literal(float = Some(121.55f))))

  }

}
