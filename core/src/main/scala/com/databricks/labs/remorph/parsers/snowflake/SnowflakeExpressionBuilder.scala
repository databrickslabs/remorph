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
    val columnName = ctx.id_(0).getText
    ir.Column(columnName)
  }

  override def visitOrder_item(ctx: Order_itemContext): ir.Expression = {
    val columnName = ctx.id_().getText
    ir.Column(columnName)
  }
}
