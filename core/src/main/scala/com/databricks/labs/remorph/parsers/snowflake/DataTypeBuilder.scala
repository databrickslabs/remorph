package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.Data_typeContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._
object DataTypeBuilder {

  def buildDataType(ctx: Data_typeContext): ir.DataType = {
    val sizeOpt = Option(ctx.data_type_size()).map(_.num().getText.toInt)
    ctx match {
      case c if c.int_alias != null =>
        // see https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint
        ir.DecimalType(Some(38), None)
      case c if c.number_alias != null =>
        val nums = c.num().asScala
        val precision = nums.headOption.map(_.getText.toInt)
        val scale = nums.drop(1).headOption.map(_.getText.toInt)
        ir.DecimalType(precision, scale)
      case c if c.float_alias != null => ir.DoubleType()
      case c if c.BOOLEAN() != null => ir.BooleanType()
      case c if c.DATE() != null => ir.DateType()
      case c if c.char_alias != null => ir.CharType(sizeOpt)
      case c if c.varchar_alias != null => ir.VarCharType(sizeOpt)
      case c if c.binary_alias != null => ir.BinaryType()
      case c if c.ARRAY() != null => ir.ArrayType()
      case _ => ir.UnparsedType()
    }
  }

}
