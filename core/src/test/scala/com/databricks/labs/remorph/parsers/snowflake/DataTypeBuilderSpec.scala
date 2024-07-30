package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate._
import org.antlr.v4.runtime.tree.ParseTreeVisitor
import org.scalatest.Assertion
import org.scalatest.matchers.should
import org.scalatest.wordspec.AnyWordSpec

class DataTypeBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with should.Matchers {

  private def example(query: String, expectedDataType: DataType): Assertion = {
    assert(DataTypeBuilder.buildDataType(parseString(query, _.dataType())) === expectedDataType)
  }
  "DataTypeBuilder" should {
    "translate most of Snowflake datatypes" in {
      example("VARCHAR", VarCharType(None))
      example("VARCHAR(32)", VarCharType(Some(32)))
      example("INT", DecimalType(Some(38), None))
      example("NUMBER", DecimalType(None, None))
      example("NUMBER(12)", DecimalType(Some(12), None))
      example("NUMBER(12, 5)", DecimalType(Some(12), Some(5)))
      example("CHAR", CharType(None))
      example("CHAR(8)", CharType(Some(8)))
      example("FLOAT", DoubleType)
      example("DOUBLE", DoubleType)
      example("BOOLEAN", BooleanType)
      example("DATE", DateType)
      example("BINARY", BinaryType)
      example("ARRAY", ArrayType(UnresolvedType))
    }

    "translate the rest to UnparsedType" in {
      example("VARIANT", UnparsedType())
      example("OBJECT", UnparsedType())
    }
  }

  override protected def astBuilder: ParseTreeVisitor[_] = null
}
