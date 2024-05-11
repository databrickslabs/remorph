package com.databricks.labs.remorph.parsers.tsql

import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.TerminalNode
import com.databricks.labs.remorph.parsers.intermediate.{Column, Expression, Literal}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}

import scala.collection.JavaConverters._
import scala.collection.convert.ImplicitConversions.`collection AsScalaIterable`

class TSqlExpressionBuilder
    extends TSqlParserBaseVisitor[ir.Expression]
    with ParserCommon
    with IncompleteParser[ir.Expression] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitFullColumnName(ctx: FullColumnNameContext): ir.Expression = {
    Column(ctx.id.getText)
  }

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

  override def visitExprFunc(ctx: ExprFuncContext): Expression = ctx.functionCall.accept(new TSqlFunctionBuilder)

  override def visitExpressionList(ctx: ExpressionListContext): ir.ExpressionList =
    ir.ExpressionList(ctx.expression().toList.map(_.accept(this).asInstanceOf[ir.Expression]))

  override def visitPrimitiveConstant(ctx: PrimitiveConstantContext): ir.Expression = ctx match {
    case c if c.DOLLAR() != null => wrapUnresolvedInput(ctx.getText)
    case c if c.STRING() != null => c.STRING().accept(this)
    case c if c.INT() != null => c.INT().accept(this)
    case c if c.FLOAT() != null => c.FLOAT().accept(this)
    case c if c.HEX() != null => c.HEX().accept(this)
    case c if c.REAL() != null => c.REAL().accept(this)
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

  override def visitSearchCondition(ctx: SearchConditionContext): ir.Expression = {
    if (ctx.searchCondition().size() > 1) {
      val conditions = ctx.searchCondition().asScala.map(_.accept(this))
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

  override def visitPredicate(ctx: PredicateContext): ir.Expression = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)
    ctx.comparisonOperator().getText match {
      case "=" => ir.Equals(left, right)
      case "!=" => ir.NotEquals(left, right)
      case ">" => ir.GreaterThan(left, right)
      case "<" => ir.LesserThan(left, right)
      case ">=" => ir.GreaterThanOrEqual(left, right)
      case "<=" => ir.LesserThanOrEqual(left, right)
    }
  }
}
