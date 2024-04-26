package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import com.databricks.labs.remorph.parsers.intermediate.{Column, Expression, Literal}
import org.antlr.v4.runtime.tree.TerminalNode
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

class TSqlExpressionBuilder
    extends TSqlParserBaseVisitor[Expression]
    with ParserCommon
    with IncompleteParser[ir.Expression] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitSelect_list_elem(ctx: Select_list_elemContext): Expression = ctx.expression_elem().accept(this)

  override def visitExpression(ctx: ExpressionContext): Expression = {
    ctx match {
      case c if c.full_column_name() != null => c.full_column_name().accept(this)
      case c if c.primitive_expression() != null => c.primitive_expression().accept(this)
    }
  }

  override def visitFull_column_name(ctx: Full_column_nameContext): Expression = {
    val columnName = ctx.id_.getText
    Column(columnName)
  }

  override def visitPrimitive_constant(ctx: Primitive_constantContext): Expression = {

    ctx match {
      case c if c.DOLLAR() != null => wrapUnresolvedInput(ctx.getText)
      case c if c.STRING() != null => c.STRING().accept(this)
      case c if c.INT() != null => c.INT().accept(this)
      case c if c.FLOAT() != null => c.FLOAT() accept (this)
      case c if c.HEX() != null => c.HEX() accept (this)
      case c if c.REAL() != null => c.REAL() accept (this)
    }
  }

  override def visitTerminal(node: TerminalNode): Expression = {
    val sym = node.getSymbol
    sym.getType match {
      case c if c == STRING => Literal(string = Some(node.getText))
      case c if c == INT => Literal(integer = Some(node.getText.toInt))
      case c if c == FLOAT => Literal(float = Some(node.getText.toFloat))
      case c if c == HEX => Literal(hex = Some(node.getText))
      case c if c == REAL => Literal(real = Some(node.getText))
      case _ => wrapUnresolvedInput(node.getText)
    }
  }
}
