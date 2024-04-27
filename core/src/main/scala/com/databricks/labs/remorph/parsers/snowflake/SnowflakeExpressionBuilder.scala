package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{ParserCommon, IncompleteParser, intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

import scala.collection.JavaConverters._
class SnowflakeExpressionBuilder
    extends SnowflakeParserBaseVisitor[ir.Expression]
    with ParserCommon
    with IncompleteParser[ir.Expression] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)
  override def visitSelect_list_elem(ctx: Select_list_elemContext): ir.Expression = {
    val rawExpression = ctx match {
      case c if c.column_elem() != null => c.column_elem().accept(this)
      case c if c.expression_elem() != null => c.expression_elem().accept(this)
      case c if c.column_elem_star() != null => c.column_elem_star().accept(this)
    }
    buildAlias(ctx.as_alias(), rawExpression)
  }

  override def visitColumn_elem_star(ctx: Column_elem_starContext): ir.Expression = {
    ir.Star(Option(ctx.object_name_or_alias()).map {
      case c if c.object_name() != null => c.object_name().getText
      case c if c.alias() != null => c.alias().id_().getText
    })
  }

  private def buildAlias(ctx: As_aliasContext, input: ir.Expression): ir.Expression =
    Option(ctx).fold(input) { c =>
      val alias = c.alias().id_().getText
      ir.Alias(input, Seq(alias), None)
    }
  override def visitColumn_name(ctx: Column_nameContext): ir.Expression = {
    ir.Column(ctx.id_(0).getText)
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

  override def visitExpr(ctx: ExprContext): ir.Expression = ctx match {
    case c if c.AND() != null =>
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.And(left, right)
    case c if c.OR() != null =>
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.Or(left, right)
    case c if c.comparison_operator() != null =>
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      buildComparisonExpression(ctx.comparison_operator(), left, right)
    case c if c.over_clause() != null =>
      val windowFunction = c.expr(0).accept(this)
      buildWindow(c.over_clause(), windowFunction)
    case c => visitChildren(c)

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
    if (ctx.NOT().size() % 2 == 1) {
      ir.Not(pred)
    } else {
      pred
    }
  }

  override def visitRanking_windowed_function(ctx: Ranking_windowed_functionContext): ir.Expression = {
    val windowFunction = buildWindowFunction(ctx)
    buildWindow(ctx.over_clause(), windowFunction)
  }

  private def buildWindow(ctx: Over_clauseContext, windowFunction: ir.Expression): ir.Expression = {
    val overClause = Option(ctx)
    val partitionSpec =
      overClause.flatMap(o => Option(o.partition_by())).map(buildPartitionSpec).getOrElse(Seq())
    val sortOrder =
      overClause.flatMap(o => Option(o.order_by_expr())).map(buildSortOrder).getOrElse(Seq())

    ir.Window(
      window_function = windowFunction,
      partition_spec = partitionSpec,
      sort_order = sortOrder,
      frame_spec = DummyWindowFrame)
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

  override def visitAggregate_function(ctx: Aggregate_functionContext): ir.Expression = {
    val param = ctx.expr_list().expr(0).accept(this)
    buildBuiltinFunction(ctx.id_().builtin_function(), param)
  }

  private def buildBuiltinFunction(ctx: Builtin_functionContext, param: ir.Expression): ir.Expression =
    Option(ctx)
      .collect {
        case c if c.AVG() != null => ir.Avg(param)
        case c if c.SUM() != null => ir.Sum(param)
        case c if c.MIN() != null => ir.Min(param)
        case c if c.COUNT() != null => ir.Count(param)
      }
      .getOrElse(param)

  override def visitCase_expression(ctx: Case_expressionContext): ir.Expression = {
    val exprs = ctx.expr().asScala
    val otherwise = Option(ctx.ELSE()).flatMap(els => exprs.find(occursBefore(els, _)).map(_.accept(this)))
    ctx match {
      case c if c.switch_section().size() > 0 =>
        val expression = exprs.find(occursBefore(_, ctx.switch_section(0))).map(_.accept(this))
        val branches = c.switch_section().asScala.map { branch =>
          ir.WhenBranch(branch.expr(0).accept(this), branch.expr(1).accept(this))
        }
        ir.Case(expression, branches, otherwise)
      case c if c.switch_search_condition_section().size() > 0 =>
        val branches = c.switch_search_condition_section().asScala.map { branch =>
          ir.WhenBranch(branch.search_condition().accept(this), branch.expr().accept(this))
        }
        ir.Case(None, branches, otherwise)
    }
  }
  override def visitPredicate(ctx: PredicateContext): ir.Expression = {

    val predicate = ctx match {
      case c if c.EXISTS() != null =>
        ir.Exists(c.subquery().accept(new SnowflakeRelationBuilder))
      case c if c.IN() != null =>
        ir.IsIn(c.subquery().accept(new SnowflakeRelationBuilder), c.expr(0).accept(this))
      case c if c.BETWEEN() != null =>
        val expression = c.expr(0).accept(this)
        val lowerBound = c.expr(1).accept(this)
        val upperBound = c.expr(2).accept(this)
        ir.And(ir.GreaterThanOrEqual(expression, lowerBound), ir.LesserThanOrEqual(expression, upperBound))
      case c if c.LIKE() != null || c.ILIKE() != null =>
        val expression = c.expr(0).accept(this)
        val patterns = if (c.ANY() != null) {
          c.expr()
            .asScala
            .filter(e => occursBefore(c.LR_BRACKET(), e) && occursBefore(e, c.RR_BRACKET()))
            .map(_.accept(this)) _
        } else {
          Seq(c.expr(1).accept(this))
        }
        val escape = Option(c.ESCAPE())
          .flatMap(_ =>
            c.expr()
              .asScala
              .find(occursBefore(c.ESCAPE(), _))
              .map(_.accept(this)))
        ir.Like(expression, patterns, escape, c.LIKE() != null)
      case c if c.RLIKE() != null =>
        val expression = c.expr(0).accept(this)
        val pattern = c.expr(1).accept(this)
        ir.RLike(expression, pattern)
      case c if c.IS() != null =>
        val isNull: ir.Expression = ir.IsNull(c.expr(0).accept(this))
        Option(c.null_not_null().NOT()).fold(isNull)(_ => ir.Not(isNull))
      case c => visitChildren(c)
    }
    Option(ctx.NOT()).fold(predicate)(_ => ir.Not(predicate))
  }
}
