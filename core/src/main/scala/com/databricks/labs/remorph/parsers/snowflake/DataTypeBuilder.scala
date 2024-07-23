package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.DataTypeContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._
object DataTypeBuilder {

  def buildDataType(ctx: DataTypeContext): ir.DataType = {
    val sizeOpt = Option(ctx.dataTypeSize()).map(_.num().getText.toInt)
    ctx match {
      case c if c.intAlias != null =>
        // see
        // https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint
        ir.DecimalType(Some(38), None)
      case c if c.numberAlias != null =>
        val nums = c.num().asScala
        val precision = nums.headOption.map(_.getText.toInt)
        val scale = nums.drop(1).headOption.map(_.getText.toInt)
        ir.DecimalType(precision, scale)
      case c if c.floatAlias != null => ir.DoubleType
      case c if c.BOOLEAN() != null => ir.BooleanType
      case c if c.DATE() != null => ir.DateType
      case c if c.charAlias != null => ir.CharType(sizeOpt)
      case c if c.varcharAlias != null => ir.VarCharType(sizeOpt)
      case c if c.binaryAlias != null => ir.BinaryType
      case c if c.ARRAY() != null => ir.ArrayType(ir.UnresolvedType)
      case _ => ir.UnparsedType()
    }
  }

}
