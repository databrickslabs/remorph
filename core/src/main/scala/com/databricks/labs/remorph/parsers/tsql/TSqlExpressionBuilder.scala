package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.{StringContext => _, _}
import com.databricks.labs.remorph.parsers.{ParserCommon, XmlFunction, tsql}
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.Trees

import scala.collection.JavaConverters._

class TSqlExpressionBuilder(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.Expression]
    with ParserCommon[ir.Expression] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Expression = {
    ir.UnresolvedExpression(ruleText = ruleText, message = message)
  }

  // Concrete visitors..

  override def visitOptionClause(ctx: TSqlParser.OptionClauseContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // we gather the options given to use by the original query, though at the moment, we do nothing
      // with them.
      val opts = vc.optionBuilder.buildOptionList(ctx.lparenOptionList().optionList().genericOption().asScala)
      ir.Options(opts.expressionOpts, opts.stringOpts, opts.boolFlags, opts.autoFlags)
  }

  override def visitUpdateElemCol(ctx: TSqlParser.UpdateElemColContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val value = ctx.expression().accept(this)
      val target1 = Option(ctx.l2)
        .map(l2 => ir.Identifier(l2.getText, isQuoted = false))
        .getOrElse(ctx.fullColumnName().accept(this))
      val a1 = buildAssign(target1, value, ctx.op)
      Option(ctx.l1).map(l1 => ir.Assign(ir.Identifier(l1.getText, isQuoted = false), a1)).getOrElse(a1)
  }

  override def visitUpdateElemUdt(ctx: TSqlParser.UpdateElemUdtContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val args = ctx.expressionList().expression().asScala.map(_.accept(this))
      val fName = ctx.id(0).getText + "." + ctx.id(1).getText
      val functionResult = vc.functionBuilder.buildFunction(fName, args)

      functionResult match {
        case unresolvedFunction: ir.UnresolvedFunction =>
          unresolvedFunction.copy(is_user_defined_function = true)
        case _ => functionResult
      }
  }

  override def visitUpdateWhereClause(ctx: UpdateWhereClauseContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.searchCondition().accept(this)
    // TODO: TSQL also supports updates via cursor traversal, which is not supported in Databricks SQL
    //       generate UnresolvedExpression
  }

  private[tsql] def buildSelectListElem(ctx: TSqlParser.SelectListElemContext): Seq[ir.Expression] = {

    // If this node has an error such as an extra comma, then don't discard it, prefix it with the errorNode
    val errors = errorCheck(ctx)
    val elem = ctx match {
      case c if c.asterisk() != null => c.asterisk().accept(this)
      case c if c.LOCAL_ID() != null => vc.expressionBuilder.buildLocalAssign(ctx)
      case c if c.expressionElem() != null => ctx.expressionElem().accept(this)
      case _ =>
        ir.UnresolvedExpression(
          ruleText = contextText(ctx),
          message = s"Unsupported select list element",
          ruleName = "expression",
          tokenName = Some(tokenName(ctx.getStart)))
    }
    errors match {
      case Some(errorResult) => Seq(errorResult, elem)
      case None => Seq(elem)
    }
  }

  /**
   * Build a local variable assignment from a column source
   *
   * @param ctx
   * the parse tree containing the assignment
   */
  private def buildLocalAssign(ctx: TSqlParser.SelectListElemContext): ir.Expression = {
    val localId = ir.Identifier(ctx.LOCAL_ID().getText, isQuoted = false)
    val expression = ctx.expression().accept(this)
    buildAssign(localId, expression, ctx.op)
  }

  private def buildAssign(target: ir.Expression, value: ir.Expression, op: Token): ir.Expression = {
    op.getType match {
      case EQ => ir.Assign(target, value)
      case PE => ir.Assign(target, ir.Add(target, value))
      case ME => ir.Assign(target, ir.Subtract(target, value))
      case SE => ir.Assign(target, ir.Multiply(target, value))
      case DE => ir.Assign(target, ir.Divide(target, value))
      case MEA => ir.Assign(target, ir.Mod(target, value))
      case AND_ASSIGN => ir.Assign(target, ir.BitwiseAnd(target, value))
      case OR_ASSIGN => ir.Assign(target, ir.BitwiseOr(target, value))
      case XOR_ASSIGN => ir.Assign(target, ir.BitwiseXor(target, value))
      // We can only reach here if the grammar is changed to add more operators and this function is not updated
      case _ =>
        ir.UnresolvedExpression(
          ruleText = op.getText,
          message = s"Unexpected operator ${op.getText} in assignment",
          ruleName = "expression",
          tokenName = Some(tokenName(op))
        ) // Handle unexpected operation types
    }
  }

  private def buildTableName(ctx: TableNameContext): ir.ObjectReference = {
    val linkedServer = Option(ctx.linkedServer).map(buildId)
    val ids = ctx.ids.asScala.map(buildId)
    val allIds = linkedServer.fold(ids)(ser => ser +: ids)
    ir.ObjectReference(allIds.head, allIds.tail: _*)
  }

  override def visitExprId(ctx: ExprIdContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Column(None, buildId(ctx.id()))
  }

  override def visitFullColumnName(ctx: FullColumnNameContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val columnName = buildId(ctx.id)
      val tableName = Option(ctx.tableName()).map(buildTableName)
      ir.Column(tableName, columnName)
  }

  /**
   * Handles * used in column expressions.
   *
   * This can be used in things like SELECT * FROM table
   *
   * @param ctx
   * the parse tree
   */
  override def visitAsterisk(ctx: AsteriskContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case _ if ctx.tableName() != null =>
          val objectName = Option(ctx.tableName()).map(buildTableName)
          ir.Star(objectName)
        case _ if ctx.INSERTED() != null => Inserted(ir.Star(None))
        case _ if ctx.DELETED() != null => Deleted(ir.Star(None))
        case _ => ir.Star(None)
      }
  }

  /**
   * Expression precedence as defined by parenthesis
   *
   * @param ctx
   * the ExprPrecedenceContext to visit, which contains the expression to which precedence is applied
   * @return
   * the visited expression in IR
   *
   * Note that precedence COULD be explicitly placed in the AST here. If we wish to construct an exact replication of
   * expression source code from the AST, we need to know that the () were there. Redundant parens are otherwise elided
   * and the generated code may seem to be incorrect in the eyes of the customer, even though it will be logically
   * equivalent.
   */
  override def visitExprPrecedence(ctx: ExprPrecedenceContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.expression().accept(this)
  }

  override def visitExprBitNot(ctx: ExprBitNotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.BitwiseNot(ctx.expression().accept(this))
  }

  // Note that while we could evaluate the unary expression if it is a numeric
  // constant, it is usually better to be explicit about the unary operation as
  // if people use -+-42 then maybe they have a reason.
  override def visitExprUnary(ctx: ExprUnaryContext): ir.Expression = {
    val expr = ctx.expression().accept(this)
    ctx.op.getType match {
      case MINUS => ir.UMinus(expr)
      case PLUS => ir.UPlus(expr)
    }
  }

  override def visitExprOpPrec1(ctx: ExprOpPrec1Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec2(ctx: ExprOpPrec2Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec3(ctx: ExprOpPrec3Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  override def visitExprOpPrec4(ctx: ExprOpPrec4Context): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildBinaryExpression(ctx.expression(0).accept(this), ctx.expression(1).accept(this), ctx.op)
  }

  /**
   * Note that the dot operator is considerably more complex than the simple case of a.b. It can also have constructs
   * such as Function().value etc. This is a simple implementation that assumes that we are building a string for a
   * column or table name in contexts where we cannot specifically know that.
   *
   * TODO: Expand this to handle more complex cases
   *
   * @param ctx
   * the parse tree
   */
  override def visitExprDot(ctx: ExprDotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      (left, right) match {
        case (c1: ir.Column, c2: ir.Column) =>
          val path = c1.columnName +: c2.tableNameOrAlias.map(ref => ref.head +: ref.tail).getOrElse(Nil)
          ir.Column(Some(ir.ObjectReference(path.head, path.tail: _*)), c2.columnName)
        case (_: ir.Column, c2: ir.CallFunction) =>
          vc.functionBuilder.functionType(c2.function_name) match {
            case XmlFunction => tsql.TsqlXmlFunction(c2, left)
            case _ => ir.Dot(left, right)
          }
        // Other cases
        case _ => ir.Dot(left, right)
      }
  }

  override def visitExprCase(ctx: ExprCaseContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.caseExpression().accept(this)
  }

  override def visitCaseExpression(ctx: CaseExpressionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val caseExpr = if (ctx.caseExpr != null) Option(ctx.caseExpr.accept(this)) else None
      val elseExpr = if (ctx.elseExpr != null) Option(ctx.elseExpr.accept(this)) else None
      val whenThenPairs: Seq[ir.WhenBranch] = ctx
        .switchSection()
        .asScala
        .map(buildWhen)

      ir.Case(caseExpr, whenThenPairs, elseExpr)
  }

  private def buildWhen(ctx: SwitchSectionContext): ir.WhenBranch =
    ir.WhenBranch(ctx.searchCondition.accept(this), ctx.expression().accept(this))

  override def visitExprFunc(ctx: ExprFuncContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.functionCall.accept(this)
  }

  override def visitExprDollar(ctx: ExprDollarContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.DollarAction
  }

  override def visitExprStar(ctx: ExprStarContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Star(None)
  }

  override def visitExprFuncVal(ctx: ExprFuncValContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      vc.functionBuilder.buildFunction(ctx.getText, Seq.empty)
  }

  override def visitExprPrimitive(ctx: ExprPrimitiveContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.primitiveExpression().accept(this)
  }

  override def visitExprCollate(ctx: ExprCollateContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Collate(ctx.expression.accept(this), removeQuotes(ctx.id.getText))
  }

  override def visitPrimitiveExpression(ctx: PrimitiveExpressionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      Option(ctx.op).map(buildPrimitive).getOrElse(ctx.constant().accept(this))
  }

  override def visitConstant(ctx: TSqlParser.ConstantContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildPrimitive(ctx.con)
  }

  override def visitExprSubquery(ctx: ExprSubqueryContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.ScalarSubquery(ctx.selectStatement().accept(vc.relationBuilder))
  }

  override def visitExprTz(ctx: ExprTzContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = ctx.expression().accept(this)
      val timezone = ctx.timeZone.expression().accept(this)
      ir.Timezone(expression, timezone)
  }

  override def visitScNot(ctx: TSqlParser.ScNotContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Not(ctx.searchCondition().accept(this))
  }

  override def visitScAnd(ctx: TSqlParser.ScAndContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.And(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))
  }

  override def visitScOr(ctx: TSqlParser.ScOrContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Or(ctx.searchCondition(0).accept(this), ctx.searchCondition(1).accept(this))
  }

  override def visitScPred(ctx: TSqlParser.ScPredContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.predicate().accept(this)
  }

  override def visitScPrec(ctx: TSqlParser.ScPrecContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.searchCondition.accept(this)
  }

  override def visitPredExists(ctx: PredExistsContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.Exists(ctx.selectStatement().accept(vc.relationBuilder))
  }

  override def visitPredFreetext(ctx: PredFreetextContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // TODO: build FREETEXT ?
      ir.UnresolvedExpression(
        ruleText = contextText(ctx),
        message = s"Freetext predicates are unsupported",
        ruleName = "expression",
        tokenName = Some(tokenName(ctx.getStart)))
  }

  override def visitPredBinop(ctx: PredBinopContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      ctx.comparisonOperator match {
        case op if op.LT != null && op.EQ != null => ir.LessThanOrEqual(left, right)
        case op if op.GT != null && op.EQ != null => ir.GreaterThanOrEqual(left, right)
        case op if op.LT != null && op.GT != null => ir.NotEquals(left, right)
        case op if op.BANG != null && op.GT != null => ir.LessThanOrEqual(left, right)
        case op if op.BANG != null && op.LT != null => ir.GreaterThanOrEqual(left, right)
        case op if op.BANG != null && op.EQ != null => ir.NotEquals(left, right)
        case op if op.EQ != null => ir.Equals(left, right)
        case op if op.GT != null => ir.GreaterThan(left, right)
        case op if op.LT != null => ir.LessThan(left, right)
      }
  }

  override def visitPredASA(ctx: PredASAContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // TODO: build ASA
      ir.UnresolvedExpression(
        ruleText = contextText(ctx),
        message = s"ALL | SOME | ANY predicate not yet supported",
        ruleName = vc.ruleName(ctx),
        tokenName = Some(tokenName(ctx.getStart)))
  }

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
      val in = if (ctx.selectStatement() != null) {
        // In the result of a sub query
        ir.In(ctx.expression().accept(this), Seq(ir.ScalarSubquery(ctx.selectStatement().accept(vc.relationBuilder))))
      } else {
        // In a list of expressions
        ir.In(ctx.expression().accept(this), ctx.expressionList().expression().asScala.map(_.accept(this)))
      }
      Option(ctx.NOT()).fold[ir.Expression](in)(_ => ir.Not(in))
  }

  override def visitPredLike(ctx: PredLikeContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val left = ctx.expression(0).accept(this)
      val right = ctx.expression(1).accept(this)
      // NB: The escape character is a complete expression that evaluates to a single char at runtime
      // and not a single char at parse time.
      val escape = Option(ctx.expression(2))
        .map(_.accept(this))
      val like = ir.Like(left, right, escape)
      Option(ctx.NOT()).fold[ir.Expression](like)(_ => ir.Not(like))
  }

  override def visitPredIsNull(ctx: PredIsNullContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = ctx.expression().accept(this)
      if (ctx.NOT() != null) ir.IsNotNull(expression) else ir.IsNull(expression)
  }

  override def visitPredExpression(ctx: PredExpressionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.expression().accept(this)
  }

  override def visitFunctionCall(ctx: FunctionCallContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case b if b.builtInFunctions() != null => b.builtInFunctions().accept(this)
        case s if s.standardFunction() != null => s.standardFunction().accept(this)
        case f if f.freetextFunction() != null => f.freetextFunction().accept(this)
        case p if p.partitionFunction() != null => p.partitionFunction().accept(this)
        case h if h.hierarchyidStaticMethod() != null => h.hierarchyidStaticMethod().accept(this)
      }
  }

  override def visitId(ctx: IdContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      buildId(ctx)
  }

  private[tsql] def buildId(ctx: IdContext): ir.Id =
    ctx match {
      case c if c.ID() != null => ir.Id(ctx.getText)
      case c if c.TEMP_ID() != null => ir.Id(ctx.getText)
      case c if c.DOUBLE_QUOTE_ID() != null =>
        ir.Id(ctx.getText.trim.stripPrefix("\"").stripSuffix("\""), caseSensitive = true)
      case c if c.SQUARE_BRACKET_ID() != null =>
        ir.Id(ctx.getText.trim.stripPrefix("[").stripSuffix("]"), caseSensitive = true)
      case c if c.RAW() != null => ir.Id(ctx.getText)
      case _ => ir.Id(removeQuotes(ctx.getText))
    }

  private[tsql] def removeQuotes(str: String): String = {
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
      case DOUBLE_BAR => ir.Concat(Seq(left, right))
    }

  private def buildPrimitive(con: Token): ir.Expression = con.getType match {
    case DEFAULT => Default()
    case LOCAL_ID => ir.Identifier(con.getText, isQuoted = false)
    case STRING => ir.Literal(removeQuotes(con.getText))
    case NULL => ir.Literal.Null
    case HEX => ir.Literal(con.getText) // Preserve format
    case MONEY => Money(ir.StringLiteral(con.getText))
    case INT | REAL | FLOAT => ir.NumericLiteral(con.getText)
  }

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val name = ctx.funcId.getText
      val args = Option(ctx.expression()).map(_.asScala.map(_.accept(this))).getOrElse(Seq.empty)
      vc.functionBuilder.buildFunction(name, args)
  }

  // Note that this visitor is made complicated and difficult because the built-in ir does not use options.
  // So we build placeholder values for the optional values. They also do not extend expression
  // so we can't build them logically with visit and accept. Maybe replace them with
  // extensions that do this?
  override def visitExprOver(ctx: ExprOverContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // The OVER clause is used to accept the IGNORE nulls clause that can be specified after certain
      // windowing functions such as LAG or LEAD, so that the clause is manifest here. The syntax allows
      // 'IGNORE NULLS' and 'RESPECT NULLS', but 'RESPECT NULLS' is the default behavior.
      val windowFunction =
        buildWindowingFunction(ctx.expression().accept(this))
      val partitionByExpressions =
        Option(ctx.overClause().expression()).map(_.asScala.toList.map(_.accept(this))).getOrElse(List.empty)
      val orderByExpressions = Option(ctx.overClause().orderByClause())
        .map(buildOrderBy)
        .getOrElse(List.empty)
      val windowFrame = Option(ctx.overClause().rowOrRangeClause())
        .map(buildWindowFrame)

      ir.Window(
        windowFunction,
        partitionByExpressions,
        orderByExpressions,
        windowFrame,
        ctx.overClause().IGNORE() != null)
  }

  // Some functions need to be converted to Databricks equivalent Windowing functions for the OVER clause
  private def buildWindowingFunction(expression: ir.Expression): ir.Expression = expression match {
    case ir.CallFunction("MONOTONICALLY_INCREASING_ID", args) => ir.CallFunction("ROW_NUMBER", args)
    case _ => expression
  }

  private def buildOrderBy(ctx: OrderByClauseContext): Seq[ir.SortOrder] =
    ctx.orderByExpression().asScala.map { orderByExpr =>
      val expression = orderByExpr.expression(0).accept(this)
      val sortOrder =
        orderByExpr match {
          case o if o.DESC() != null => ir.Descending
          case o if o.ASC() != null => ir.Ascending
          case _ => ir.UnspecifiedSortDirection
        }
      ir.SortOrder(expression, sortOrder, ir.SortNullsUnspecified)
    }

  private def buildWindowFrame(ctx: RowOrRangeClauseContext): ir.WindowFrame = {
    val frameType = buildFrameType(ctx)
    val bounds = Trees
      .findAllRuleNodes(ctx, TSqlParser.RULE_windowFrameBound)
      .asScala
      .collect { case wfb: WindowFrameBoundContext => wfb }
      .map(buildFrame)

    val frameStart = bounds.head // Safe due to the nature of window frames always having at least a start bound
    val frameEnd =
      bounds.tail.headOption.getOrElse(ir.NoBoundary)

    ir.WindowFrame(frameType, frameStart, frameEnd)
  }

  private def buildFrameType(ctx: RowOrRangeClauseContext): ir.FrameType = {
    if (Option(ctx.ROWS()).isDefined) ir.RowsFrame
    else ir.RangeFrame
  }

  private[tsql] def buildFrame(ctx: WindowFrameBoundContext): ir.FrameBoundary =
    ctx match {
      case c if c.UNBOUNDED() != null && c.PRECEDING() != null => ir.UnboundedPreceding
      case c if c.UNBOUNDED() != null && c.FOLLOWING() != null => ir.UnboundedFollowing
      case c if c.CURRENT() != null => ir.CurrentRow
      case c if c.INT() != null && c.PRECEDING() != null =>
        ir.PrecedingN(ir.Literal(c.INT().getText.toInt, ir.IntegerType))
      case c if c.INT() != null && c.FOLLOWING() != null =>
        ir.FollowingN(ir.Literal(c.INT().getText.toInt, ir.IntegerType))
    }

  override def visitExpressionElem(ctx: ExpressionElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val columnDef = ctx.expression().accept(this)
      val aliasOption =
        Option(ctx.columnAlias()).orElse(Option(ctx.asColumnAlias()).map(_.columnAlias())).map { alias =>
          val name = Option(alias.id()).map(buildId).getOrElse(ir.Id(alias.STRING().getText))
          ir.Alias(columnDef, name)
        }
      aliasOption.getOrElse(columnDef)
  }

  override def visitExprWithinGroup(ctx: ExprWithinGroupContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = ctx.expression().accept(this)
      val orderByExpressions = buildOrderBy(ctx.withinGroup().orderByClause())
      ir.WithinGroup(expression, orderByExpressions)
  }

  override def visitExprDistinct(ctx: ExprDistinctContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // Support for functions such as COUNT(DISTINCT column), which is an expression not a child
      ir.Distinct(ctx.expression().accept(this))
  }

  override def visitExprAll(ctx: ExprAllContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // Support for functions such as COUNT(ALL column), which is an expression not a child.
      // ALL has no actual effect on the result so we just pass the expression as is. If we wish to
      // reproduce existing annotations like this, then we would need to add IR.
      ctx.expression().accept(this)
  }

  override def visitPartitionFunction(ctx: PartitionFunctionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // $$PARTITION is not supported in Databricks SQL, so we will report it is not supported
      vc.functionBuilder.buildFunction(s"$$PARTITION", List.empty)
  }

  /**
   * Handles the NEXT VALUE FOR function in SQL Server, which has a special syntax.
   *
   * @param ctx
   * the parse tree
   */
  override def visitNextValueFor(ctx: NextValueForContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val sequenceName = buildTableName(ctx.tableName())
      vc.functionBuilder.buildFunction("NEXTVALUEFOR", Seq(sequenceName))
  }

  override def visitCast(ctx: CastContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = ctx.expression().accept(this)
      val dataType = vc.dataTypeBuilder.build(ctx.dataType())
      ir.Cast(expression, dataType, returnNullOnError = ctx.TRY_CAST() != null)
  }

  override def visitJsonArray(ctx: JsonArrayContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val elements = buildExpressionList(Option(ctx.expressionList()))
      val absentOnNull = checkAbsentNull(ctx.jsonNullClause())
      buildJsonArray(elements, absentOnNull)
  }

  override def visitJsonObject(ctx: JsonObjectContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val jsonKeyValues = Option(ctx.jsonKeyValue()).map(_.asScala).getOrElse(Nil)
      val namedStruct = buildNamedStruct(jsonKeyValues)
      val absentOnNull = checkAbsentNull(ctx.jsonNullClause())
      buildJsonObject(namedStruct, absentOnNull)
  }

  override def visitFreetextFunction(ctx: FreetextFunctionContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // Databricks SQL does not support FREETEXT functions, so there is no point in trying to convert these
      // functions. We do need to generate IR that indicates that this is a function that is not supported.
      vc.functionBuilder.buildFunction(ctx.f.getText, List.empty)
  }

  override def visitHierarchyidStaticMethod(ctx: HierarchyidStaticMethodContext): ir.Expression = errorCheck(
    ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      // Databricks SQL does not support HIERARCHYID functions, so there is no point in trying to convert these
      // functions. We do need to generate IR that indicates that this is a function that is not supported.
      vc.functionBuilder.buildFunction("HIERARCHYID", List.empty)
  }

  override def visitOutputDmlListElem(ctx: OutputDmlListElemContext): ir.Expression = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val expression = Option(ctx.expression()).map(_.accept(this)).getOrElse(ctx.asterisk().accept(this))
      val aliasOption = Option(ctx.asColumnAlias()).map(_.columnAlias()).map { alias =>
        val name = Option(alias.id()).map(buildId).getOrElse(ir.Id(alias.STRING().getText))
        ir.Alias(expression, name)
      }
      aliasOption.getOrElse(expression)
  }

  /**
   * Check if the ABSENT ON NULL clause is present in the JSON clause. The behavior is as follows:
   * <ul>
   * <li>If the clause does not exist, the ABSENT ON NULL is assumed - so true</li>
   * <li>If the clause exists and ABSENT ON NULL - true</li>
   * <li>If the clause exists and NULL ON NULL - false</li>
   * </ul>
   *
   * @param ctx
   * null clause parser context
   * @return
   */
  private def checkAbsentNull(ctx: JsonNullClauseContext): Boolean = {
    Option(ctx).forall(_.loseNulls != null)
  }

  private def buildNamedStruct(ctx: Seq[JsonKeyValueContext]): ir.NamedStruct = {
    val (keys, values) = ctx.map { keyValueContext =>
      val expressions = keyValueContext.expression().asScala.toList
      (expressions.head.accept(this), expressions(1).accept(this))
    }.unzip

    ir.NamedStruct(keys, values)
  }

  private def buildExpressionList(ctx: Option[ExpressionListContext]): Seq[ir.Expression] = {
    ctx.map(_.expression().asScala.map(_.accept(this))).getOrElse(Seq.empty)
  }

  /**
   * Databricks SQL does not have a native JSON_ARRAY function, so we use a Lambda filter and TO_JSON instead, but have
   * to cater for the case where an expression is NULL and the TSql option ABSENT ON NULL is set. When ABSENT ON NULL is
   * set, then any NULL expressions are left out of the JSON array.
   *
   * @param args
   * the list of expressions yield JSON values
   * @param absentOnNull
   * whether we should remove NULL values from the JSON array
   * @return
   * IR for the JSON_ARRAY function
   */
  private[tsql] def buildJsonArray(args: Seq[ir.Expression], absentOnNull: Boolean): ir.Expression = {
    if (absentOnNull) {
      val lambdaVariable = ir.UnresolvedNamedLambdaVariable(Seq("x"))
      val lambdaBody = ir.Not(ir.IsNull(lambdaVariable))
      val lambdaFunction = ir.LambdaFunction(lambdaBody, Seq(lambdaVariable))
      val filter = ir.FilterExpr(args, lambdaFunction)
      ir.CallFunction("TO_JSON", Seq(ir.ValueArray(Seq(filter))))
    } else {
      ir.CallFunction("TO_JSON", Seq(ir.ValueArray(args)))
    }
  }

  /**
   * Databricks SQL does not have a native JSON_OBJECT function, so we use a Lambda filter and TO_JSON instead, but have
   * to cater for the case where an expression is NULL and the TSql option ABSENT ON NULL is set. When ABSENT ON NULL is
   * set, then any NULL expressions are left out of the JSON object.
   *
   * @param namedStruct
   * the named struct of key-value pairs
   * @param absentOnNull
   * whether we should remove NULL values from the JSON object
   * @return
   * IR for the JSON_OBJECT function
   */
  // TODO: This is not likely the correct way to handle this, but it is a start
  //       maybe needs external function at runtime
  private[tsql] def buildJsonObject(namedStruct: ir.NamedStruct, absentOnNull: Boolean): ir.Expression = {
    if (absentOnNull) {
      val lambdaVariables = ir.UnresolvedNamedLambdaVariable(Seq("k", "v"))
      val valueVariable = ir.UnresolvedNamedLambdaVariable(Seq("v"))
      val lambdaBody = ir.Not(ir.IsNull(valueVariable))
      val lambdaFunction = ir.LambdaFunction(lambdaBody, Seq(lambdaVariables))
      val filter = ir.FilterStruct(namedStruct, lambdaFunction)
      ir.CallFunction("TO_JSON", Seq(filter))
    } else {
      ir.CallFunction("TO_JSON", Seq(namedStruct))
    }
  }
}
