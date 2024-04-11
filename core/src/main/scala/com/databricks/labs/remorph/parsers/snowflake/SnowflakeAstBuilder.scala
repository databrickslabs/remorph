package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder extends SnowflakeParserBaseVisitor[AnyRef] with ParserCommon {
  override def visitLiteral(ctx: LiteralContext): ir.Literal = if (ctx.STRING() != null) {
    ir.Literal(string = Some(ctx.STRING().getText))
  } else if (ctx.DECIMAL != null) {
    visitDecimal(ctx.DECIMAL.getText)
  } else if (ctx.true_false() != null) {
    visitTrue_false(ctx.true_false())
  } else if (ctx.NULL_() != null) {
    ir.Literal(nullType = Some(ir.NullType()))
  } else {
    ir.Literal(nullType = Some(ir.NullType()))
  }

  override def visitTrue_false(ctx: True_falseContext): ir.Literal = ctx.TRUE() match {
    case null => ir.Literal(boolean = Some(false))
    case _ => ir.Literal(boolean = Some(true))
  }

  private def visitDecimal(decimal: String) = BigDecimal(decimal) match {
    case d if d.isValidInt => ir.Literal(integer = Some(d.toInt))
    case d if d.isValidLong => ir.Literal(long = Some(d.toLong))
    case d if d.isValidShort => ir.Literal(short = Some(d.toShort))
    case d if d.isDecimalFloat || d.isExactFloat => ir.Literal(float = Some(d.toFloat))
    case d if d.isDecimalDouble || d.isExactDouble => ir.Literal(double = Some(d.toDouble))
    case _ => ir.Literal(decimal = Some(ir.Decimal(decimal, None, None)))
  }
}
