/*
package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.{Concat, DecimalType, IRHelpers, Id, Literal, SetVariable}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.mockito.MockitoSugar

import scala.Console.in

class SnowflakeCommandBuilderSpec
    extends AnyWordSpec
    with SnowflakeParserTestCommon
    with Matchers
    with MockitoSugar
    with IRHelpers {

  override protected def astBuilder: SnowflakeCommandBuilder =
    new SnowflakeCommandBuilder

  "translate Let to SetVariable expressions" in {
    example("LET X := 1;", _.let(), SetVariable(name = "X", dataType = None, expr = Some(Literal(short = Some(1)))))

    example(
      "select_statement := 'select * from table where id = ' || id;",
      _.let(),
      SetVariable(
        name = "select_statement",
        dataType = None,
        expr = Some(Concat(Literal(string = Some("select * from table where id = ")), Id("id")))))

    example(
      "let price number(13,2) default 111.50;",
      _.let(),
      SetVariable(
        name = "price",
        dataType = Some(DecimalType(Some(13), Some(2))),
        expr = Some(Literal(float = Some(111.5f)))))

    example(
      "let price number(13,2) := 121.55;",
      _.let(),
      SetVariable(
        name = "price",
        dataType = Some(DecimalType(Some(13), Some(2))),
        expr = Some(Literal(float = Some(121.55f)))))

  }

}
 */
