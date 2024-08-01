package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.UnresolvedType
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.Token

import java.time.{LocalDateTime, ZoneOffset}
import java.time.format.DateTimeFormatter
import scala.collection.JavaConverters._
import scala.util.Try

class SnowflakeExpressionBuilder()
    extends SnowflakeParserBaseVisitor[ir.Expression]
    with ParserCommon[ir.Expression]
    with IncompleteParser[ir.Expression] {

  private val functionBuilder = new SnowflakeFunctionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitId(ctx: IdContext): ir.Id = ctx match {
    case c if c.DOUBLE_QUOTE_ID() != null =>
      val idValue = c.getText.trim.stripPrefix("\"").stripSuffix("\"").replaceAll("\"\"", "\"")
      ir.Id(idValue, caseSensitive = true)
    case id => ir.Id(id.getText)
  }

  override def visitSelectListElem(ctx: SelectListElemContext): ir.Expression = {
    val rawExpression = ctx match {
      case c if c.columnElem() != null => c.columnElem().accept(this)
      case c if c.expressionElem() != null => c.expressionElem().accept(this)
      case c if c.columnElemStar() != null => c.columnElemStar().accept(this)
    }
    buildAlias(ctx.asAlias(), rawExpression)
  }

  override def visitColumnElem(ctx: ColumnElemContext): ir.Expression = {
    val objectNameIds = Option(ctx.objectName()).map(_.id().asScala.map(visitId)).getOrElse(Seq())
    val columnIds = ctx.columnName().id().asScala.map(visitId)
    val fqn = objectNameIds ++ columnIds
    val objectRefIds = fqn.take(fqn.size - 1)
    val objectRef = if (objectRefIds.isEmpty) {
      None
    } else {
      Some(ir.ObjectReference(objectRefIds.head, objectRefIds.tail: _*))
    }
    ir.Column(objectRef, fqn.last)
  }

  override def visitObjectName(ctx: ObjectNameContext): ir.ObjectReference = {
    val ids = ctx.id().asScala.map(visitId)
    ir.ObjectReference(ids.head, ids.tail: _*)
  }

  override def visitColumnElemStar(ctx: ColumnElemStarContext): ir.Expression = {
    ir.Star(Option(ctx.objectName()).map { on =>
      val objectNameIds = on.id().asScala.map(visitId)
      ir.ObjectReference(objectNameIds.head, objectNameIds.tail: _*)
    })
  }

  private def buildAlias(ctx: AsAliasContext, input: ir.Expression): ir.Expression =
    Option(ctx).fold(input) { c =>
      val alias = visitId(c.alias().id())
      ir.Alias(input, Seq(alias), None)
    }
  override def visitColumnName(ctx: ColumnNameContext): ir.Expression = {
    ctx.id().asScala match {
      case Seq(columnName) => ir.Column(None, visitId(columnName))
      case Seq(tableNameOrAlias, columnName) =>
        ir.Column(Some(ir.ObjectReference(visitId(tableNameOrAlias))), visitId(columnName))
    }
  }

  override def visitOrderItem(ctx: OrderItemContext): ir.SortOrder = {
    val direction = if (ctx.DESC() != null) ir.Descending else ir.Ascending
    val nullOrdering = if (direction == ir.Descending) {
      if (ctx.LAST() != null) {
        ir.NullsLast
      } else {
        ir.NullsFirst
      }
    } else {
      if (ctx.FIRST() != null) {
        ir.NullsFirst
      } else {
        ir.NullsLast
      }
    }
    ir.SortOrder(ctx.expr().accept(this), direction, nullOrdering)
  }

  override def visitLiteral(ctx: LiteralContext): ir.Literal = {
    val sign = Option(ctx.sign()).map(_ => "-").getOrElse("")
    ctx match {
      case c if c.DATE_LIT() != null =>
        val dateStr = c.DATE_LIT().getText.stripPrefix("DATE'").stripSuffix("'")
        Try(java.time.LocalDate.parse(dateStr))
          .map(date => ir.Literal(date = Some(date.toEpochDay)))
          .getOrElse(ir.Literal(nullType = Some(ir.NullType)))
      case c if c.TIMESTAMP_LIT() != null =>
        val timestampStr = c.TIMESTAMP_LIT().getText.stripPrefix("TIMESTAMP'").stripSuffix("'")
        val format = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
        Try(LocalDateTime.parse(timestampStr, format))
          .map(dt => ir.Literal(timestamp = Some(dt.toEpochSecond(ZoneOffset.UTC))))
          .getOrElse(ir.Literal(nullType = Some(ir.NullType)))
      case c if c.STRING() != null => ir.Literal(string = Some(removeQuotes(c.STRING().getText)))
      case c if c.DECIMAL() != null => buildLiteralNumber(sign + c.DECIMAL().getText)
      case c if c.FLOAT() != null => buildLiteralNumber(sign + c.FLOAT().getText)
      case c if c.REAL() != null => buildLiteralNumber(sign + c.REAL().getText)
      case c if c.NULL_() != null => ir.Literal(nullType = Some(ir.NullType))
      case c if c.trueFalse() != null => visitTrueFalse(c.trueFalse())
      case c if c.jsonLiteral() != null => visitJsonLiteral(c.jsonLiteral())
      case c if c.arrayLiteral() != null => visitArrayLiteral(c.arrayLiteral())
      case _ => ir.Literal(nullType = Some(ir.NullType))
    }
  }

  override def visitNum(ctx: NumContext): ir.Literal = buildLiteralNumber(ctx.getText)

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  override def visitTrueFalse(ctx: TrueFalseContext): ir.Literal = ctx.TRUE() match {
    case null => ir.Literal(boolean = Some(false))
    case _ => ir.Literal(boolean = Some(true))
  }

  private def buildLiteralNumber(decimal: String): ir.Literal = BigDecimal(decimal) match {
    case d if d.isValidShort => ir.Literal(short = Some(d.toShort))
    case d if d.isValidInt => ir.Literal(integer = Some(d.toInt))
    case d if d.isValidLong => ir.Literal(long = Some(d.toLong))
    case d if d.isDecimalFloat || d.isExactFloat => ir.Literal(float = Some(d.toFloat))
    case d if d.isDecimalDouble || d.isExactDouble => ir.Literal(double = Some(d.toDouble))
    case _ => ir.Literal(decimal = Some(ir.Decimal(decimal, None, None)))
  }

  override def visitExprNextval(ctx: ExprNextvalContext): ir.Expression = {
    NextValue(ctx.objectName().getText)
  }

  override def visitExprDot(ctx: ExprDotContext): ir.Expression = {
    val lhs = ctx.expr(0).accept(this)
    val rhs = ctx.expr(1).accept(this)
    ir.Dot(lhs, rhs)
  }

  override def visitExprColon(ctx: ExprColonContext): ir.Expression = {
    val lhs = ctx.expr(0).accept(this)
    val rhs = ctx.expr(1).accept(this)
    ir.JsonAccess(lhs, rhs)
  }

  override def visitExprCollate(ctx: ExprCollateContext): ir.Expression = {
    ir.Collate(ctx.expr().accept(this), removeQuotes(ctx.string().getText))
  }

  override def visitExprNot(ctx: ExprNotContext): ir.Expression = {
    ctx.NOT().asScala.foldLeft(ctx.expr().accept(this)) { case (e, _) => ir.Not(e) }
  }

  override def visitExprAnd(ctx: ExprAndContext): ir.Expression = {
    val left = ctx.expr(0).accept(this)
    val right = ctx.expr(1).accept(this)
    ir.And(left, right)
  }

  override def visitExprOr(ctx: ExprOrContext): ir.Expression = {
    val left = ctx.expr(0).accept(this)
    val right = ctx.expr(1).accept(this)
    ir.Or(left, right)
  }

  override def visitExprPredicate(ctx: ExprPredicateContext): ir.Expression = {
    buildPredicatePartial(ctx.predicatePartial(), ctx.expr().accept(this))
  }

  override def visitExprComparison(ctx: ExprComparisonContext): ir.Expression = {
    val left = ctx.expr(0).accept(this)
    val right = ctx.expr(1).accept(this)
    buildComparisonExpression(ctx.comparisonOperator(), left, right)
  }

  override def visitExprDistinct(ctx: ExprDistinctContext): ir.Expression = {
    ir.Distinct(ctx.expr().accept(this))
  }

  override def visitExprWithinGroup(ctx: ExprWithinGroupContext): ir.Expression = {
    val expr = ctx.expr().accept(this)
    val sortOrders = buildSortOrder(ctx.withinGroup().orderByClause())
    ir.WithinGroup(expr, sortOrders)
  }

  override def visitExprOver(ctx: ExprOverContext): ir.Expression = {
    buildWindow(ctx.overClause(), ctx.expr().accept(this))
  }

  override def visitExprAscribe(ctx: ExprAscribeContext): ir.Expression = {
    ir.Cast(ctx.expr().accept(this), DataTypeBuilder.buildDataType(ctx.dataType()))
  }

  override def visitExprSign(ctx: ExprSignContext): ir.Expression = ctx.sign() match {
    case c if c.PLUS() != null => ir.UPlus(ctx.expr().accept(this))
    case c if c.MINUS() != null => ir.UMinus(ctx.expr().accept(this))
  }

  override def visitExprPrecedence0(ctx: ExprPrecedence0Context): ir.Expression = {
    buildBinaryOperation(ctx.op, ctx.expr(0).accept(this), ctx.expr(1).accept(this))
  }

  override def visitExprPrecedence1(ctx: ExprPrecedence1Context): ir.Expression = {
    buildBinaryOperation(ctx.op, ctx.expr(0).accept(this), ctx.expr(1).accept(this))
  }

  override def visitJsonLiteral(ctx: JsonLiteralContext): ir.Literal = {
    val fields = ctx.kvPair().asScala.map { kv =>
      val fieldName = removeQuotes(kv.key.getText)
      val fieldValue = visitLiteral(kv.literal())
      fieldName -> fieldValue
    }
    ir.Literal(json = Some(ir.JsonExpr(UnresolvedType, fields)))
  }

  override def visitArrayLiteral(ctx: ArrayLiteralContext): ir.Literal = {
    ir.Literal(array = Some(ir.ArrayExpr(UnresolvedType, ctx.literal().asScala.map(visitLiteral))))
  }

  override def visitPrimArrayAccess(ctx: PrimArrayAccessContext): ir.Expression = {
    ir.ArrayAccess(ctx.id().accept(this), ctx.num().accept(this))
  }

  override def visitPrimObjectAccess(ctx: PrimObjectAccessContext): ir.Expression = {
    ir.JsonAccess(ctx.id().accept(this), ir.Id(removeQuotes(ctx.string().getText)))
  }

  private def buildBinaryOperation(operator: Token, left: ir.Expression, right: ir.Expression): ir.Expression =
    operator.getType match {
      case STAR => ir.Multiply(left, right)
      case DIVIDE => ir.Divide(left, right)
      case PLUS => ir.Add(left, right)
      case MINUS => ir.Subtract(left, right)
      case MODULE => ir.Mod(left, right)
      case PIPE_PIPE => ir.Concat(Seq(left, right))
    }

  private[snowflake] def buildComparisonExpression(
      op: ComparisonOperatorContext,
      left: ir.Expression,
      right: ir.Expression): ir.Expression = {
    if (op.EQ() != null) {
      ir.Equals(left, right)
    } else if (op.NE() != null || op.LTGT() != null) {
      ir.NotEquals(left, right)
    } else if (op.GT() != null) {
      ir.GreaterThan(left, right)
    } else if (op.LT() != null) {
      ir.LessThan(left, right)
    } else if (op.GE() != null) {
      ir.GreaterThanOrEqual(left, right)
    } else if (op.LE() != null) {
      ir.LessThanOrEqual(left, right)
    } else {
      ir.UnresolvedExpression(op.getText)
    }
  }

  override def visitIffExpr(ctx: IffExprContext): ir.Expression = {
    val condition = ctx.predicate().accept(this)
    val thenBranch = ctx.expr(0).accept(this)
    val elseBranch = ctx.expr(1).accept(this)
    Iff(condition, thenBranch, elseBranch)
  }

  override def visitCastExpr(ctx: CastExprContext): ir.Expression = ctx match {
    case c if c.castOp != null =>
      val expression = c.expr().accept(this)
      val dataType = DataTypeBuilder.buildDataType(c.dataType())
      ir.Cast(expression, dataType, returnNullOnError = c.TRY_CAST() != null)
    case c if c.INTERVAL() != null =>
      ir.Cast(c.expr().accept(this), ir.IntervalType)
  }

  override def visitRankingWindowedFunction(ctx: RankingWindowedFunctionContext): ir.Expression = {
    // TODO handle ignoreOrRespectNulls
    buildWindow(ctx.overClause(), ctx.standardFunction().accept(this))
  }

  private def buildWindow(ctx: OverClauseContext, windowFunction: ir.Expression): ir.Expression = {
    val partitionSpec = visitMany(ctx.expr())
    val sortOrder =
      Option(ctx.windowOrderingAndFrame()).map(c => buildSortOrder(c.orderByClause())).getOrElse(Seq())

    val frameSpec =
      Option(ctx.windowOrderingAndFrame())
        .flatMap(c => Option(c.rowOrRangeClause()))
        .map(buildWindowFrame)

    ir.Window(
      window_function = windowFunction,
      partition_spec = partitionSpec,
      sort_order = sortOrder,
      frame_spec = frameSpec)
  }

  private[snowflake] def buildSortOrder(ctx: OrderByClauseContext): Seq[ir.SortOrder] = {
    ctx.orderItem().asScala.map(visitOrderItem)
  }

  private def buildWindowFrame(ctx: RowOrRangeClauseContext): ir.WindowFrame = {
    val frameType = if (ctx.ROWS() != null) ir.RowsFrame else ir.RangeFrame
    val lower = buildFrameBound(ctx.windowFrameExtent().windowFrameBound(0))
    val upper = buildFrameBound(ctx.windowFrameExtent().windowFrameBound(1))
    ir.WindowFrame(frameType, lower, upper)
  }

  private def buildFrameBound(ctx: WindowFrameBoundContext): ir.FrameBoundary = ctx match {
    case c if c.UNBOUNDED() != null && c.PRECEDING != null => ir.UnboundedPreceding
    case c if c.UNBOUNDED() != null && c.FOLLOWING() != null => ir.UnboundedFollowing
    case c if c.num() != null && c.PRECEDING() != null => ir.PrecedingN(c.num().accept(this))
    case c if c.num() != null && c.FOLLOWING() != null => ir.FollowingN(c.num().accept(this))
    case c if c.CURRENT() != null => ir.CurrentRow
  }

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = {
    val functionName = ctx.functionName() match {
      case c if c.id() != null => visitId(c.id()).id
      case c if c.nonReservedFunctionName() != null => c.nonReservedFunctionName().getText
    }
    val arguments = ctx match {
      case c if c.exprList() != null => visitMany(c.exprList().expr())
      case c if c.paramAssocList() != null => c.paramAssocList().paramAssoc().asScala.map(_.accept(this))
      case _ => Seq.empty
    }
    functionBuilder.buildFunction(functionName, arguments)
  }

  // aggregateFunction

  override def visitAggFuncExprList(ctx: AggFuncExprListContext): ir.Expression = {
    val param = visitMany(ctx.exprList().expr())
    functionBuilder.buildFunction(visitId(ctx.id()), param)
  }

  override def visitAggFuncStar(ctx: AggFuncStarContext): ir.Expression = {
    functionBuilder.buildFunction(visitId(ctx.id()), Seq(ir.Star(None)))
  }

  override def visitAggFuncList(ctx: AggFuncListContext): ir.Expression = {
    val param = ctx.expr().accept(this)
    val separator = Option(ctx.string()).map(s => ir.Literal(string = Some(removeQuotes(s.getText))))
    ctx.op.getType match {
      case LISTAGG => functionBuilder.buildFunction("LISTAGG", param +: separator.toSeq)
      case ARRAY_AGG => functionBuilder.buildFunction("ARRAYAGG", Seq(param))
    }
  }
  // end aggregateFunction

  override def visitBuiltinExtract(ctx: BuiltinExtractContext): ir.Expression = {
    val part = ir.Id(removeQuotes(ctx.part.getText))
    val date = ctx.expr().accept(this)
    functionBuilder.buildFunction(ctx.EXTRACT().getText, Seq(part, date))
  }

  override def visitCaseExpression(ctx: CaseExpressionContext): ir.Expression = {
    val exprs = ctx.expr().asScala
    val otherwise = Option(ctx.ELSE()).flatMap(els => exprs.find(occursBefore(els, _)).map(_.accept(this)))
    ctx match {
      case c if c.switchSection().size() > 0 =>
        val expression = exprs.find(occursBefore(_, ctx.switchSection(0))).map(_.accept(this))
        val branches = c.switchSection().asScala.map { branch =>
          ir.WhenBranch(branch.expr(0).accept(this), branch.expr(1).accept(this))
        }
        ir.Case(expression, branches, otherwise)
      case c if c.switchSearchConditionSection().size() > 0 =>
        val branches = c.switchSearchConditionSection().asScala.map { branch =>
          ir.WhenBranch(branch.predicate().accept(this), branch.expr().accept(this))
        }
        ir.Case(None, branches, otherwise)
    }
  }
  override def visitPredicate(ctx: PredicateContext): ir.Expression = ctx match {
    case c if c.EXISTS() != null =>
      ir.Exists(c.subquery().accept(new SnowflakeRelationBuilder))
    case c if c.predicatePartial() != null =>
      val expr = c.expr().accept(this)
      buildPredicatePartial(c.predicatePartial(), expr)
    case c => visitChildren(c)
  }

  private def buildPredicatePartial(ctx: PredicatePartialContext, expression: ir.Expression): ir.Expression = {
    val predicate = ctx match {
      case c if c.IN() != null && c.subquery() != null =>
        IsInRelation(c.subquery().accept(new SnowflakeRelationBuilder), expression)
      case c if c.IN() != null && c.exprList() != null =>
        val collection = visitMany(c.exprList().expr())
        IsInCollection(collection, expression)
      case c if c.BETWEEN() != null =>
        val lowerBound = c.expr(0).accept(this)
        val upperBound = c.expr(1).accept(this)
        ir.And(ir.GreaterThanOrEqual(expression, lowerBound), ir.LessThanOrEqual(expression, upperBound))
      case c if c.LIKE() != null || c.ILIKE() != null =>
        val patterns = if (c.ANY() != null) {
          c.expr()
            .asScala
            .filter(e => occursBefore(c.L_PAREN(), e) && occursBefore(e, c.R_PAREN()))
            .map(_.accept(this))
        } else {
          Seq(c.expr(0).accept(this))
        }
        val escape = Option(c.ESCAPE())
          .flatMap(_ =>
            c.expr()
              .asScala
              .find(occursBefore(c.ESCAPE(), _))
              .map(_.accept(this)))
        LikeSnowflake(expression, patterns, escape, c.LIKE() != null)
      case c if c.RLIKE() != null =>
        val pattern = c.expr(0).accept(this)
        ir.RLike(expression, pattern)
      case c if c.IS() != null =>
        val isNull: ir.Expression = ir.IsNull(expression)
        Option(c.nullNotNull().NOT()).fold(isNull)(_ => ir.Not(isNull))
    }
    Option(ctx.NOT()).fold(predicate)(_ => ir.Not(predicate))
  }

  override def visitParamAssoc(ctx: ParamAssocContext): ir.Expression = {
    NamedArgumentExpression(ctx.id().getText.toUpperCase(), ctx.expr().accept(this))
  }

  override def visitSetColumnValue(ctx: SetColumnValueContext): ir.Expression = {
    ir.Assign(ctx.id().accept(this), ctx.expr().accept(this))
  }
}
