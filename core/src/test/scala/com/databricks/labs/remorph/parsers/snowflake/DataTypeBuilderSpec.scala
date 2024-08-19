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
    "precision types" in {
      example("CHAR(1)", CharType(Some(1)))
      example("CHARACTER(1)", CharType(Some(1)))
      example("DECIMAL(10, 2)", DecimalType(Some(10), Some(2)))
      example("NUMBER(10, 2)", DecimalType(Some(10), Some(2)))
      example("NUMERIC(10, 2)", DecimalType(Some(10), Some(2)))
      example("VARCHAR(10)", VarCharType(Some(10)))
    }

    "non-precision types" in {
      example("ARRAY", ArrayType(UnresolvedType))
      example("BIGINT", LongType)
      example("BINARY", BinaryType)
      example("BOOLEAN", BooleanType)
      example("BYTEINT", IntegerType)
      example("DATE", DateType)
      example("DOUBLE", DoubleType)
      example("DOUBLE PRECISION", DoubleType)
      example("FLOAT", FloatType)
      example("FLOAT4", FloatType)
      example("FLOAT8", DoubleType)
      example("INT", IntegerType)
      example("INTEGER", IntegerType)
      example("OBJECT", UnparsedType("OBJECT"))
      example("REAL", FloatType)
      example("SMALLINT", ShortType)
      example("STRING", StringType)
      example("TEXT", StringType)
      example("TIME", TimestampType)
      example("TIMESTAMP", TimestampType)
      example("TIMESTAMP_LTZ", TimestampType)
      example("TIMESTAMP_NTZ", TimestampNTZType)
      example("TIMESTAMP_TZ", TimestampType)
      example("TINYINT", ShortType)
      example("VARBINARY", BinaryType)
      example("VARIANT", UnparsedType("VARIANT"))
    }
  }

  override protected def astBuilder: ParseTreeVisitor[_] = null
}
