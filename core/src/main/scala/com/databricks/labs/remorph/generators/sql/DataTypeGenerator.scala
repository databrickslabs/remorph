package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{OkResult, PartialResult, Result, intermediate => ir}

/**
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/sql-ref-datatypes.html
 */
object DataTypeGenerator {

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): Result[String] = dt match {
    case ir.NullType => OkResult("VOID")
    case ir.BooleanType => OkResult("BOOLEAN")
    case ir.BinaryType => OkResult("BINARY")
    case ir.ShortType => OkResult("SMALLINT")
    case ir.TinyintType => OkResult("TINYINT")
    case ir.IntegerType => OkResult("INT")
    case ir.LongType => OkResult("BIGINT")
    case ir.FloatType => OkResult("FLOAT")
    case ir.DoubleType => OkResult("DOUBLE")
    case ir.DecimalType(precision, scale) =>
      val arguments = precision.toSeq ++ scale.toSeq
      if (arguments.isEmpty) {
        OkResult("DECIMAL")
      } else {
        sql"DECIMAL${arguments.mkString("(", ", ", ")")}"
      }
    case ir.StringType => OkResult("STRING")
    case ir.DateType => OkResult("DATE")
    case ir.TimestampType => OkResult("TIMESTAMP")
    case ir.TimestampNTZType => OkResult("TIMESTAMP_NTZ")
    case ir.ArrayType(elementType) => sql"ARRAY<${generateDataType(ctx, elementType)}>"
    case ir.StructType(fields) =>
      val fieldTypes = fields
        .map { case ir.StructField(name, dataType, nullable, metadata) =>
          val isNullable = if (nullable) "" else " NOT NULL"
          sql"$name:${generateDataType(ctx, dataType)}$isNullable"
        }
        .mkSql(",")
      sql"STRUCT<$fieldTypes>"
    case ir.MapType(keyType, valueType) =>
      sql"MAP<${generateDataType(ctx, keyType)}, ${generateDataType(ctx, valueType)}>"
    case ir.VarcharType(size) => sql"VARCHAR${maybeSize(size)}"
    case ir.CharType(size) => sql"CHAR${maybeSize(size)}"
    case ir.VariantType => sql"VARIANT"
    case _ => PartialResult(s"!!! $dt !!!", ir.UnsupportedDataType(dt.toString))
  }

  private def maybeSize(size: Option[Int]): String = size.map(s => s"($s)").getOrElse("")
}
