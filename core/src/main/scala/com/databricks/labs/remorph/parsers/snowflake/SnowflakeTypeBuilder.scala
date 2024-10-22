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

  def buildDataType(ctx: DataTypeContext): ir.DataType = {
    if (ctx == null) {
      return ir.UnresolvedType
    }
    val typeDef = ctx.getText.toUpperCase()
    typeDef match {
      // precision types - loosing precision except for decimal
      case _ if ctx.charAlias != null => ir.StringType
      case _ if ctx.varcharAlias != null => ir.StringType
      case _ if ctx.numberAlias != null => decimal(ctx)
      case _ if ctx.TIMESTAMP() != null => ir.TimestampType
      case _ if ctx.TIMESTAMP_LTZ() != null => ir.TimestampType
      case _ if ctx.TIMESTAMP_NTZ() != null => ir.TimestampNTZType

      // non-precision types
      case _ if ctx.ARRAY() != null => ir.ArrayType(buildDataType(ctx.dataType()))
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
      case "OBJECT" => ir.UnparsedType("OBJECT") // TODO: get more examples
      case "REAL" => ir.DoubleType
      case "SMALLINT" => defaultNumber
      case "STRING" => ir.StringType
      case "TEXT" => ir.StringType
      case "TIME" => ir.TimestampType
      case "TIMESTAMP_TZ" => ir.TimestampType
      case "TINYINT" => ir.TinyintType
      case "VARBINARY" => ir.BinaryType
      case "VARIANT" => ir.VariantType

      // and everything else
      case _ => ir.UnparsedType(typeDef)
    }
  }

  private def decimal(c: DataTypeContext) = {
    val nums = c.num().asScala
    // https://docs.snowflake.com/en/sql-reference/data-types-numeric#number
    // Per Docs defaulting the precision to 38 and scale to 0
    val precision = nums.headOption.map(_.getText.toInt).getOrElse(38)
    val scale = nums.drop(1).headOption.map(_.getText.toInt).getOrElse(0)
    ir.DecimalType(precision, scale)
  }
}
