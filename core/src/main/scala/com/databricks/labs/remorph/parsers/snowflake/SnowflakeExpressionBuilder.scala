package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.Token

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.Locale
import scala.collection.JavaConverters._
import scala.util.Try

class SnowflakeExpressionBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.Expression]
    with ParserCommon[ir.Expression]
    with ir.IRHelpers {

  private val functionBuilder = new SnowflakeFunctionBuilder
  private val typeBuilder = new SnowflakeTypeBuilder

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Expression =
    ir.UnresolvedExpression(ruleText = ruleText, message = message)

  // Concrete visitors..

  override def visitFunctionCall(ctx: FunctionCallContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case b if b.builtinFunction() != null => b.builtinFunction().accept(this)
        case s if s.standardFunction() != null => s.standardFunction().accept(this)
        case a if a.aggregateFunction() != null => a.aggregateFunction().accept(this)
        case r if r.rankingWindowedFunction() != null => r.rankingWindowedFunction().accept(this)
      }
  }

  override def visitValuesTable(ctx: ValuesTableContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.valuesTableBody().accept(this)
  }

  override def visitGroupByElem(ctx: GroupByElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case c if c.columnElem() != null => c.columnElem().accept(this)
        case n if n.INT() != null => ir.NumericLiteral(n.INT().getText)
        case e if e.expressionElem() != null => e.expressionElem().accept(this)
      }
  }

  override def visitId(ctx: IdContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildId(ctx)
  }

  private[snowflake] def buildId(ctx: IdContext): ir.Id = ctx match {
    case c if c.DOUBLE_QUOTE_ID() != null =>
      val idValue = c.getText.trim.stripPrefix("\"").stripSuffix("\"").replaceAll("\"\"", "\"")
      ir.Id(idValue, caseSensitive = true)
    case v if v.AMP() != null =>
      // Note that there is nothing special about &id other than they become $id in Databricks
      // Many places in the builder concatenate the output of visitId with other strings and so we
      // lose the ir.Dot(ir.Variable, ir.Id) that we could pick up and therefore propagate ir.Variable if
      // we wanted to leave the translation to generate phase. I think we probably do want to do that, but
      // a lot of code has bypassed accept() and called visitId directly, and expects ir.Id,
      // then uses fields from it.
      //
      // To rework that is quite a big job. So, for now, we translate &id to $id here.
      // It is not wrong for the id rule to hold the AMP ID alt, but ideally it would produce
      // an ir.Variable and we would process that at generation time instead of concatenating into strings :(
      ir.Id(s"$$${v.ID().getText}")
    case d if d.LOCAL_ID() != null =>
      ir.Id(s"$$${d.LOCAL_ID().getText.drop(1)}")
    case id => ir.Id(id.getText)
  }

  override def visitSelectListElem(ctx: SelectListElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val rawExpression = ctx match {
        case c if c.columnElem() != null => c.columnElem().accept(this)
        case c if c.expressionElem() != null => c.expressionElem().accept(this)
        case c if c.columnElemStar() != null => c.columnElemStar().accept(this)
      }
      buildAlias(ctx.asAlias(), rawExpression)
  }

  override def visitExpressionElem(ctx: ExpressionElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case e if e.expr() != null => e.expr().accept(this)
        case p if p.searchCondition() != null => p.searchCondition().accept(this)
      }
  }

  override def visitColumnElem(ctx: ColumnElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val objectNameIds: Seq[ir.NameOrPosition] = Option(ctx.dotIdentifier()).toSeq.flatMap(_.id().asScala.map(buildId))
      val columnIds: Seq[ir.NameOrPosition] = ctx match {
        case c if c.columnName() != null => c.columnName().id().asScala.map(buildId)
        case c if c.columnPosition() != null => Seq(visitColumnPosition(c.columnPosition()))
      }
      val fqn = objectNameIds ++ columnIds
      val objectRefIds = fqn.take(fqn.size - 1)
      val objectRef = if (objectRefIds.isEmpty) {
        None
      } else {
        Some(ir.ObjectReference(objectRefIds.head, objectRefIds.tail: _*))
      }
      ir.Column(objectRef, fqn.last)
  }

  override def visitDotIdentifier(ctx: DotIdentifierContext): ir.ObjectReference = {
    val ids = ctx.id().asScala.map(buildId)
    ir.ObjectReference(ids.head, ids.tail: _*)
  }

  override def visitColumnPosition(ctx: ColumnPositionContext): ir.Position = {
    ir.Position(ctx.INT().getText.toInt)
  }

  override def visitColumnElemStar(ctx: ColumnElemStarContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Star(Option(ctx.dotIdentifier()).map { on =>
        val objectNameIds = on.id().asScala.map(buildId)
        ir.ObjectReference(objectNameIds.head, objectNameIds.tail: _*)
      })
  }

  private def buildAlias(ctx: AsAliasContext, input: ir.Expression): ir.Expression =
    Option(ctx).fold(input) { c =>
      val alias = buildId(c.alias().id())
      ir.Alias(input, alias)
    }

  override def visitColumnName(ctx: ColumnNameContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.id().asScala match {
        case Seq(columnName) => ir.Column(None, buildId(columnName))
        case Seq(tableNameOrAlias, columnName) =>
          ir.Column(Some(ir.ObjectReference(buildId(tableNameOrAlias))), buildId(columnName))
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

  override def visitLiteral(ctx: LiteralContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val sign = Option(ctx.sign()).map(_ => "-").getOrElse("")
      ctx match {
        case c if Option(c.id()).exists(_.getText.toLowerCase(Locale.ROOT) == "date") =>
          val dateStr = c.string().getText.stripPrefix("'").stripSuffix("'")
          Try(java.time.LocalDate.parse(dateStr))
            .map(ir.Literal(_))
            .getOrElse(ir.Literal.Null)
        case c if c.TIMESTAMP() != null =>
          val timestampStr = c.string.getText.stripPrefix("'").stripSuffix("'")
          val format = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
          Try(LocalDateTime.parse(timestampStr, format))
            .map(ir.Literal(_))
            .getOrElse(ir.Literal.Null)
        case c if c.string() != null => c.string.accept(this)
        case c if c.INT() != null => ir.NumericLiteral(sign + c.INT().getText)
        case c if c.FLOAT() != null => ir.NumericLiteral(sign + c.FLOAT().getText)
        case c if c.REAL() != null => ir.NumericLiteral(sign + c.REAL().getText)
        case c if c.NULL() != null => ir.Literal.Null
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
   * A string literal is a sequence of tokens identifying either a variable reference
   * or a piece of normal text. At this point in time, we basically re-assemble the pieces
   * here into an ir.StringLiteral. The variable references are translated here into the Databricks
   * SQL equivalent, which is $id.
   * </p>
   * <p>
   * Note however that we really should be generating  something like ir.CompositeString(Seq[something])
   * and then anywhere our ir currently uses a String ir ir.StringLiteral, we should be using ir.CompositeString,
   * which will then be correctly translated at generation time. We wil get there in increments however - for
   * now, this hack will correctly translate variable references in string literals.
   * </p>
   *
   * @param ctx the parse tree
   */
  override def visitString(ctx: SnowflakeParser.StringContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {

        // $$string$$ means interpret the string as raw string with no variable substitution, escape sequences, etc.
        // TODO: Do we need a raw flag in the ir.StringLiteral so that we generate r'sdfsdfsdsfds' for Databricks SQL?
        //       or is r'string' a separate Ir in Spark?
        case _ if ctx.DOLLAR_STRING() != null =>
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

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  override def visitTrueFalse(ctx: TrueFalseContext): ir.Literal =
    ctx.TRUE() match {
      case null => ir.Literal.False
      case _ => ir.Literal.True
    }

  override def visitExprNot(ctx: ExprNotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.NOT().asScala.foldLeft(ctx.expr().accept(this)) { case (e, _) => ir.Not(e) }
  }

  override def visitExprAnd(ctx: ExprAndContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.And(left, right)
  }

  override def visitExprOr(ctx: ExprOrContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.Or(left, right)
  }

  override def visitNonLogicalExpression(ctx: NonLogicalExpressionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.expression().accept(this)
  }

  override def visitExprPrecedence(ctx: ExprPrecedenceContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.expression().accept(this)
  }

  override def visitExprNextval(ctx: ExprNextvalContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      NextValue(ctx.dotIdentifier().getText)
  }

  override def visitExprDot(ctx: ExprDotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val lhs = ctx.expression(0).accept(this)
      val rhs = ctx.expression(1).accept(this)
      ir.Dot(lhs, rhs)
  }

  override def visitExprColon(ctx: ExprColonContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val lhs = ctx.expression(0).accept(this)
      val rhs = ctx.expression(1).accept(this)
      ir.JsonAccess(lhs, rhs)
  }

  override def visitExprCollate(ctx: ExprCollateContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Collate(ctx.expression().accept(this), removeQuotes(ctx.string().getText))
  }

  override def visitExprCase(ctx: ExprCaseContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.caseExpression().accept(this)
  }

  override def visitExprIff(ctx: ExprIffContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.iffExpr().accept(this)
  }

  override def visitExprComparison(ctx: ExprComparisonContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      buildComparisonExpression(ctx.comparisonOperator(), left, right)
  }

  override def visitExprDistinct(ctx: ExprDistinctContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Distinct(ctx.expression().accept(this))
  }

  override def visitExprWithinGroup(ctx: ExprWithinGroupContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expr = ctx.expression().accept(this)
      val sortOrders = buildSortOrder(ctx.withinGroup().orderByClause())
      ir.WithinGroup(expr, sortOrders)
  }

  override def visitExprOver(ctx: ExprOverContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildWindow(ctx.overClause(), ctx.expression().accept(this))
  }

  override def visitExprCast(ctx: ExprCastContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.castExpr().accept(this)
  }

  override def visitExprAscribe(ctx: ExprAscribeContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Cast(ctx.expression().accept(this), typeBuilder.buildDataType(ctx.dataType()))
  }

  override def visitExprSign(ctx: ExprSignContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.sign() match {
        case c if c.PLUS() != null => ir.UPlus(ctx.expression().accept(this))
        case c if c.MINUS() != null => ir.UMinus(ctx.expression().accept(this))
      }
  }

  override def visitExprPrecedence0(ctx: ExprPrecedence0Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryOperation(ctx.op, ctx.expression(0).accept(this), ctx.expression(1).accept(this))
  }

  override def visitExprPrecedence1(ctx: ExprPrecedence1Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryOperation(ctx.op, ctx.expression(0).accept(this), ctx.expression(1).accept(this))
  }

  override def visitExprPrimitive(ctx: ExprPrimitiveContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.primitiveExpression().accept(this)
  }

  override def visitExprFuncCall(ctx: ExprFuncCallContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.functionCall().accept(this)
  }

  override def visitJsonLiteral(ctx: JsonLiteralContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val fields = ctx.kvPair().asScala.map { kv =>
        val fieldName = removeQuotes(kv.key.getText)
        val fieldValue = visitLiteral(kv.literal())
        ir.Alias(fieldValue, ir.Id(fieldName))
      }
      ir.StructExpr(fields)
  }

  override def visitArrayLiteral(ctx: ArrayLiteralContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val elements = ctx.expr().asScala.map(_.accept(this)).toList
      // TODO: The current type determination may be too naive
      // but this does not affect code generation as the generator does not use it.
      // Here we determine the type of the array by inspecting the first expression in the array literal,
      // but when an array literal contains a double or a cast and the first value appears to be an integer,
      // then the array literal type should probably be typed as DoubleType and not IntegerType, which means
      // we need a function that types all the expressions and types it as the most general type.
      val dataType = elements.headOption.map(_.dataType).getOrElse(ir.UnresolvedType)
      ir.ArrayExpr(elements, dataType)
  }

  override def visitPrimArrayAccess(ctx: PrimArrayAccessContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.ArrayAccess(ctx.id().accept(this), ir.NumericLiteral(ctx.INT().getText))
  }

  override def visitPrimExprColumn(ctx: PrimExprColumnContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.id().accept(this)
  }

  override def visitPrimObjectAccess(ctx: PrimObjectAccessContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.JsonAccess(ctx.id().accept(this), ir.Id(removeQuotes(ctx.string().getText)))
  }

  override def visitPrimExprLiteral(ctx: PrimExprLiteralContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.literal().accept(this)
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
      ir.UnresolvedExpression(
        ruleText = contextText(op),
        message =
          s"Unknown comparison operator ${contextText(op)} in SnowflakeExpressionBuilder.buildComparisonExpression",
        ruleName = vc.ruleName(op),
        tokenName = Some(tokenName(op.getStart)))
    }
  }

  override def visitIffExpr(ctx: IffExprContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val condition = ctx.searchCondition().accept(this)
      val thenBranch = ctx.expr(0).accept(this)
      val elseBranch = ctx.expr(1).accept(this)
      ir.If(condition, thenBranch, elseBranch)
  }

  override def visitCastExpr(ctx: CastExprContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
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
  }

  override def visitRankingWindowedFunction(ctx: RankingWindowedFunctionContext): ir.Expression = errorCheck(
    ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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
  // default frameSpec(UNBOUNDED FOLLOWING) is not supported for:
  // "LAG", "DENSE_RANK","LEAD", "PERCENT_RANK","RANK","ROW_NUMBER"
  private val rankRelatedWindowFunctions = Set("CUME_DIST", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE", "NTILE")

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
    case c if c.INT() != null && c.PRECEDING() != null => ir.PrecedingN(ir.NumericLiteral(c.INT.getText))
    case c if c.INT() != null && c.FOLLOWING() != null => ir.FollowingN(ir.NumericLiteral(c.INT.getText))
    case c if c.CURRENT() != null => ir.CurrentRow
  }

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val functionName = fetchFunctionName(ctx)
      val arguments = ctx match {
        case c if c.exprList() != null => visitMany(c.exprList().expr())
        case c if c.paramAssocList() != null => c.paramAssocList().paramAssoc().asScala.map(_.accept(this))
        case _ => Seq.empty
      }
      functionBuilder.buildFunction(functionName, arguments)
  }

  private def fetchFunctionName(ctx: StandardFunctionContext): String = {
    if (ctx.functionName() != null) {
      ctx.functionName() match {
        case c if c.id() != null => buildId(c.id()).id
        case c if c.nonReservedFunctionName() != null => c.nonReservedFunctionName().getText
      }
    } else {
      ctx.functionOptionalBrackets().getText
    }
  }

  // aggregateFunction

  override def visitAggFuncExprList(ctx: AggFuncExprListContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val param = visitMany(ctx.exprList().expr())
      functionBuilder.buildFunction(buildId(ctx.id()), param)
  }

  override def visitAggFuncStar(ctx: AggFuncStarContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      functionBuilder.buildFunction(buildId(ctx.id()), Seq(ir.Star(None)))
  }

  override def visitAggFuncList(ctx: AggFuncListContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val param = ctx.expr().accept(this)
      val separator = Option(ctx.string()).map(s => ir.Literal(removeQuotes(s.getText)))
      ctx.op.getType match {
        case LISTAGG => functionBuilder.buildFunction("LISTAGG", param +: separator.toSeq)
        case ARRAY_AGG => functionBuilder.buildFunction("ARRAYAGG", Seq(param))
      }
  }

  override def visitBuiltinExtract(ctx: BuiltinExtractContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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

  override def visitCaseExpression(ctx: CaseExpressionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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
            ir.WhenBranch(branch.searchCondition().accept(this), branch.expr().accept(this))
          }
          ir.Case(None, branches, otherwise)
      }
  }

  // Search conditions and predicates

  override def visitScNot(ctx: ScNotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Not(ctx.searchCondition().accept(this))
  }

  override def visitScAnd(ctx: ScAndContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.And(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))
  }

  override def visitScOr(ctx: ScOrContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Or(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))
  }

  override def visitScPred(ctx: ScPredContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.predicate().accept(this)
  }

  override def visitScPrec(ctx: ScPrecContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.searchCondition.accept(this)
  }

  override def visitPredExists(ctx: PredExistsContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Exists(ctx.subquery().accept(vc.relationBuilder))
  }

  override def visitPredBinop(ctx: PredBinopContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      ctx.comparisonOperator match {
        case op if op.LE != null => ir.LessThanOrEqual(left, right)
        case op if op.GE != null => ir.GreaterThanOrEqual(left, right)
        case op if op.LTGT != null => ir.NotEquals(left, right)
        case op if op.NE != null => ir.NotEquals(left, right)
        case op if op.EQ != null => ir.Equals(left, right)
        case op if op.GT != null => ir.GreaterThan(left, right)
        case op if op.LT != null => ir.LessThan(left, right)
      }
  }

  override def visitPredASA(ctx: PredASAContext): ir.Expression =
    // TODO: build ASA
    ir.UnresolvedExpression(
      ruleText = contextText(ctx),
      message = "ALL | SOME | ANY is not yet supported",
      ruleName = vc.ruleName(ctx),
      tokenName = Some(tokenName(ctx.getStart)))

  override def visitPredBetween(ctx: PredBetweenContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val lowerBound = ctx.expression(1).accept(this)
      val upperBound = ctx.expression(2).accept(this)
      val expression = ctx.expression(0).accept(this)
      val between = ir.Between(expression, lowerBound, upperBound)
      Option(ctx.NOT()).fold[ir.Expression](between)(_ => ir.Not(between))
  }

  override def visitPredIn(ctx: PredInContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val in = if (ctx.subquery() != null) {
        // In the result of a sub query
        ir.In(ctx.expression().accept(this), Seq(ir.ScalarSubquery(ctx.subquery().accept(vc.relationBuilder))))
      } else {
        // In a list of expressions
        ir.In(ctx.expression().accept(this), ctx.exprList().expr().asScala.map(_.accept(this)))
      }
      Option(ctx.NOT()).fold[ir.Expression](in)(_ => ir.Not(in))
  }

  override def visitPredLikeSinglePattern(ctx: PredLikeSinglePatternContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      // NB: The escape character is a complete expression that evaluates to a single char at runtime
      // and not a single char at parse time.
      val escape = Option(ctx.expression(2))
        .map(_.accept(this))
      val like = ctx.op.getType match {
        case LIKE => ir.Like(left, right, escape)
        case ILIKE => ir.ILike(left, right, escape)
      }
      Option(ctx.NOT()).fold[ir.Expression](like)(_ => ir.Not(like))
  }

  override def visitPredLikeMultiplePatterns(ctx: PredLikeMultiplePatternsContext): ir.Expression =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val left = ctx.expression(0).accept(this)
        val patterns = visitMany(ctx.exprListInParentheses().exprList().expr())
        val normalizedPatterns = normalizePatterns(patterns, ctx.expression(1))
        val like = ctx.op.getType match {
          case LIKE if ctx.ALL() != null => ir.LikeAll(left, normalizedPatterns)
          case LIKE => ir.LikeAny(left, normalizedPatterns)
          case ILIKE if ctx.ALL() != null => ir.ILikeAll(left, normalizedPatterns)
          case ILIKE => ir.ILikeAny(left, normalizedPatterns)
        }
        Option(ctx.NOT()).fold[ir.Expression](like)(_ => ir.Not(like))
    }

  override def visitPredRLike(ctx: PredRLikeContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      val rLike = ir.RLike(left, right)
      Option(ctx.NOT()).fold[ir.Expression](rLike)(_ => ir.Not(rLike))
  }

  override def visitPredIsNull(ctx: PredIsNullContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = ctx.expression().accept(this)
      if (ctx.NOT() != null) ir.IsNotNull(expression) else ir.IsNull(expression)
  }

  override def visitPredExpr(ctx: PredExprContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.expression().accept(this)
  }

  private def normalizePatterns(patterns: Seq[ir.Expression], escape: ExpressionContext): Seq[ir.Expression] = {
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

  override def visitParamAssoc(ctx: ParamAssocContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      NamedArgumentExpression(ctx.id().getText.toUpperCase(), ctx.expr().accept(this))
  }

  override def visitSetColumnValue(ctx: SetColumnValueContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Assign(ctx.columnName().accept(this), ctx.expr().accept(this))
  }

  override def visitExprSubquery(ctx: ExprSubqueryContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.ScalarSubquery(ctx.subquery().accept(vc.relationBuilder))
  }
}
