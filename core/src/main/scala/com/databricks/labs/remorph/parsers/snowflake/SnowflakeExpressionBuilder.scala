package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

class SnowflakeExpressionBuilder extends SnowflakeParserBaseVisitor[ir.Expression] {

  override def visitSelect_list_elem(ctx: Select_list_elemContext): ir.Expression = {
    val column = ctx.column_elem().accept(this)
    if (ctx.as_alias() != null) {
      ctx.as_alias().accept(this) match {
        case ir.Alias(_, name, metadata) => ir.Alias(column, name, metadata)
        case _ => null
      }
    } else {
      column
    }
  }
  override def visitColumn_name(ctx: Column_nameContext): ir.Expression = {
    ir.Column(ctx.id_(0).getText)
  }

  override def visitAs_alias(ctx: As_aliasContext): ir.Expression = {
    val alias = ctx.alias().id_().getText
    ir.Alias(null, Seq(alias), None)
  }

  override def visitPrimitive_expression(ctx: Primitive_expressionContext): ir.Expression = {
    val columnName = ctx.id_(0).getText
    ir.Column(columnName)
  }
}
