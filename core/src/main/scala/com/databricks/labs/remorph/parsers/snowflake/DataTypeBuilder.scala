package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.DataTypeContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   https://spark.apache.org/docs/latest/sql-ref-datatypes.html
 * @see
 *   https://docs.snowflake.com/en/sql-reference-data-types
 */
object DataTypeBuilder {
  def buildDataType(ctx: DataTypeContext): ir.DataType = {
    val typeDef = ctx.getText.toUpperCase()
    typeDef match {
      // precision types
      case _ if ctx.charAlias != null => ir.CharType(maybeSize(ctx))
      case _ if ctx.numberAlias != null => decimal(ctx)
      case _ if ctx.VARCHAR() != null => ir.VarCharType(maybeSize(ctx))

      // non-precision types
      case "ARRAY" => ir.ArrayType(ir.UnresolvedType)
      case "BIGINT" => ir.LongType
      case "BINARY" => ir.BinaryType
      case "BOOLEAN" => ir.BooleanType
      case "BYTEINT" => ir.IntegerType
      case "DATE" => ir.DateType
      case "DOUBLE" => ir.DoubleType
      case "DOUBLE PRECISION" => ir.DoubleType
      case "FLOAT" => ir.FloatType
      case "FLOAT4" => ir.FloatType
      case "FLOAT8" => ir.DoubleType
      case "INT" => ir.IntegerType
      case "INTEGER" => ir.IntegerType
      case "OBJECT" => ir.UnparsedType("OBJECT") // TODO: get more examples
      case "REAL" => ir.FloatType
      case "SMALLINT" => ir.ShortType
      case "STRING" => ir.StringType
      case "TEXT" => ir.StringType
      case "TIME" => ir.TimestampType
      case "TIMESTAMP" => ir.TimestampType
      case "TIMESTAMP_LTZ" => ir.TimestampType
      case "TIMESTAMP_NTZ" => ir.TimestampNTZType
      case "TIMESTAMP_TZ" => ir.TimestampType
      case "TINYINT" => ir.ShortType
      case "VARBINARY" => ir.BinaryType
      case "VARIANT" => ir.UnparsedType("VARIANT") // TODO: get more examples

      // and everything else
      case _ => ir.UnparsedType(typeDef)
    }
  }

  private def decimal(c: DataTypeContext) = {
    val nums = c.num().asScala
    val precision = nums.headOption.map(_.getText.toInt)
    val scale = nums.drop(1).headOption.map(_.getText.toInt)
    ir.DecimalType(precision, scale)
  }

  private def maybeSize(ctx: DataTypeContext) = {
    Option(ctx.dataTypeSize()).map(_.num().getText.toInt)
  }
}
