package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{IncompleteParser, ParserCommon, intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters._

class SnowflakeRelationBuilder
    extends SnowflakeParserBaseVisitor[ir.LogicalPlan]
    with IncompleteParser[ir.LogicalPlan]
    with ParserCommon[ir.LogicalPlan] {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val functionBuilder = new SnowflakeFunctionBuilder

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.LogicalPlan =
    ir.UnresolvedRelation(unparsedInput)
  override def visitSelectStatement(ctx: SelectStatementContext): ir.LogicalPlan = {
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

  private def buildLimitOffset(ctx: LimitClauseContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx).fold(input) { c =>
      if (c.LIMIT() != null) {
        val limit = ir.Limit(input, ctx.expr(0).accept(expressionBuilder))
        if (c.OFFSET() != null) {
          ir.Offset(limit, ctx.expr(1).accept(expressionBuilder))
        } else {
          limit
        }
      } else {
        ir.Offset(input, ctx.expr(0).accept(expressionBuilder))
      }
    }
  }

  private def buildDistinct(
      ctx: AllDistinctContext,
      input: ir.LogicalPlan,
      projectExpressions: Seq[ir.Expression]): ir.LogicalPlan =
    if (Option(ctx).exists(_.DISTINCT() != null)) {
      val columnNames = projectExpressions.collect {
        case ir.Column(_, c) => Seq(c)
        case ir.Alias(_, a, _) => a
      }.flatten
      ir.Deduplicate(input, columnNames, columnNames.isEmpty, within_watermark = false)
    } else {
      input
    }

  private def buildTop(ctxOpt: Option[TopClauseContext], input: ir.LogicalPlan): ir.LogicalPlan =
    ctxOpt.fold(input) { top =>
      ir.Limit(input, top.expr().accept(expressionBuilder))
    }

  override def visitSelectOptionalClauses(ctx: SelectOptionalClausesContext): ir.LogicalPlan = {
    val from = Option(ctx.fromClause()).map(_.accept(this)).getOrElse(ir.NoTable())
    buildOrderBy(
      ctx.orderByClause(),
      buildQualify(
        ctx.qualifyClause(),
        buildHaving(ctx.havingClause(), buildGroupBy(ctx.groupByClause(), buildWhere(ctx.whereClause(), from)))))
  }

  override def visitFromClause(ctx: FromClauseContext): ir.LogicalPlan = {
    val tableSources = visitMany(ctx.tableSources().tableSource())
    // The tableSources seq cannot be empty (as empty FROM clauses are not allowed
    tableSources match {
      case Seq(tableSource) => tableSource
      case sources =>
        sources.reduce(
          ir.Join(_, _, None, ir.InnerJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }
  }

  private def buildFilter[A](ctx: A, conditionRule: A => ParserRuleContext, input: ir.LogicalPlan): ir.LogicalPlan =
    Option(ctx).fold(input) { c =>
      ir.Filter(input, conditionRule(c).accept(expressionBuilder))
    }
  private def buildHaving(ctx: HavingClauseContext, input: ir.LogicalPlan): ir.LogicalPlan =
    buildFilter[HavingClauseContext](ctx, _.predicate(), input)

  private def buildQualify(ctx: QualifyClauseContext, input: ir.LogicalPlan): ir.LogicalPlan =
    buildFilter[QualifyClauseContext](ctx, _.expr(), input)
  private def buildWhere(ctx: WhereClauseContext, from: ir.LogicalPlan): ir.LogicalPlan =
    buildFilter[WhereClauseContext](ctx, _.predicate(), from)

  private def buildGroupBy(ctx: GroupByClauseContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx).fold(input) { c =>
      val groupingExpressions =
        c.groupByList()
          .groupByElem()
          .asScala
          .map(_.accept(expressionBuilder))
      val aggregate =
        ir.Aggregate(child = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
      buildHaving(c.havingClause(), aggregate)
    }
  }

  private def buildOrderBy(ctx: OrderByClauseContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.orderItem().asScala.map(expressionBuilder.visitOrderItem)
      ir.Sort(input, sortOrders, is_global = false)
    }
  }

  override def visitObjRefTableFunc(ctx: ObjRefTableFuncContext): ir.LogicalPlan = {
    val tableFunc = ir.TableFunction(ctx.functionCall().accept(expressionBuilder))
    buildSubqueryAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), tableFunc))
  }

  override def visitObjRefSubquery(ctx: ObjRefSubqueryContext): ir.LogicalPlan = {
    val relation = ctx match {
      case c if c.subquery() != null => c.subquery().accept(this)
      case c if c.functionCall() != null => ir.TableFunction(c.functionCall().accept(expressionBuilder))
    }
    val maybeLateral = if (ctx.LATERAL() != null) {
      ir.Lateral(relation)
    } else {
      relation
    }
    buildSubqueryAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), maybeLateral))
  }

  private def buildSubqueryAlias(ctx: TableAliasContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx)
      .map(a =>
        ir.SubqueryAlias(
          input,
          expressionBuilder.visitId(a.alias().id()),
          a.id().asScala.map(expressionBuilder.visitId)))
      .getOrElse(input)
  }

  override def visitValuesTableBody(ctx: ValuesTableBodyContext): ir.LogicalPlan = {
    val expressions =
      ctx
        .exprListInParentheses()
        .asScala
        .map(l => expressionBuilder.visitMany(l.exprList().expr()))
    ir.Values(expressions)
  }

  override def visitObjRefDefault(ctx: ObjRefDefaultContext): ir.LogicalPlan = {
    buildTableAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), ctx.objectName().accept(this)))
  }

  override def visitTableRef(ctx: TableRefContext): ir.LogicalPlan = {
    val table = ctx.objectName().accept(this)
    Option(ctx.asAlias())
      .map { a =>
        ir.TableAlias(table, a.alias().getText, Seq())
      }
      .getOrElse(table)
  }

  override def visitObjectName(ctx: ObjectNameContext): ir.LogicalPlan = {
    val tableName = ctx.id().asScala.map(expressionBuilder.visitId).map(_.id).mkString(".")
    ir.NamedTable(tableName, Map.empty, is_streaming = false)
  }

  private def buildTableAlias(ctx: TableAliasContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx)
      .map { c =>
        val alias = c.alias().getText
        val columns = Option(c.id()).map(_.asScala.map(expressionBuilder.visitId)).getOrElse(Seq.empty)
        ir.TableAlias(relation, alias, columns)
      }
      .getOrElse(relation)
  }

  private def buildPivotOrUnpivot(ctx: PivotUnpivotContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    if (ctx == null) {
      relation
    } else if (ctx.PIVOT() != null) {
      buildPivot(ctx, relation)
    } else {
      buildUnpivot(ctx, relation)
    }
  }

  private def buildPivot(ctx: PivotUnpivotContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    val pivotValues: Seq[ir.Literal] = expressionBuilder.visitMany(ctx.values).collect { case lit: ir.Literal => lit }
    val argument = ir.Column(None, expressionBuilder.visitId(ctx.pivotColumn))
    val column = ir.Column(None, expressionBuilder.visitId(ctx.valueColumn))
    val aggFunc = expressionBuilder.visitId(ctx.aggregateFunc)
    val aggregateFunction = functionBuilder.buildFunction(aggFunc, Seq(argument))
    ir.Aggregate(
      child = relation,
      group_type = ir.Pivot,
      grouping_expressions = Seq(aggregateFunction),
      pivot = Some(ir.Pivot(column, pivotValues)))
  }

  private def buildUnpivot(ctx: PivotUnpivotContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    val unpivotColumns = ctx
      .columnList()
      .columnName()
      .asScala
      .map(_.accept(expressionBuilder))
    val variableColumnName = expressionBuilder.visitId(ctx.valueColumn)
    val valueColumnName = expressionBuilder.visitId(ctx.nameColumn)
    ir.Unpivot(
      child = relation,
      ids = unpivotColumns,
      values = None,
      variable_column_name = variableColumnName,
      value_column_name = valueColumnName)
  }

  override def visitTableSource(ctx: TableSourceContext): ir.LogicalPlan = {
    val tableSource = ctx.tableSourceItemJoined().accept(this)
    buildSample(ctx.sample(), tableSource)
  }

  override def visitTableSourceItemJoined(ctx: TableSourceItemJoinedContext): ir.LogicalPlan = {
    val left = ctx.objectRef().accept(this)
    ctx.joinClause().asScala.foldLeft(left)(buildJoin)
  }

  private def buildJoin(left: ir.LogicalPlan, right: JoinClauseContext): ir.Join = {
    val usingColumns = Option(right.columnList()).map(_.columnName().asScala.map(_.getText)).getOrElse(Seq())
    ir.Join(
      left,
      right.objectRef().accept(this),
      Option(right.predicate()).map(_.accept(expressionBuilder)),
      translateJoinType(right.joinType()),
      usingColumns,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
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

  override def visitCommonTableExpression(ctx: CommonTableExpressionContext): ir.LogicalPlan = {
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

  private def buildSample(ctx: SampleContext, input: ir.LogicalPlan): ir.LogicalPlan = {
    Option(ctx)
      .map { sampleCtx =>
        val seed = Option(sampleCtx.sampleSeed()).map(s => buildNum(s.num()))
        val sampleMethod = buildSampleMethod(sampleCtx.sampleMethod())
        ir.TableSample(input, sampleMethod, seed)
      }
      .getOrElse(input)
  }

  override def visitTableOrQuery(ctx: TableOrQueryContext): ir.LogicalPlan = ctx match {
    case c if c.tableRef() != null => c.tableRef().accept(this)
    case c if c.subquery() != null =>
      val subquery = c.subquery().accept(this)
      Option(c.asAlias())
        .map { a =>
          ir.SubqueryAlias(subquery, expressionBuilder.visitId(a.alias().id()), Seq())
        }
        .getOrElse(subquery)

  }
}
