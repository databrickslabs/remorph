package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

import scala.collection.JavaConverters._
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

  override def visitRanking_windowed_function(ctx: Ranking_windowed_functionContext): ir.Expression = {
    val windowFunction = buildWindowFunction(ctx)
    val overClause = Option(ctx.over_clause())
    val partitionSpec =
      overClause.flatMap(o => Option(o.partition_by())).map(buildPartitionSpec).getOrElse(Seq())
    val sortOrder =
      overClause.flatMap(o => Option(o.order_by_expr())).map(buildSortOrder).getOrElse(Seq())
    // dummy implementation because the grammar for this is missing
    // see https://github.com/databrickslabs/remorph/issues/258
    val frameSpec = ir.WindowFrame(
      frame_type = ir.RowsFrame,
      lower = ir.FrameBoundary(current_row = false, unbounded = true, value = ir.Noop),
      upper = ir.FrameBoundary(current_row = true, unbounded = false, value = ir.Noop))
    ir.Window(
      window_function = windowFunction,
      partition_spec = partitionSpec,
      sort_order = sortOrder,
      frame_spec = frameSpec)
  }

  private def buildWindowFunction(ctx: Ranking_windowed_functionContext): ir.Expression = {
    if (ctx.ROW_NUMBER() != null) {
      ir.RowNumber
    } else if (ctx.NTILE() != null) {
      val parameter = ctx.expr(0).accept(this)
      ir.NTile(parameter)
    } else {
      visitChildren(ctx)
    }
  }

  private def buildPartitionSpec(ctx: Partition_byContext): Seq[ir.Expression] = {
    ctx.expr_list().expr().asScala.map(_.accept(this))
  }

  private[snowflake] def buildSortOrder(ctx: Order_by_exprContext): Seq[ir.SortOrder] = {
    val exprList = ctx.expr_list_sorted()
    val exprs = exprList.expr().asScala
    val commas = exprList.COMMA().asScala.map(_.getSymbol.getStopIndex) :+ exprList.getStop.getStopIndex
    val descs = exprList.asc_desc().asScala.filter(_.DESC() != null).map(_.getStop.getStopIndex)

    // Lists returned by expr() and asc_desc() above may have different sizes
    // for example with `ORDER BY a, b DESC, c` (3 expr but only 1 asc_desc).
    // So we use the position of the asc_desc elements relative to the position of
    // commas in the ORDER BY expression to determine which expr is affected by each asc_desc
    exprs.zip(commas).map { case (expr, upperBound) =>
      val direction =
        descs
          .find(pos => pos > expr.getStop.getStopIndex && pos <= upperBound)
          .map(_ => ir.DescendingSortDirection)
          .getOrElse(ir.AscendingSortDirection)

      // no specification is available for nulls ordering, so defaulting to nulls last
      // see https://github.com/databrickslabs/remorph/issues/258
      ir.SortOrder(expr.accept(this), direction, ir.SortNullsLast)
    }
  }
}
