package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.UnresolvedType
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.Token

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import scala.collection.JavaConverters._
import scala.util.Try

class SnowflakeExpressionBuilder()
    extends SnowflakeParserBaseVisitor[ir.Expression]
    with ParserCommon[ir.Expression]
    with IncompleteParser[ir.Expression]
    with ir.IRHelpers {

  private val functionBuilder = new SnowflakeFunctionBuilder
  private val typeBuilder = new SnowflakeTypeBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.UnresolvedExpression =
    ir.UnresolvedExpression(unparsedInput)

  override def visitId(ctx: IdContext): ir.Id = ctx match {
    case c if c.DOUBLE_QUOTE_ID() != null =>
      val idValue = c.getText.trim.stripPrefix("\"").stripSuffix("\"").replaceAll("\"\"", "\"")
      ir.Id(idValue, caseSensitive = true)
    case v if v.AMP() != null =>
      // Note that there is nothing special about &id other than they become $id in Databricks
      // Many places in the builder concatenate the output of visitId with other strings and so we
      // lose the ir.Dot(ir.Variable, ir.Id) that we could pick up and therefore propagate ir.Variable if
      // we wanted to leave the translation to generate phase. I think we probably do want to do that, but
      // a lot of code has bypassed accept() and called visitId directly, and expects ir.Id, then uses fields from it.
      //
      // To rework that is quite a big job. So, for now, we translate &id to $id here. It is not wrong for the id rule
      // to hold the AMP ID alt, but ideally it would produce an ir.Variable and we would process that at generation
      // time instead of concatenating into strings :(
      ir.Id(s"$$${v.ID().getText}")
    case d if d.ID2() != null =>
      ir.Id(s"$$${d.ID2().getText.drop(1)}")
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
      ir.Alias(input, alias)
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

  override def visitLiteral(ctx: LiteralContext): ir.Expression = {
    val sign = Option(ctx.sign()).map(_ => "-").getOrElse("")
    ctx match {
      case c if c.DATE_LIT() != null =>
        val dateStr = c.DATE_LIT().getText.stripPrefix("DATE'").stripSuffix("'")
        Try(java.time.LocalDate.parse(dateStr))
          .map(ir.Literal(_))
          .getOrElse(ir.Literal.Null)
      case c if c.TIMESTAMP_LIT() != null =>
        val timestampStr = c.TIMESTAMP_LIT().getText.stripPrefix("TIMESTAMP'").stripSuffix("'")
        val format = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
        Try(LocalDateTime.parse(timestampStr, format))
          .map(ir.Literal(_))
          .getOrElse(ir.Literal.Null)
      case c if c.string() != null => c.string.accept(this)
      case c if c.DECIMAL() != null => ir.NumericLiteral(sign + c.DECIMAL().getText)
      case c if c.FLOAT() != null => ir.NumericLiteral(sign + c.FLOAT().getText)
      case c if c.REAL() != null => ir.NumericLiteral(sign + c.REAL().getText)
      case c if c.NULL_() != null => ir.Literal.Null
      case c if c.trueFalse() != null => visitTrueFalse(c.trueFalse())
      case c if c.jsonLiteral() != null => visitJsonLiteral(c.jsonLiteral())
      case c if c.arrayLiteral() != null => visitArrayLiteral(c.arrayLiteral())
      case _ => ir.Literal.Null
    }
  }

  /**
   * Reconstruct a string literal from its composite parts, translating variable
   * references on the fly.
   * <p>
   *   A string literal is a sequence of tokens identifying either a variable reference
   *   or a piece of normal text. At this point in time, we basically re-assemble the pieces
   *   here into an ir.StringLiteral. The variable references are translated here into the Databricks
   *   SQL equivalent, which is $id.
   * </p>
   * <p>
   *   Note however that we really should be generating  something like ir.CompositeString(Seq[something])
   *   and then anywhere our ir currently uses a String ir ir.StringLiteral, we should be using ir.CompositeString,
   *   which will then be correctly translated at generation time. We wil get there in increments however - for
   *   now, this hack will correctly translate variable references in string literals.
   * </p>
   *
   * @param ctx the parse tree
   */
  override def visitString(ctx: SnowflakeParser.StringContext): ir.Expression = {
    ctx match {

      // $$string$$ means interpret the string as raw string with no variable substitution, escape sequences, etc.
      // TODO: Do we need a raw flag in the ir.StringLiteral so that we generate r'sdfsdfsdsfds' for Databricks SQL?
      //       or is r'string' a separate Ir in Spark?
      case ds if ctx.DOLLAR_STRING() != null =>
        val str = ctx.DOLLAR_STRING().getText.stripPrefix("$$").stripSuffix("$$")
        ir.StringLiteral(str)

      // Else we must have composite string literal
      case _ =>
        val str = if (ctx.stringPart() == null) {
          ""
        } else {
          ctx
            .stringPart()
            .asScala
            .map {
              case p if p.VAR_SIMPLE() != null => s"$${${p.VAR_SIMPLE().getText.drop(1)}}" // &var => ${var} (soon)
              case p if p.VAR_COMPLEX() != null => s"$$${p.VAR_COMPLEX().getText.drop(1)}" // &{var} => ${var}
              case p if p.STRING_AMPAMP() != null => "&" // && => &
              case p if p.STRING_CONTENT() != null => p.STRING_CONTENT().getText
              case p if p.STRING_ESCAPE() != null => p.STRING_ESCAPE().getText
              case p if p.STRING_SQUOTE() != null => "''" // Escaped single quote
              case p if p.STRING_UNICODE() != null => p.STRING_UNICODE().getText
              case _ => removeQuotes(ctx.getText)
            }
            .mkString
        }
        ir.StringLiteral(str)
    }
  }

  override def visitNum(ctx: NumContext): ir.Expression = ir.NumericLiteral(ctx.getText)

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  override def visitTrueFalse(ctx: TrueFalseContext): ir.Literal = ctx.TRUE() match {
    case null => ir.Literal.False
    case _ => ir.Literal.True
  }

  override def visitExprPrecedence(ctx: ExprPrecedenceContext): ir.Expression = {
    ctx.expr().accept(this)
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
    ir.Cast(ctx.expr().accept(this), typeBuilder.buildDataType(ctx.dataType()))
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

  override def visitJsonLiteral(ctx: JsonLiteralContext): ir.Expression = {
    val fields = ctx.kvPair().asScala.map { kv =>
      val fieldName = removeQuotes(kv.key.getText)
      val fieldValue = visitLiteral(kv.literal())
      ir.Alias(fieldValue, ir.Id(fieldName))
    }
    ir.StructExpr(fields)
  }

  override def visitArrayLiteral(ctx: ArrayLiteralContext): ir.Expression = {
    val elements = ctx.literal().asScala.map(visitLiteral).toList.toSeq
    val dataType = elements.headOption.map(_.dataType).getOrElse(UnresolvedType)
    ir.ArrayExpr(elements, dataType)
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
    ir.If(condition, thenBranch, elseBranch)
  }

  override def visitCastExpr(ctx: CastExprContext): ir.Expression = ctx match {
    case c if c.castOp != null =>
      val expression = c.expr().accept(this)
      val dataType = typeBuilder.buildDataType(c.dataType())
      ctx.castOp.getType match {
        case CAST => ir.Cast(expression, dataType)
        case TRY_CAST => ir.TryCast(expression, dataType)
      }

    case c if c.INTERVAL() != null =>
      ir.Cast(c.expr().accept(this), ir.IntervalType)
  }

  override def visitRankingWindowedFunction(ctx: RankingWindowedFunctionContext): ir.Expression = {
    val ignore_nulls = if (ctx.ignoreOrRepectNulls() != null) {
      ctx.ignoreOrRepectNulls().getText.equalsIgnoreCase("IGNORENULLS")
    } else false

    buildWindow(ctx.overClause(), ctx.standardFunction().accept(this), ignore_nulls)
  }

  private def buildWindow(
      ctx: OverClauseContext,
      windowFunction: ir.Expression,
      ignore_nulls: Boolean = false): ir.Expression = {
    val partitionSpec = visitMany(ctx.expr())
    val sortOrder =
      Option(ctx.windowOrderingAndFrame()).map(c => buildSortOrder(c.orderByClause())).getOrElse(Seq())

    val frameSpec =
      Option(ctx.windowOrderingAndFrame())
        .flatMap(c => Option(c.rowOrRangeClause()))
        .map(buildWindowFrame)
        .orElse(snowflakeDefaultFrameSpec(windowFunction))

    ir.Window(
      window_function = windowFunction,
      partition_spec = partitionSpec,
      sort_order = sortOrder,
      frame_spec = frameSpec,
      ignore_nulls = ignore_nulls)
  }

  // see: https://docs.snowflake.com/en/sql-reference/functions-analytic#list-of-window-functions
  private val rankRelatedWindowFunctions = Set(
    "CUME_DIST",
    "DENSE_RANK",
    "FIRST_VALUE",
    "LAG",
    "LAST_VALUE",
    "LEAD",
    "NTH_VALUE",
    "NTILE",
    "PERCENT_RANK",
    "RANK",
    "ROW_NUMBER")

  /**
   * For rank-related window functions, snowflake's default frame deviate from ANSI standard. So in such case, we must
   * make the frame specification explicit. see:
   * https://docs.snowflake.com/en/sql-reference/functions-analytic#usage-notes-for-window-frames
   */
  private def snowflakeDefaultFrameSpec(windowFunction: ir.Expression): Option[ir.WindowFrame] = {
    val rankRelatedDefaultFrameSpec = ir.WindowFrame(ir.RowsFrame, ir.UnboundedPreceding, ir.UnboundedFollowing)
    windowFunction match {
      case fn: ir.Fn if rankRelatedWindowFunctions.contains(fn.prettyName) => Some(rankRelatedDefaultFrameSpec)
      case _ => None
    }
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
    val separator = Option(ctx.string()).map(s => ir.Literal(removeQuotes(s.getText)))
    ctx.op.getType match {
      case LISTAGG => functionBuilder.buildFunction("LISTAGG", param +: separator.toSeq)
      case ARRAY_AGG => functionBuilder.buildFunction("ARRAYAGG", Seq(param))
    }
  }
  // end aggregateFunction

  override def visitBuiltinExtract(ctx: BuiltinExtractContext): ir.Expression = {
    val part = if (ctx.ID() != null) { ir.Id(removeQuotes(ctx.ID().getText)) }
    else {
      buildIdFromString(ctx.string())
    }
    val date = ctx.expr().accept(this)
    functionBuilder.buildFunction(ctx.EXTRACT().getText, Seq(part, date))
  }

  private def buildIdFromString(ctx: SnowflakeParser.StringContext): ir.Id = ctx.accept(this) match {
    case ir.StringLiteral(s) => ir.Id(s)
    case _ => throw new IllegalArgumentException("Expected a string literal")
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
        ir.In(expression, Seq(ir.ScalarSubquery(c.subquery().accept(new SnowflakeRelationBuilder))))
      case c if c.IN() != null && c.exprList() != null =>
        val collection = visitMany(c.exprList().expr())
        ir.In(expression, collection)
      case c if c.BETWEEN() != null =>
        val lowerBound = c.expr(0).accept(this)
        val upperBound = c.expr(1).accept(this)
        ir.And(ir.GreaterThanOrEqual(expression, lowerBound), ir.LessThanOrEqual(expression, upperBound))
      case c if c.likeExpression() != null => buildLikeExpression(c.likeExpression(), expression)
      case c if c.IS() != null =>
        val isNull: ir.Expression = ir.IsNull(expression)
        Option(c.nullNotNull().NOT()).fold(isNull)(_ => ir.IsNotNull(expression))
    }
    Option(ctx.NOT()).fold(predicate)(_ => ir.Not(predicate))
  }

  private def buildLikeExpression(ctx: LikeExpressionContext, child: ir.Expression): ir.Expression = ctx match {
    case single: LikeExprSinglePatternContext =>
      val pattern = single.pat.accept(this)
      val escape = Option(single.escapeChar)
        .map(_.accept(this))
        .collect { case ir.StringLiteral(s) =>
          s.head
        }
        .getOrElse('\\')
      single.op.getType match {
        case LIKE => ir.Like(child, pattern, escape)
        case ILIKE => ir.ILike(child, pattern, escape)
      }
    case multi: LikeExprMultiplePatternsContext =>
      val patterns = visitMany(multi.exprListInParentheses().exprList().expr())
      val normalizedPatterns = normalizePatterns(patterns, multi.expr())
      multi.op.getType match {
        case LIKE if multi.ALL() != null => ir.LikeAll(child, normalizedPatterns)
        case LIKE => ir.LikeAny(child, normalizedPatterns)
        case ILIKE if multi.ALL() != null => ir.ILikeAll(child, normalizedPatterns)
        case ILIKE => ir.ILikeAny(child, normalizedPatterns)
      }

    case rlike: LikeExprRLikeContext => ir.RLike(child, rlike.expr().accept(this))

  }

  private def normalizePatterns(patterns: Seq[ir.Expression], escape: ExprContext): Seq[ir.Expression] = {
    Option(escape)
      .map(_.accept(this))
      .collect { case ir.StringLiteral(esc) =>
        patterns.map {
          case ir.StringLiteral(pat) =>
            val escapedPattern = pat.replace(esc, s"\\$esc")
            ir.StringLiteral(escapedPattern)
          case e => ir.StringReplace(e, ir.Literal(esc), ir.Literal("\\"))
        }
      }
      .getOrElse(patterns)
  }

  override def visitParamAssoc(ctx: ParamAssocContext): ir.Expression = {
    NamedArgumentExpression(ctx.id().getText.toUpperCase(), ctx.expr().accept(this))
  }

  override def visitSetColumnValue(ctx: SetColumnValueContext): ir.Expression = {
    ir.Assign(ctx.id().accept(this), ctx.expr().accept(this))
  }

  override def visitExprSubquery(ctx: ExprSubqueryContext): ir.Expression = {
    ir.ScalarSubquery(ctx.subquery().accept(new SnowflakeRelationBuilder))
  }
}
