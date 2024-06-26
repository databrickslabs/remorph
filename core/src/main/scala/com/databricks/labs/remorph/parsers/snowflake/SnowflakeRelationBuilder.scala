package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters._

class SnowflakeRelationBuilder extends SnowflakeParserBaseVisitor[ir.Relation] with IncompleteParser[ir.Relation] {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val functionBuilder = new SnowflakeFunctionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.Relation = ir.UnresolvedRelation(unparsedInput)
  override def visitSelectStatement(ctx: SelectStatementContext): ir.Relation = {
    val select = ctx.selectOptionalClauses().accept(this)
    val relation = buildLimitOffset(ctx.limitClause(), select)
    val (top, allOrDistinct, selectListElements) = ctx match {
      case c if ctx.selectClause() != null =>
        (
          None,
          c.selectClause().selectListNoTop().allDistinct(),
          c.selectClause().selectListNoTop().selectList().selectListElem().asScala)
      case c if ctx.selectTopClause() != null =>
        (
          Option(c.selectTopClause().selectListTop().topClause()),
          c.selectTopClause().selectListTop().allDistinct(),
          c.selectTopClause().selectListTop().selectList().selectListElem().asScala)
    }
    val expressions = selectListElements.map(_.accept(expressionBuilder))
    ir.Project(buildTop(top, buildDistinct(allOrDistinct, relation, expressions)), expressions)

  }

  private def buildLimitOffset(ctx: LimitClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      if (c.LIMIT() != null) {
        val limit = ir.Limit(input, ctx.num(0).getText.toInt)
        if (c.OFFSET() != null) {
          ir.Offset(limit, ctx.num(1).getText.toInt)
        } else {
          limit
        }
      } else {
        ir.Offset(input, ctx.num(0).getText.toInt)
      }
    }
  }

  private def buildDistinct(
      ctx: AllDistinctContext,
      input: ir.Relation,
      projectExpressions: Seq[ir.Expression]): ir.Relation =
    if (Option(ctx).exists(_.DISTINCT() != null)) {
      val columnNames = projectExpressions.collect {
        case ir.Column(_, c) => Seq(c)
        case ir.Alias(_, a, _) => a
      }.flatten
      ir.Deduplicate(input, columnNames, columnNames.isEmpty, within_watermark = false)
    } else {
      input
    }

  private def buildTop(ctxOpt: Option[TopClauseContext], input: ir.Relation): ir.Relation =
    ctxOpt.fold(input) { top =>
      ir.Limit(input, top.num().getText.toInt)
    }

  override def visitSelectOptionalClauses(ctx: SelectOptionalClausesContext): ir.Relation = {
    val from = Option(ctx.fromClause()).map(_.accept(this)).getOrElse(ir.NoTable())
    buildOrderBy(
      ctx.orderByClause(),
      buildQualify(
        ctx.qualifyClause(),
        buildHaving(ctx.havingClause(), buildGroupBy(ctx.groupByClause(), buildWhere(ctx.whereClause(), from)))))
  }

  override def visitFromClause(ctx: FromClauseContext): ir.Relation = {
    val tableSources = ctx.tableSources().tableSource().asScala.map(_.accept(this))
    // The tableSources seq cannot be empty (as empty FROM clauses are not allowed
    tableSources match {
      case Seq(tableSource) => tableSource
      case sources =>
        sources.reduce(
          ir.Join(_, _, None, ir.InnerJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }
  }

  private def buildFilter[A](ctx: A, conditionRule: A => ParserRuleContext, input: ir.Relation): ir.Relation =
    Option(ctx).fold(input) { c =>
      ir.Filter(input, conditionRule(c).accept(expressionBuilder))
    }
  private def buildHaving(ctx: HavingClauseContext, input: ir.Relation): ir.Relation =
    buildFilter[HavingClauseContext](ctx, _.searchCondition(), input)

  private def buildQualify(ctx: QualifyClauseContext, input: ir.Relation): ir.Relation =
    buildFilter[QualifyClauseContext](ctx, _.expr(), input)
  private def buildWhere(ctx: WhereClauseContext, from: ir.Relation): ir.Relation =
    buildFilter[WhereClauseContext](ctx, _.searchCondition(), from)

  private def buildGroupBy(ctx: GroupByClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val groupingExpressions =
        c.groupByList()
          .groupByElem()
          .asScala
          .map(_.accept(expressionBuilder))
      val aggregate =
        ir.Aggregate(input = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
      buildHaving(c.havingClause(), aggregate)
    }
  }

  private def buildOrderBy(ctx: OrderByClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.orderItem().asScala.map(expressionBuilder.visitOrderItem)
      ir.Sort(input = input, order = sortOrders, is_global = false)
    }
  }

  override def visitObjRefSubquery(ctx: ObjRefSubqueryContext): ir.Relation = {
    val subquery = ctx.subquery().accept(this)
    Option(ctx.asAlias())
      .map(a => ir.SubqueryAlias(subquery, expressionBuilder.visitId(a.alias().id()), ""))
      .getOrElse(subquery)
  }
  override def visitObjRefValues(ctx: ObjRefValuesContext): ir.Relation = {
    val expressions =
      ctx
        .valuesTable()
        .valuesTableBody()
        .exprListInParentheses()
        .asScala
        .map(l => expressionBuilder.visitSeq(l.exprList().expr().asScala))
    ir.Values(expressions)
  }

  override def visitObjRefDefault(ctx: ObjRefDefaultContext): ir.Relation = {
    val tableName = ctx.objectName().id(0).getText
    val table = ir.NamedTable(tableName, Map.empty, is_streaming = false)
    buildPivotOrUnpivot(ctx.pivotUnpivot(), table)
  }

  private def buildPivotOrUnpivot(ctx: PivotUnpivotContext, relation: ir.Relation): ir.Relation = {
    if (ctx == null) {
      relation
    } else if (ctx.PIVOT() != null) {
      buildPivot(ctx, relation)
    } else {
      buildUnpivot(ctx, relation)
    }
  }

  private def buildPivot(ctx: PivotUnpivotContext, relation: ir.Relation): ir.Relation = {
    val pivotValues: Seq[ir.Literal] =
      ctx.values.asScala.map(_.accept(expressionBuilder)).collect { case lit: ir.Literal =>
        lit
      }
    val argument = ir.Column(None, expressionBuilder.visitId(ctx.pivotColumn))
    val column = ir.Column(None, expressionBuilder.visitId(ctx.valueColumn))
    val aggFunc = expressionBuilder.visitId(ctx.aggregateFunc)
    val aggregateFunction = functionBuilder.buildFunction(aggFunc, Seq(argument))
    ir.Aggregate(
      input = relation,
      group_type = ir.Pivot,
      grouping_expressions = Seq(aggregateFunction),
      pivot = Some(ir.Pivot(column, pivotValues)))
  }

  private def buildUnpivot(ctx: PivotUnpivotContext, relation: ir.Relation): ir.Relation = {
    val unpivotColumns = ctx
      .columnList()
      .columnName()
      .asScala
      .map(_.accept(expressionBuilder))
    val variableColumnName = expressionBuilder.visitId(ctx.valueColumn)
    val valueColumnName = expressionBuilder.visitId(ctx.nameColumn)
    ir.Unpivot(
      input = relation,
      ids = unpivotColumns,
      values = None,
      variable_column_name = variableColumnName,
      value_column_name = valueColumnName)
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val tableSource = ctx.tableSourceItemJoined().accept(this)
    buildSample(ctx.sample(), tableSource)
  }

  override def visitTableSourceItemJoined(ctx: TableSourceItemJoinedContext): ir.Relation = {

    def buildJoin(left: ir.Relation, right: JoinClauseContext): ir.Join = {

      ir.Join(
        left,
        right.objectRef().accept(this),
        None,
        translateJoinType(right.joinType()),
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false))
    }
    val left = ctx.objectRef().accept(this)
    ctx.joinClause().asScala.foldLeft(left)(buildJoin)
  }

  private[snowflake] def translateJoinType(joinType: JoinTypeContext): ir.JoinType = {
    if (joinType == null || joinType.outerJoin() == null) {
      ir.InnerJoin
    } else if (joinType.outerJoin().LEFT() != null) {
      ir.LeftOuterJoin
    } else if (joinType.outerJoin().RIGHT() != null) {
      ir.RightOuterJoin
    } else if (joinType.outerJoin().FULL() != null) {
      ir.FullOuterJoin
    } else {
      ir.UnspecifiedJoin
    }
  }

  override def visitCommonTableExpression(ctx: CommonTableExpressionContext): ir.Relation = {
    val tableName = ctx.id().getText
    val columns = Option(ctx.columnList())
      .map(_.columnName().asScala)
      .getOrElse(Seq())
      .map(_.accept(expressionBuilder))
    val query = ctx.selectStatement().accept(this)
    ir.CTEDefinition(tableName, columns, query)
  }

  private def buildNum(ctx: NumContext): BigDecimal = {
    BigDecimal(ctx.getText)
  }

  private def buildSampleMethod(ctx: SampleMethodContext): ir.SamplingMethod = ctx match {
    case c: SampleMethodRowFixedContext => ir.RowSamplingFixedAmount(buildNum(c.num()))
    case c: SampleMethodRowProbaContext => ir.RowSamplingProbabilistic(buildNum(c.num()))
    case c: SampleMethodBlockContext => ir.BlockSampling(buildNum(c.num()))
  }

  private def buildSample(ctx: SampleContext, input: ir.Relation): ir.Relation = {
    Option(ctx)
      .map { sampleCtx =>
        val seed = Option(sampleCtx.sampleSeed()).map(s => buildNum(s.num()))
        val sampleMethod = buildSampleMethod(sampleCtx.sampleMethod())
        ir.TableSample(input, sampleMethod, seed)
      }
      .getOrElse(input)
  }
}
