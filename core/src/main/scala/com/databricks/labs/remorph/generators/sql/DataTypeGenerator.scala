package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

object DataTypeGenerator {

  def generateDataType(ctx: GeneratorContext, dt: ir.DataType): String = dt match {
    case ir.NullType => "VOID"
    case ir.BooleanType => "BOOLEAN"
    case ir.BinaryType => "BINARY"
    case ir.ShortType => "SMALLINT"
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
    case ir.StructType() => "STRUCT" // TODO fix this
    case ir.MapType(keyType, valueType) =>
      s"MAP<${generateDataType(ctx, keyType)}, ${generateDataType(ctx, valueType)}>"
  }

}
