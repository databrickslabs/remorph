package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.DataTypeContext
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   https://spark.apache.org/docs/latest/sql-ref-datatypes.html
 * @see
 *   https://docs.snowflake.com/en/sql-reference-data-types
 */
class SnowflakeTypeBuilder {
  // see https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint
  private def defaultNumber = ir.DecimalType(Some(38), Some(0))

  def buildDataType(ctx: DataTypeContext): ir.DataType = ctx match {
    case null => ir.UnresolvedType
    case _ if ctx.ARRAY() != null => ir.ArrayType(buildDataType(ctx.dataType()))
    case _ if ctx.OBJECT() != null => ir.UnparsedType("OBJECT") // TODO: get more examples
    case _ =>
      val typeDef = ctx.id.getText.toUpperCase()
      typeDef match {
        // precision types - loosing precision except for decimal
        case "CHAR" | "NCHAR" | "CHARACTER" => ir.StringType // character types
        case "CHAR_VARYING" | "NCHAR_VARYING" | "NVARCHAR2" | "NVARCHAR" | "STRING" | "TEXT" | "VARCHAR" =>
          ir.StringType // VARCHAR is string type in Databricks
        case "NUMBER" | "NUMERIC" | "DECIMAL" => decimal(ctx)
        case "TIMESTAMP" | "TIMESTAMP_LTZ" | "TIMESTAMP_TZ" | "TIMESTAMPTZ" => ir.TimestampType
        case "TIMESTAMP_NTZ" => ir.TimestampNTZType

        // non-precision types
        case "BIGINT" => defaultNumber
        case "BINARY" => ir.BinaryType
        case "BOOLEAN" => ir.BooleanType
        case "BYTEINT" => defaultNumber
        case "DATE" => ir.DateType
        case "DOUBLE" => ir.DoubleType
        case "DOUBLE PRECISION" => ir.DoubleType
        case "FLOAT" => ir.DoubleType
        case "FLOAT4" => ir.DoubleType
        case "FLOAT8" => ir.DoubleType
        case "INT" => defaultNumber
        case "INTEGER" => defaultNumber
        case "REAL" => ir.DoubleType
        case "SMALLINT" => defaultNumber
        case "TIME" => ir.TimestampType
        case "TINYINT" => ir.TinyintType
        case "VARBINARY" => ir.BinaryType
        case "VARIANT" => ir.VariantType

        // TODO: GEOGRAPHY is not yet catered for in Snowflake type builder
        // TODO: GEOMETRY is not yet catered for in Snowflake type builder

        // and everything else must be an input error or a type we don't know about yet
        case _ => ir.UnparsedType(typeDef)
      }
  }

  private def decimal(c: DataTypeContext) = {
    val nums = c.INT().asScala
    // https://docs.snowflake.com/en/sql-reference/data-types-numeric#number
    // Per Docs defaulting the precision to 38 and scale to 0
    val precision = nums.headOption.map(_.getText.toInt).getOrElse(38)
    val scale = nums.drop(1).headOption.map(_.getText.toInt).getOrElse(0)
    ir.DecimalType(precision, scale)
  }
}
