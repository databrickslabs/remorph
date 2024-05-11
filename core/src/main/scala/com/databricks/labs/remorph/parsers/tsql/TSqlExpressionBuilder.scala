package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.Identifier
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.TerminalNode

class TSqlExpressionBuilder extends TSqlParserBaseVisitor[ir.Expression] with ParserCommon {

  /**
   * Expression precedence as defined by parenthesis
   *
   * @param ctx
   *   the ExprPrecedenceContext to visit, which contains the expression to which precedence is applied
   * @return
   *   the visited expression in IR
   *
   * Note that precedence COULD be explicitly placed in the AST here. If we wish to construct an exact replication of
   * expression source code from the AST, we need to know that the () were there. Redundant parens are otherwise elided
   * and the generated code may seem to be incorrect in the eyes of the customer, even though it will be logically
   * equivalent.
   */
  override def visitExprPrecedence(ctx: ExprPrecedenceContext): ir.Expression = {
    ctx.expression().accept(this)
  }

  override def visitExprBitNot(ctx: ExprBitNotContext): ir.Expression = {
    ir.BitwiseNot(ctx.expression().accept(this))
  }

  // Note that while we could evaluate the unary expression if it is a numeric
  // constant, it is usually better to be explicit about the unary operation as
  // if people use -+-42 then maybe they have a reason.
  override def visitExprUnary(ctx: ExprUnaryContext): ir.Expression = ctx.op.getType match {
    case MINUS => ir.UMinus(ctx.expression().accept(this))
    case PLUS => ir.UPlus(ctx.expression().accept(this))
  }

  override def visitExprOpPrec1(ctx: ExprOpPrec1Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec2(ctx: ExprOpPrec2Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec3(ctx: ExprOpPrec3Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec4(ctx: ExprOpPrec4Context): ir.Expression = {
    buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprDot(ctx: ExprDotContext): ir.Expression = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)
    ir.Dot(left, right)
  }

  override def visitPrimitiveConstant(ctx: TSqlParser.PrimitiveConstantContext): ir.Expression = {
    if (ctx.DOLLAR != null) {
      return ir.Literal(string = Some(ctx.getText))
    }
    buildConstant(ctx.con)
  }

  private def buildConstant(con: Token): ir.Expression = con.getType match {
    case c if c == STRING => ir.Literal(string = Some(removeQuotes(con.getText)))
    case c if c == INT => ir.Literal(integer = Some(con.getText.toInt))
    case c if c == FLOAT => ir.Literal(float = Some(con.getText.toFloat))
    case c if c == HEX => ir.Literal(string = Some(con.getText)) // Preserve format for now
    case c if c == REAL => ir.Literal(double = Some(con.getText.toDouble))
    case c if c == NULL_ => ir.Literal(nullType = Some(ir.NullType()))
  }

  override def visitId_(ctx: Id_Context): ir.Expression = ctx match {
    case c if c.ID() != null => Identifier(ctx.getText, isQuoted = false)
    case c if c.TEMP_ID() != null => Identifier(ctx.getText, isQuoted = false)
    case c if c.DOUBLE_QUOTE_ID() != null => Identifier(ctx.getText, isQuoted = true)
    case c if c.SQUARE_BRACKET_ID() != null => Identifier(ctx.getText, isQuoted = true)
    case c if c.RAW() != null => Identifier(ctx.getText, isQuoted = false)
    case _ => Identifier(ctx.getText, isQuoted = false)
  }

  override def visitTerminal(node: TerminalNode): ir.Expression = buildConstant(node.getSymbol)

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
    }
}
