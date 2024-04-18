package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

class SnowflakeExpressionBuilder extends SnowflakeParserBaseVisitor[ir.Expression] {

  override def visitSelect_list_elem(ctx: SnowflakeParser.Select_list_elemContext): ir.Expression = {
    if (ctx.column_elem() != null) {
      val column = ctx.column_elem().accept(this)
      if (ctx.as_alias() != null) {
        ctx.as_alias().accept(this) match {
          case ir.Alias(_, name, metadata) => ir.Alias(column, name, metadata)
          case _ => null
        }
      } else {
        column
      }
    } else if (ctx.expression_elem() != null) {
      ctx.expression_elem().accept(this)
    } else {
      null
    }
  }
  override def visitColumn_name(ctx: Column_nameContext): ir.Expression = {
    ir.Column(ctx.id_(0).getText)
  }

  override def visitAs_alias(ctx: As_aliasContext): ir.Expression = {
    val alias = ctx.alias().id_().getText
    ir.Alias(null, Seq(alias), None)
  }

  override def visitAggregate_function(ctx: Aggregate_functionContext): ir.Expression = {
    val param = ctx.expr_list().accept(this)
    val functionName = ctx.id_().builtin_function()
    if (functionName.COUNT() != null) {
      ir.Count(param)
    } else {
      null
    }
  }

  override def visitPrimitive_expression(ctx: Primitive_expressionContext): ir.Expression = {
    if (ctx.id_(0) != null) {
      val columnName = ctx.id_(0).getText
      ir.Column(columnName)
    } else {
      super.visitPrimitive_expression(ctx)
    }
  }

  override def visitOrder_item(ctx: Order_itemContext): ir.Expression = {
    val columnName = ctx.id_().getText
    ir.Column(columnName)
  }

  override def visitLiteral(ctx: LiteralContext): ir.Literal = {
    val sign = Option(ctx.sign()).map(_ => "-").getOrElse("")
    if (ctx.STRING() != null) {
      ir.Literal(string = Some(removeQuotes(ctx.STRING().getText)))
    } else if (ctx.DECIMAL() != null) {
      visitDecimal(sign + ctx.DECIMAL().getText)
    } else if (ctx.FLOAT() != null) {
      visitDecimal(sign + ctx.FLOAT().getText)
    } else if (ctx.REAL() != null) {
      visitDecimal(sign + ctx.REAL().getText)
    } else if (ctx.true_false() != null) {
      visitTrue_false(ctx.true_false())
    } else if (ctx.NULL_() != null) {
      ir.Literal(nullType = Some(ir.NullType()))
    } else {
      ir.Literal(nullType = Some(ir.NullType()))
    }
  }

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
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

  override def visitExpr(ctx: ExprContext): ir.Expression = {

    if (ctx.AND() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.And(left, right)
    } else if (ctx.OR() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.Or(left, right)
    } else if (ctx.comparison_operator() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      buildComparisonExpression(ctx.comparison_operator(), left, right)
    } else {
      visitChildren(ctx)
    }
  }

  private def buildComparisonExpression(
      op: Comparison_operatorContext,
      left: ir.Expression,
      right: ir.Expression): ir.Expression = {
    if (op.EQ() != null) {
      ir.Equals(left, right)
    } else if (op.NE() != null || op.LTGT() != null) {
      ir.NotEquals(left, right)
    } else if (op.GT() != null) {
      ir.GreaterThan(left, right)
    } else if (op.LT() != null) {
      ir.LesserThan(left, right)
    } else if (op.GE() != null) {
      ir.GreaterThanOrEqual(left, right)
    } else if (op.LE() != null) {
      ir.LesserThanOrEqual(left, right)
    } else {
      visitChildren(op)
    }
  }

  override def visitSearch_condition(ctx: Search_conditionContext): ir.Expression = {
    val pred = ctx.predicate().accept(this)
    // TODO: investigate why NOT() is a list here
    if (ctx.NOT().size() > 0) {
      ir.Not(pred)
    } else {
      pred
    }
  }

}
