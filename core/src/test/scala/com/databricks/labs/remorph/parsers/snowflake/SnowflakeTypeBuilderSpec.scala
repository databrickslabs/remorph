package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate._
import org.antlr.v4.runtime.tree.ParseTreeVisitor
import org.scalatest.Assertion
import org.scalatest.matchers.should
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeTypeBuilderSpec extends AnyWordSpec with SnowflakeParserTestCommon with should.Matchers {

  private def example(query: String, expectedDataType: DataType): Assertion = {
    assert(new SnowflakeTypeBuilder().buildDataType(parseString(query, _.dataType())) === expectedDataType)
  }
  "SnowflakeTypeBuilder" should {
    "precision types" in {
      example("CHAR(1)", StringType)
      example("CHARACTER(1)", StringType)
      example("VARCHAR(10)", StringType)
      example("DECIMAL(10, 2)", DecimalType(Some(10), Some(2)))
      example("NUMBER(10, 2)", DecimalType(Some(10), Some(2)))
      example("NUMERIC(10, 2)", DecimalType(Some(10), Some(2)))
    }

    "non-precision types" in {
      example("ARRAY(INTEGER)", ArrayType(defaultNumber))
      example("ARRAY", ArrayType(UnresolvedType))
      example("BIGINT", defaultNumber)
      example("BINARY", BinaryType)
      example("BOOLEAN", BooleanType)
      example("BYTEINT", defaultNumber)
      example("DATE", DateType)
      example("DOUBLE", DoubleType)
      example("DOUBLE PRECISION", DoubleType)
      example("FLOAT", DoubleType)
      example("FLOAT4", DoubleType)
      example("FLOAT8", DoubleType)
      example("INT", defaultNumber)
      example("INTEGER", defaultNumber)
      example("OBJECT", UnparsedType("OBJECT"))
      example("REAL", DoubleType)
      example("SMALLINT", defaultNumber)
      example("STRING", StringType)
      example("TEXT", StringType)
      example("TIME", TimestampType)
      example("TIMESTAMP", TimestampType)
      example("TIMESTAMP_LTZ", TimestampType)
      example("TIMESTAMP_NTZ", TimestampNTZType)
      example("TIMESTAMP_TZ", TimestampType)
      example("TINYINT", TinyintType)
      example("VARBINARY", BinaryType)
      example("VARIANT", VariantType)
    }
  }

  private def defaultNumber = {
    DecimalType(Some(38), Some(0))
  }

  override protected def astBuilder: ParseTreeVisitor[_] = null
}
