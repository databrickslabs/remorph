package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.DataTypeContext
import com.databricks.labs.remorph.{intermediate => ir}

class DataTypeBuilder {

  def build(ctx: DataTypeContext): ir.DataType = {
    ctx.dataTypeIdentity() match {
      case context: TSqlParser.DataTypeIdentityContext => buildIdentity(context)
      case _ => buildScalar(ctx)
    }
  }

  private def buildScalar(ctx: DataTypeContext): ir.DataType = {

    val lenOpt = Option(ctx.INT(0)) map (_.getText.toInt) // A single length parameter
    val scaleOpt = Option(ctx.INT(1)) map (_.getText.toInt) // A single scale parameter

    val typeDefinition = ctx.id().getText
    typeDefinition.toLowerCase() match {
      case "tinyint" => ir.ByteType(size = Some(1))
      case "smallint" => ir.ShortType
      case "int" => ir.IntegerType
      case "bigint" => ir.LongType
      case "bit" => ir.BooleanType
      case "money" => ir.DecimalType(precision = Some(19), scale = Some(4)) // Equivalent money
      case "smallmoney" => ir.DecimalType(precision = Some(10), scale = Some(4)) // Equivalent smallmoney
      case "float" => ir.FloatType
      case "real" => ir.DoubleType
      case "date" => ir.DateType
      case "time" => ir.TimeType
      case "datetime" => ir.TimestampType
      case "datetime2" => ir.TimestampType
      case "datetimeoffset" => ir.StringType // TODO: No direct equivalent
      case "smalldatetime" => ir.TimestampType // Equivalent smalldatetime
      case "char" => ir.CharType(size = lenOpt)
      case "varchar" => ir.VarcharType(size = lenOpt)
      case "nchar" => ir.CharType(size = lenOpt)
      case "nvarchar" => ir.VarcharType(size = lenOpt)
      case "text" => ir.VarcharType(None)
      case "ntext" => ir.VarcharType(None)
      case "image" => ir.BinaryType
      case "decimal" | "numeric" => ir.DecimalType(precision = lenOpt, scale = scaleOpt) // Equivalent decimal
      case "binary" => ir.BinaryType
      case "varbinary" => ir.BinaryType
      case "json" => ir.VarcharType(None)
      case "uniqueidentifier" => ir.VarcharType(size = Some(16)) // Equivalent uniqueidentifier
      case _ => ir.UnparsedType(typeDefinition)
    }
  }

  private def buildIdentity(ctx: TSqlParser.DataTypeIdentityContext): ir.DataType =
    // As of right now, there is no way to implement the IDENTITY property declared as a column type in TSql
    ir.UnparsedType(ctx.getText)

}
