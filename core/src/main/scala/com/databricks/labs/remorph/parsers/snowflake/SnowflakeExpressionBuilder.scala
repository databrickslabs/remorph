package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.Token

import scala.collection.JavaConverters._
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
    case id => ir.Id(id.getText, caseSensitive = false)
  }

  override def visitSelectListElem(ctx: SelectListElemContext): ir.Expression = {
    val rawExpression = ctx match {
      case c if c.columnElem() != null => c.columnElem().accept(this)
      case c if c.expressionElem() != null => c.expressionElem().accept(this)
      case c if c.columnElemStar() != null => c.columnElemStar().accept(this)
    }
    buildAlias(ctx.asAlias(), rawExpression)
  }

  override def visitColumnElemStar(ctx: ColumnElemStarContext): ir.Expression = {
    ir.Star(Option(ctx.objectNameOrAlias()).map {
      case c if c.objectName() != null =>
        val objectNameIds = c.objectName().ids.asScala.map(visitId)
        ir.ObjectReference(objectNameIds.head, objectNameIds.tail: _*)
      case c if c.alias() != null => ir.ObjectReference(visitId(c.alias().id()))
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

  override def visitFullColumnName(ctx: FullColumnNameContext): ir.Expression = {
    val colName = visitId(ctx.colName)
    val objectNameIds = ctx.tableName.asScala.map(visitId)
    val tableName = if (objectNameIds.isEmpty) {
      None
    } else {
      Some(ir.ObjectReference(objectNameIds.head, objectNameIds.tail: _*))
    }
    ir.Column(tableName, colName)
  }

  override def visitLiteral(ctx: LiteralContext): ir.Expression = {
    val sign = Option(ctx.sign()).map(_ => "-").getOrElse("")
    if (ctx.STRING() != null) {
      ir.Literal(string = Some(removeQuotes(ctx.STRING().getText)))
    } else if (ctx.DECIMAL() != null) {
      visitDecimal(sign + ctx.DECIMAL().getText)
    } else if (ctx.FLOAT() != null) {
      visitDecimal(sign + ctx.FLOAT().getText)
    } else if (ctx.REAL() != null) {
      visitDecimal(sign + ctx.REAL().getText)
    } else if (ctx.trueFalse() != null) {
      visitTrueFalse(ctx.trueFalse())
    } else if (ctx.NULL_() != null) {
      ir.Literal(nullType = Some(ir.NullType()))
    } else {
      ir.Literal(nullType = Some(ir.NullType()))
    }
  }

  private def removeQuotes(str: String): String = {
    str.stripPrefix("'").stripSuffix("'")
  }

  override def visitTrueFalse(ctx: TrueFalseContext): ir.Literal = ctx.TRUE() match {
    case null => ir.Literal(boolean = Some(false))
    case _ => ir.Literal(boolean = Some(true))
  }

  private def visitDecimal(decimal: String) = BigDecimal(decimal) match {
    case d if d.isValidShort => ir.Literal(short = Some(d.toShort))
    case d if d.isValidInt => ir.Literal(integer = Some(d.toInt))
    case d if d.isValidLong => ir.Literal(long = Some(d.toLong))
    case d if d.isDecimalFloat || d.isExactFloat => ir.Literal(float = Some(d.toFloat))
    case d if d.isDecimalDouble || d.isExactDouble => ir.Literal(double = Some(d.toDouble))
    case _ => ir.Literal(decimal = Some(ir.Decimal(decimal, None, None)))
  }

  override def visitExprNextval(ctx: ExprNextvalContext): ir.Expression = {
    ir.NextValue(ctx.objectName().getText)
  }

  override def visitExprArrayAccess(ctx: ExprArrayAccessContext): ir.Expression = {
    ir.ArrayAccess(ctx.expr(0).accept(this), ctx.expr(1).accept(this))
  }

  override def visitExprJsonAccess(ctx: ExprJsonAccessContext): ir.Expression = {
    val jsonPath = buildJsonPath(ctx.jsonPath())
    ir.JsonAccess(ctx.expr().accept(this), jsonPath)
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

  private def buildJsonPath(ctx: JsonPathContext): Seq[String] =
    ctx.jsonPathElem().asScala.map {
      case elem if elem.ID() != null => elem.ID().getText
      case elem if elem.DOUBLE_QUOTE_ID() != null =>
        elem.DOUBLE_QUOTE_ID().getText.stripPrefix("\"").stripSuffix("\"")
    }

  private def buildBinaryOperation(operator: Token, left: ir.Expression, right: ir.Expression): ir.Expression =
    operator.getType match {
      case STAR => ir.Multiply(left, right)
      case DIVIDE => ir.Divide(left, right)
      case PLUS => ir.Add(left, right)
      case MINUS => ir.Subtract(left, right)
      case MODULE => ir.Mod(left, right)
      case PIPE_PIPE => ir.Concat(left, right)
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
      ir.LesserThan(left, right)
    } else if (op.GE() != null) {
      ir.GreaterThanOrEqual(left, right)
    } else if (op.LE() != null) {
      ir.LesserThanOrEqual(left, right)
    } else {
      ir.UnresolvedExpression(op.getText)
    }
  }

  override def visitIffExpr(ctx: IffExprContext): ir.Expression = {
    val condition = ctx.searchCondition().accept(this)
    val thenBranch = ctx.expr(0).accept(this)
    val elseBranch = ctx.expr(1).accept(this)
    ir.Iff(condition, thenBranch, elseBranch)
  }

  override def visitSearchCondition(ctx: SearchConditionContext): ir.Expression = {
    val pred = ctx.predicate().accept(this)
    if (ctx.NOT().size() % 2 == 1) {
      ir.Not(pred)
    } else {
      pred
    }
  }

  override def visitArrLiteral(ctx: ArrLiteralContext): ir.Expression = {
    val elementsExpressions = ctx.value().asScala.map(_.accept(this))
    val elements = elementsExpressions.collect { case lit: ir.Literal => lit }
    if (elementsExpressions.size != elements.size) {
      ir.UnresolvedExpression(ctx.getText)
    } else {
      ir.Literal(array = Some(ir.ArrayExpr(dataType = None, elements = elements)))
    }
  }

  override def visitCastExpr(ctx: CastExprContext): ir.Expression = ctx match {
    case c if c.castOp != null =>
      val expression = c.expr().accept(this)
      val dataType = DataTypeBuilder.buildDataType(c.dataType())
      ir.Cast(expression, dataType, returnNullOnError = c.TRY_CAST() != null)
    case c if c.conversion != null =>
      ir.Cast(c.expr().accept(this), extractDateTimeType(c.conversion))
    case c if c.INTERVAL() != null =>
      ir.Cast(c.expr().accept(this), ir.IntervalType())
  }

  private def extractDateTimeType(t: Token): ir.DataType = t.getType match {
    // default timestamp type is TIMESTAMP_NZT
    case TO_TIMESTAMP => ir.TimestampNTZType()
    case TO_TIME | TIME => ir.TimeType()
    case TO_DATE | DATE => ir.DateType()
  }

  override def visitRankingWindowedFunction(ctx: RankingWindowedFunctionContext): ir.Expression = {
    val windowFunction = buildWindowFunction(ctx)
    buildWindow(ctx.overClause(), windowFunction)
  }

  private def buildWindow(ctx: OverClauseContext, windowFunction: ir.Expression): ir.Expression = {
    val overClause = Option(ctx)
    val partitionSpec =
      overClause.flatMap(o => Option(o.partitionBy())).map(buildPartitionSpec).getOrElse(Seq())
    val sortOrder =
      overClause.flatMap(o => Option(o.orderByExpr())).map(buildSortOrder).getOrElse(Seq())

    ir.Window(
      window_function = windowFunction,
      partition_spec = partitionSpec,
      sort_order = sortOrder,
      frame_spec = DummyWindowFrame)
  }

  private[snowflake] def buildWindowFunction(ctx: RankingWindowedFunctionContext): ir.Expression = ctx match {
    case c if c.ROW_NUMBER() != null => ir.RowNumber
    case c if c.NTILE() != null =>
      val parameter = ctx.expr(0).accept(this)
      ir.NTile(parameter)
    case c => ir.UnresolvedExpression(c.getText)
  }

  private def buildPartitionSpec(ctx: PartitionByContext): Seq[ir.Expression] = {
    ctx.exprList().expr().asScala.map(_.accept(this))
  }

  private[snowflake] def buildSortOrder(ctx: OrderByExprContext): Seq[ir.SortOrder] = {
    val exprList = ctx.exprListSorted()
    val exprs = exprList.expr().asScala
    val commas = exprList.COMMA().asScala.map(_.getSymbol.getStopIndex) :+ exprList.getStop.getStopIndex
    val descs = exprList.ascDesc().asScala.filter(_.DESC() != null).map(_.getStop.getStopIndex)

    // Lists returned by expr() and ascDesc() above may have different sizes
    // for example with `ORDER BY a, b DESC, c` (3 expr but only 1 ascDesc).
    // So we use the position of the ascDesc elements relative to the position of
    // commas in the ORDER BY expression to determine which expr is affected by each ascDesc
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

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = {
    val functionName = ctx.id().getText
    val arguments = Option(ctx.exprList()).map(_.expr().asScala.map(_.accept(this))).getOrElse(Seq())
    functionBuilder.buildFunction(functionName, arguments)
  }

  // aggregateFunction

  override def visitAggFuncExprList(ctx: AggFuncExprListContext): ir.Expression = {
    val param = ctx.exprList().expr().asScala.map(_.accept(this))
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

  override def visitBuiltinTrim(ctx: BuiltinTrimContext): ir.Expression = {
    val expression = ctx.expr().accept(this)
    val characters = Option(ctx.string()).map(_.accept(this)).toList
    functionBuilder.buildFunction(ctx.trim.getText, expression :: characters)
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
          ir.WhenBranch(branch.searchCondition().accept(this), branch.expr().accept(this))
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

      case c if c.IN() != null =>
        ir.IsIn(c.subquery().accept(new SnowflakeRelationBuilder), expression)
      case c if c.BETWEEN() != null =>
        val lowerBound = c.expr(0).accept(this)
        val upperBound = c.expr(1).accept(this)
        ir.And(ir.GreaterThanOrEqual(expression, lowerBound), ir.LesserThanOrEqual(expression, upperBound))
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
        ir.Like(expression, patterns, escape, c.LIKE() != null)
      case c if c.RLIKE() != null =>
        val pattern = c.expr(0).accept(this)
        ir.RLike(expression, pattern)
      case c if c.IS() != null =>
        val isNull: ir.Expression = ir.IsNull(expression)
        Option(c.nullNotNull().NOT()).fold(isNull)(_ => ir.Not(isNull))
    }
    Option(ctx.NOT()).fold(predicate)(_ => ir.Not(predicate))
  }

}
