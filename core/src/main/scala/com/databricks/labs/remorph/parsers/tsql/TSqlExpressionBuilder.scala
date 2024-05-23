package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{FunctionBuilder, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.TerminalNode
import org.antlr.v4.runtime.tree.Trees

import scala.collection.JavaConverters.{asScalaBufferConverter, collectionAsScalaIterableConverter}

class TSqlExpressionBuilder extends TSqlParserBaseVisitor[ir.Expression] with ParserCommon {

  // TODO: A lot of work here for things that are not just simple x.y.z
  override def visitSelectListElem(ctx: TSqlParser.SelectListElemContext): ir.Expression =
    ctx.expressionElem.accept(this)

  override def visitFullTableName(ctx: FullTableNameContext): ir.Literal = {
    // Extract the components of the full table name, if they exist
    val linkedServer = Option(ctx.linkedServer).map(_ => ctx.linkedServer.getText + ".")
    val database = Option(ctx.database).map(_.getText)
    val schema = Option(ctx.schema).map(_.getText)
    val name = ctx.table.getText

    val unparsedIdentifier = List(linkedServer, database, schema, Some(name)).flatten.mkString(".")
    ir.Literal(string = Some(unparsedIdentifier))
  }

  override def visitFullColumnName(ctx: FullColumnNameContext): ir.Column = {
    val columnName = ctx.id.getText
    val fullColumnName = Option(ctx.fullTableName())
      .map(_.accept(this))
      .collect {
        case nt: ir.Literal if nt.string.isDefined => nt.string.get + "." + columnName
      }
      .getOrElse(columnName)
    ir.Column(fullColumnName)
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

  /**
   * Note that the dot operator is considerably more complex than the simple case of a.b. It can also have constructs
   * such as Function().value etc. This is a simple implementation that assumes that we are building a string for a
   * column or table name in contexts where we cannot specifically know that.
   *
   * TODO: Expand this to handle more complex cases
   *
   * @param ctx
   *   the parse tree
   */
  override def visitExprDot(ctx: ExprDotContext): ir.Expression = {
    val left = ctx.expression(0).accept(this)
    val right = ctx.expression(1).accept(this)
    (left, right) match {
      // x.y
      case (c1: ir.Column, c2: ir.Column) =>
        ir.Column(c1.name + "." + c2.name)
      // Other cases
      case _ => ir.Dot(left, right)
    }
  }

  override def visitExprCase(ctx: ExprCaseContext): ir.Expression = {
    ctx.caseExpression().accept(this)
  }

  override def visitCaseExpression(ctx: CaseExpressionContext): ir.Expression = {
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

  override def visitExprFunc(ctx: ExprFuncContext): ir.Expression = ctx.functionCall.accept(this)

  override def visitExprDollar(ctx: ExprDollarContext): ir.Expression = ir.DollarAction()

  override def visitExprCollate(ctx: ExprCollateContext): ir.Expression =
    ir.Collate(ctx.expression.accept(this), removeQuotes(ctx.id.getText))

  override def visitPrimitiveConstant(ctx: TSqlParser.PrimitiveConstantContext): ir.Expression = {
    if (ctx.DOLLAR != null) {
      return ir.Literal(string = Some(ctx.getText))
    }
    buildConstant(ctx.con)
  }

  override def visitExprTz(ctx: ExprTzContext): ir.Expression = {
    val expression = ctx.expression().accept(this)
    val timezone = ctx.timeZone.expression().accept(this)
    ir.Timezone(expression, timezone)
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
    ctx.expression().size() match {
      case 1 => ctx.expression(0).accept(this)
      case _ =>
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

  /**
   * For now, we assume that we are dealing with Column names. Later we can add some context by keeping a symbol table
   * for DECLARE. LOCAL_ID is not catered for as part of an expression in the current grammar, but even that can be an
   * alias for a column name.
   *
   * For now then, they are all seen as columns.
   *
   * @param ctx
   *   the parse tree
   */
  override def visitId(ctx: IdContext): ir.Expression = ctx match {
    case c if c.ID() != null => ir.Column(ctx.getText)
    case c if c.TEMP_ID() != null => ir.Column(ctx.getText)
    case c if c.DOUBLE_QUOTE_ID() != null => ir.Column(ctx.getText)
    case c if c.SQUARE_BRACKET_ID() != null => ir.Column(ctx.getText)
    case c if c.RAW() != null => ir.Column(ctx.getText)
    case _ => ir.Column(ctx.getText)
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

  private def buildConstant(con: Token): ir.Expression = con.getType match {
    case c if c == STRING => ir.Literal(string = Some(removeQuotes(con.getText)))
    case c if c == INT => ir.Literal(integer = Some(con.getText.toInt))
    case c if c == FLOAT => ir.Literal(float = Some(con.getText.toFloat))
    case c if c == HEX => ir.Literal(string = Some(con.getText)) // Preserve format for now
    case c if c == REAL => ir.Literal(double = Some(con.getText.toDouble))
    case c if c == NULL_ => ir.Literal(nullType = Some(ir.NullType()))
  }

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = {
    val name = ctx.funcId.getText
    val args = Option(ctx.expression()).map(_.asScala.map(_.accept(this))).getOrElse(Seq.empty)
    FunctionBuilder.buildFunction(name, args)
  }

  /**
   * This is a special case where we are building a column definition. This is used in the SELECT statement to define
   * the columns that are being selected. This is a special case because we need to handle the aliasing of columns.
   *
   * @param ctx
   *   the parse tree
   */
  override def visitExpressionElem(ctx: ExpressionElemContext): ir.Expression = {
    val columnDef = ctx.expression().accept(this)
    val aliasOption = Trees.findAllRuleNodes(ctx, TSqlParser.RULE_columnAlias).asScala.headOption
    aliasOption match {
      case Some(alias) => ir.Alias(columnDef, Seq(alias.getText), None)
      case _ => columnDef
    }
  }
}
