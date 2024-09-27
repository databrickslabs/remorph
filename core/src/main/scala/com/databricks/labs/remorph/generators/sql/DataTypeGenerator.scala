package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

/**
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/sql-ref-datatypes.html
 */
object DataTypeGenerator {

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): String = dt match {
    case ir.NullType => "VOID"
    case ir.BooleanType => "BOOLEAN"
    case ir.BinaryType => "BINARY"
    case ir.ShortType => "SMALLINT"
    case ir.TinyintType => "TINYINT"
    case ir.IntegerType => "INT"
    case ir.LongType => "BIGINT"
    case ir.FloatType => "FLOAT"
    case ir.DoubleType => "DOUBLE"
    case ir.DecimalType(precision, scale) =>
      val arguments = precision.toSeq ++ scale.toSeq
      if (arguments.isEmpty) {
        "DECIMAL"
      } else {
        s"DECIMAL${arguments.mkString("(", ", ", ")")}"
      }
    case ir.StringType => "STRING"
    case ir.DateType => "DATE"
    case ir.TimestampType => "TIMESTAMP"
    case ir.TimestampNTZType => "TIMESTAMP_NTZ"
    case ir.ArrayType(elementType) => s"ARRAY<${generateDataType(ctx, elementType)}>"
    case ir.StructType(fields) =>
      val fieldTypes = fields
        .map { case ir.StructField(name, dataType, nullable) =>
          val isNullable = if (nullable) "" else " NOT NULL"
          s"$name:${generateDataType(ctx, dataType)}$isNullable"
        }
        .mkString(",")
      s"STRUCT<$fieldTypes>"
    case ir.MapType(keyType, valueType) =>
      s"MAP<${generateDataType(ctx, keyType)}, ${generateDataType(ctx, valueType)}>"
    case ir.VarcharType(size) => s"VARCHAR${maybeSize(size)}"
    case ir.CharType(size) => s"CHAR${maybeSize(size)}"
    case _ => throw TranspileException(s"not implemented: $dt")
  }

  private def maybeSize(size: Option[Int]): String = size.map(s => s"($s)").getOrElse("")
}
