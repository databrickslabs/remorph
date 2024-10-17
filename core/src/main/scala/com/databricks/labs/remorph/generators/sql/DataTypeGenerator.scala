package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{Failure, Result, Success, WorkflowStage, intermediate => ir}

/**
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/sql-ref-datatypes.html
 */
object DataTypeGenerator {

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): Result[String] = dt match {
    case ir.NullType => Success("VOID")
    case ir.BooleanType => Success("BOOLEAN")
    case ir.BinaryType => Success("BINARY")
    case ir.ShortType => Success("SMALLINT")
    case ir.TinyintType => Success("TINYINT")
    case ir.IntegerType => Success("INT")
    case ir.LongType => Success("BIGINT")
    case ir.FloatType => Success("FLOAT")
    case ir.DoubleType => Success("DOUBLE")
    case ir.DecimalType(precision, scale) =>
      val arguments = precision.toSeq ++ scale.toSeq
      if (arguments.isEmpty) {
        Success("DECIMAL")
      } else {
        sql"DECIMAL${arguments.mkString("(", ", ", ")")}"
      }
    case ir.StringType => Success("STRING")
    case ir.DateType => Success("DATE")
    case ir.TimestampType => Success("TIMESTAMP")
    case ir.TimestampNTZType => Success("TIMESTAMP_NTZ")
    case ir.ArrayType(elementType) => sql"ARRAY<${generateDataType(ctx, elementType)}>"
    case ir.StructType(fields) =>
      val fieldTypes = fields
        .map { case ir.StructField(name, dataType, nullable) =>
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
    case _ => Failure(WorkflowStage.GENERATE, ir.UnsupportedDataType(dt))
  }

  private def maybeSize(size: Option[Int]): String = size.map(s => s"($s)").getOrElse("")
}
