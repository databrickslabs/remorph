package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import com.databricks.labs.remorph.parsers.intermediate.{Column, Expression, Literal}
import org.antlr.v4.runtime.tree.TerminalNode
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

import scala.collection.JavaConverters._

class TSqlExpressionBuilder
    extends TSqlParserBaseVisitor[Expression]
    with ParserCommon
    with IncompleteParser[ir.Expression] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitSelect_list_elem(ctx: Select_list_elemContext): Expression = ctx.expression_elem().accept(this)

  override def visitExpression(ctx: ExpressionContext): Expression = ctx match {
    case c if c.full_column_name() != null => c.full_column_name().accept(this)
    case c if c.primitive_expression() != null => c.primitive_expression().accept(this)
  }

  override def visitFull_column_name(ctx: Full_column_nameContext): Expression = {
    val columnName = ctx.id_.getText
    Column(columnName)
  }

  override def visitPrimitive_constant(ctx: Primitive_constantContext): Expression = ctx match {
    case c if c.DOLLAR() != null => wrapUnresolvedInput(ctx.getText)
    case c if c.STRING() != null => c.STRING().accept(this)
    case c if c.INT() != null => c.INT().accept(this)
    case c if c.FLOAT() != null => c.FLOAT().accept(this)
    case c if c.HEX() != null => c.HEX().accept(this)
    case c if c.REAL() != null => c.REAL().accept(this)
  }

  override def visitTerminal(node: TerminalNode): Expression = node.getSymbol.getType match {
    case c if c == STRING => Literal(string = Some(node.getText))
    case c if c == INT => Literal(integer = Some(node.getText.toInt))
    case c if c == FLOAT => Literal(float = Some(node.getText.toFloat))
    case c if c == HEX => Literal(string = Some(node.getText)) // Preserve format for now
    case c if c == REAL => Literal(double = Some(node.getText.toDouble))
    case _ => wrapUnresolvedInput(node.getText)
  }
  override def visitSearch_condition(ctx: Search_conditionContext): Expression = {
    if (ctx.search_condition().size() > 1) {
      val conditions = ctx.search_condition().asScala.map(_.accept(this))
      conditions.reduce((left, right) =>
        ctx match {
          case c if c.AND() != null => ir.And(left, right)
          case c if c.OR() != null => ir.Or(left, right)
          case c if c.NOT() != null => ir.Not(left)
        })
    } else {

      if (!ctx.NOT().isEmpty) {

        ir.Not(ctx.predicate().accept(this))
      } else {
        ctx.predicate().accept(this)
      }
    }

  }

  override def visitPredicate(ctx: PredicateContext): Expression = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)
    ctx.comparison_operator().getText match {
      case "=" => ir.Equals(left, right)
      case "!=" => ir.NotEquals(left, right)
      case ">" => ir.GreaterThan(left, right)
      case "<" => ir.LesserThan(left, right)
      case ">=" => ir.GreaterThanOrEqual(left, right)
      case "<=" => ir.LesserThanOrEqual(left, right)
    }
  }
}
