package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.TerminalNode

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * This class is responsible for building a Column object from various components of a TSql AST. It is used where the
 * context of the AST is a Full_column_nameContext.
 */
class TSqlColumnBuilder extends TSqlExpressionBuilder {

  override def visitExprDot(ctx: ExprDotContext): ir.Column = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)

    (left, right) match {

      // x.y
      case (c1: ir.Column, c2: ir.Column) =>
        ir.Column(c1.name + "." + c2.name)
      case _ => throw new IllegalArgumentException("Expected a Table and a Column")
    }
  }

  /**
   * This method is used to build components of a column reference from a TerminalNode. The Result is used higher up the
   * parse tree to construct a column reference.
   *
   * @param ctx
   *   the Id context to visit
   * @return
   *   the visited Column object
   */
  override def visitId_(ctx: Id_Context): ir.Expression = ctx match {
    case c if c.ID() != null => ir.Column(ctx.getText)
    case c if c.TEMP_ID() != null => ir.Column(ctx.getText)
    case c if c.DOUBLE_QUOTE_ID() != null => ir.Column(ctx.getText)
    case c if c.SQUARE_BRACKET_ID() != null => ir.Column(ctx.getText)
    case c if c.RAW() != null => ir.Column(ctx.getText)
    case _ => ir.UnresolvedExpression(ctx.getText)
  }

  override def visitSelectList(ctx: TSqlParser.SelectListContext): ir.Expression =
    ir.ExpressionList(ctx.selectListElem().asScala.toList.map(_.accept(this)))

  // TODO: A lot of work here for things that are not just simple x.y.z
  override def visitSelectListElem(ctx: TSqlParser.SelectListElemContext): ir.Expression =
    ctx.expressionElem.accept(this)

  override def visitFullTableName(ctx: FullTableNameContext): ir.Literal = {
    // Extract the components of the full table name, if they exist
    val linkedServer = Option(ctx.linkedServer).map(_.getText)
    val database = Option(ctx.database).map(_.getText)
    val schema = Option(ctx.schema).map(_.getText)
    val name = ctx.table.getText

    val unparsedIdentifier = List(linkedServer, database, schema, Some(name)).flatten.mkString(".")
    ir.Literal(string = Some(unparsedIdentifier))
  }

  override def visitFullColumnName(ctx: FullColumnNameContext): ir.Column = {
    val tableName = Option(ctx.fullTableName).map(_.accept(this) match {
      case nt: ir.Literal => nt.string
      case _ => ""
    })
    val columnName = ctx.id_.getText
    val fullColumnName = tableName.map(_ + "." + columnName).getOrElse(columnName)
    ir.Column(fullColumnName)
  }

  override def visitPrimitiveConstant(ctx: TSqlParser.PrimitiveConstantContext): ir.Expression = {
    if (ctx.DOLLAR != null) {
      return ir.Literal(string = Some(ctx.getText))
    }
    buildConstant(ctx.con)
  }

  override def visitTerminal(node: TerminalNode): ir.Expression = buildConstant(node.getSymbol)

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  private def buildConstant(con: Token): ir.Expression = con.getType match {
    case c if c == STRING => ir.Literal(string = Some(removeQuotes(con.getText)))
    case c if c == INT => ir.Literal(integer = Some(con.getText.toInt))
    case c if c == FLOAT => ir.Literal(float = Some(con.getText.toFloat))
    case c if c == HEX => ir.Literal(string = Some(con.getText)) // Preserve format for now
    case c if c == REAL => ir.Literal(double = Some(con.getText.toDouble))
    case c if c == NULL_ => ir.Literal(nullType = Some(ir.NullType()))
    case _ => ir.UnresolvedExpression(con.getText)
  }

  override def visitScNot(ctx: TSqlParser.ScNotContext): ir.Expression =
    ir.Not(ctx.searchCondition().accept(this))

  override def visitScAnd(ctx: TSqlParser.ScAndContext): ir.Expression =
    ir.And(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))

  override def visitScOr(ctx: TSqlParser.ScOrContext): ir.Expression =
    ir.Or(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))

  override def visitScPred(ctx: TSqlParser.ScPredContext): ir.Expression = ctx.predicate().accept(this)

  override def visitScPrec(ctx: TSqlParser.ScPrecContext): ir.Expression = ctx.searchCondition.accept(this)

  override def visitPredicate(ctx: TSqlParser.PredicateContext): ir.Expression = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)

    ctx.comparisonOperator match {
      case op if op.LT != null && op.EQ != null => ir.LesserThanOrEqual(left, right)
      case op if op.GT != null && op.EQ != null => ir.GreaterThanOrEqual(left, right)
      case op if op.LT != null && op.GT != null => ir.NotEquals(left, right)
      case op if op.EQ != null => ir.Equals(left, right)
      case op if op.GT != null => ir.GreaterThan(left, right)
      case op if op.LT != null => ir.LesserThan(left, right)
    }
  }
}
