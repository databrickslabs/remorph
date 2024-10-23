package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{OkResult, PartialResult, RemorphContext, TBAS, intermediate => ir}

/**
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/sql-ref-datatypes.html
 */
object DataTypeGenerator extends TBAS[RemorphContext]{

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): SQL = dt match {
    case ir.NullType => lift(OkResult("VOID"))
    case ir.BooleanType => lift(OkResult("BOOLEAN"))
    case ir.BinaryType => lift(OkResult("BINARY"))
    case ir.ShortType => lift(OkResult("SMALLINT"))
    case ir.TinyintType => lift(OkResult("TINYINT"))
    case ir.IntegerType => lift(OkResult("INT"))
    case ir.LongType => lift(OkResult("BIGINT"))
    case ir.FloatType => lift(OkResult("FLOAT"))
    case ir.DoubleType => lift(OkResult("DOUBLE"))
    case ir.DecimalType(precision, scale) =>
      val arguments = precision.toSeq ++ scale.toSeq
      if (arguments.isEmpty) {
        lift(OkResult("DECIMAL"))
      } else {
        sql"DECIMAL${arguments.mkString("(", ", ", ")")}"
      }
    case ir.StringType => lift(OkResult("STRING"))
    case ir.DateType => lift(OkResult("DATE"))
    case ir.TimestampType => lift(OkResult("TIMESTAMP"))
    case ir.TimestampNTZType => lift(OkResult("TIMESTAMP_NTZ"))
    case ir.ArrayType(elementType) => sql"ARRAY<${generateDataType(ctx, elementType)}>"
    case ir.StructType(fields) =>
      val fieldTypes = fields
        .map { case ir.StructField(name, dataType, nullable, _) =>
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
    case _ => lift(PartialResult(s"!!! $dt !!!", ir.UnsupportedDataType(dt.toString)))
  }

  private def maybeSize(size: Option[Int]): String = size.map(s => s"($s)").getOrElse("")
}
