package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.{Result, WorkflowStage, intermediate => ir}

/**
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/sql-ref-datatypes.html
 */
object DataTypeGenerator {

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): Result[String] = dt match {
    case ir.NullType => Result.Success("VOID")
    case ir.BooleanType => Result.Success("BOOLEAN")
    case ir.BinaryType => Result.Success("BINARY")
    case ir.ShortType => Result.Success("SMALLINT")
    case ir.TinyintType => Result.Success("TINYINT")
    case ir.IntegerType => Result.Success("INT")
    case ir.LongType => Result.Success("BIGINT")
    case ir.FloatType => Result.Success("FLOAT")
    case ir.DoubleType => Result.Success("DOUBLE")
    case ir.DecimalType(precision, scale) =>
      val arguments = precision.toSeq ++ scale.toSeq
      if (arguments.isEmpty) {
        Result.Success("DECIMAL")
      } else {
        sql"DECIMAL${arguments.mkString("(", ", ", ")")}"
      }
    case ir.StringType => Result.Success("STRING")
    case ir.DateType => Result.Success("DATE")
    case ir.TimestampType => Result.Success("TIMESTAMP")
    case ir.TimestampNTZType => Result.Success("TIMESTAMP_NTZ")
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
    case _ => Result.Failure(WorkflowStage.GENERATE, ir.UnsupportedDataType(dt))
  }

  private def maybeSize(size: Option[Int]): String = size.map(s => s"($s)").getOrElse("")
}
