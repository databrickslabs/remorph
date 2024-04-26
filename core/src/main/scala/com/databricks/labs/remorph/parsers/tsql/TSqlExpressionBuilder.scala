package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.{Column, Expression}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

class TSqlExpressionBuilder extends TSqlParserBaseVisitor[Expression] {

  override def visitSelect_list_elem(ctx: Select_list_elemContext): Expression = ctx.expression_elem().accept(this)

  override def visitExpression(ctx: ExpressionContext): Expression = {
    ctx match {
      case c if c.full_column_name() != null => c.full_column_name().accept(this)
    }
  }

  override def visitFull_column_name(ctx: Full_column_nameContext): Expression = {
    val columnName = ctx.id_.getText
    Column(columnName)
  }
}
