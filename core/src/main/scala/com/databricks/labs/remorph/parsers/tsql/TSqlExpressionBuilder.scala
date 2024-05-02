package com.databricks.labs.remorph.parsers.tsql

import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.TerminalNode

import com.databricks.labs.remorph.parsers.intermediate.{Column, Literal}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

class TSqlExpressionBuilder
    extends TSqlParserBaseVisitor[ir.Expression]
    with ParserCommon
    with IncompleteParser[ir.Expression] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitFull_column_name(ctx: Full_column_nameContext): ir.Expression = {
    Column(ctx.id_.getText)
  }

  // This is merely a placeholder until the grammar can be fixed. It ensures that the
  // precedence expression is correctly handled
  override def visitBracket_expression(ctx: Bracket_expressionContext): ir.Expression = {
    ctx.expression().accept(this)
  }

  override def visitExpr_op_prec_1(ctx: Expr_op_prec_1Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExpr_op_prec_2(ctx: Expr_op_prec_2Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitPrimitive_constant(ctx: Primitive_constantContext): ir.Expression = ctx match {
    case c if c.DOLLAR() != null => wrapUnresolvedInput(ctx.getText)
    case c if c.STRING() != null => c.STRING().accept(this)
    case c if c.INT() != null => c.INT().accept(this)
    case c if c.FLOAT() != null => c.FLOAT() accept (this)
    case c if c.HEX() != null => c.HEX() accept (this)
    case c if c.REAL() != null => c.REAL() accept (this)
  }

  override def visitTerminal(node: TerminalNode): ir.Expression = node.getSymbol.getType match {
    case c if c == STRING => Literal(string = Some(removeQuotes(node.getText)))
    case c if c == INT => Literal(integer = Some(node.getText.toInt))
    case c if c == FLOAT => Literal(float = Some(node.getText.toFloat))
    case c if c == HEX => Literal(string = Some(node.getText)) // Preserve format for now
    case c if c == REAL => Literal(double = Some(node.getText.toDouble))
    case c if c == NULL_ => Literal(nullType = Some(ir.NullType()))
    case _ => wrapUnresolvedInput(node.getText)
  }

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  private def buildBinaryExpression(left: ir.Expression, right: ir.Expression, operator: Token): ir.Expression =
    operator.getType match {
      case STAR => ir.Multiply(left, right)
      case DIV => ir.Divide(left, right)
      case MOD => ir.Mod(left, right)
      case PLUS => ir.Add(left, right)
      case MINUS => ir.Subtract(left, right)
      case BIT_AND => ir.BitwiseAnd(left, right)
      case BIT_XOR => ir.BitwiseXor(left, right)
      case BIT_OR => ir.BitwiseOr(left, right)
      case DOUBLE_BAR => ir.Concat(left, right)
      case _ => ir.UnresolvedOperator(s"Unsupported operator: ${operator.getText}")
    }
}
