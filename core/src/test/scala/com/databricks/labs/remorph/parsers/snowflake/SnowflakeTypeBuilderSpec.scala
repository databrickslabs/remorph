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

    "ARRAY(INTEGER)" in {
      example("ARRAY(INTEGER)", ArrayType(defaultNumber))
    }
    "ARRAY" in {
      example("ARRAY", ArrayType(UnresolvedType))
    }
    "BIGINT" in {
      example("BIGINT", defaultNumber)
    }
    "BINARY" in {
      example("BINARY", BinaryType)
    }
    "BOOLEAN" in {
      example("BOOLEAN", BooleanType)
    }
    "BYTEINT" in {
      example("BYTEINT", defaultNumber)
    }
    "DATE" in {
      example("DATE", DateType)
    }
    "DOUBLE" in {
      example("DOUBLE", DoubleType)
    }
    "DOUBLE PRECISION" in {
      example("DOUBLE PRECISION", DoubleType)
    }
    "FLOAT" in {
      example("FLOAT", DoubleType)
    }
    "FLOAT4" in {
      example("FLOAT4", DoubleType)
    }
    "FLOAT8" in {
      example("FLOAT8", DoubleType)
    }
    "INT" in {
      example("INT", defaultNumber)
    }
    "INTEGER" in {
      example("INTEGER", defaultNumber)
    }
    "OBJECT" in {
      example("OBJECT", UnparsedType("OBJECT"))
    }
    "REAL" in {
      example("REAL", DoubleType)
    }
    "SMALLINT" in {
      example("SMALLINT", defaultNumber)
    }
    "STRING" in {
      example("STRING", StringType)
    }
    "TEXT" in {
      example("TEXT", StringType)
    }
    "TIME" in {
      example("TIME", TimestampType)
    }
    "TIMESTAMP" in {
      example("TIMESTAMP", TimestampType)
    }
    "TIMESTAMP_LTZ" in {
      example("TIMESTAMP_LTZ", TimestampType)
    }
    "TIMESTAMP_NTZ" in {
      example("TIMESTAMP_NTZ", TimestampNTZType)
    }
    "TIMESTAMP_TZ" in {
      example("TIMESTAMP_TZ", TimestampType)
    }
    "TINYINT" in {
      example("TINYINT", TinyintType)
    }
    "VARBINARY" in {
      example("VARBINARY", BinaryType)
    }
    "VARIANT" in {
      example("VARIANT", VariantType)
    }
  }

  private def defaultNumber = {
    DecimalType(Some(38), Some(0))
  }

  override protected def astBuilder: ParseTreeVisitor[_] = null
}
