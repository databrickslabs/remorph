package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{LocationTracking, ParserCommon}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.snowflake.rules.InlineColumnExpression
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters._

class SnowflakeRelationBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.WithKnownLocationRange[ir.LogicalPlan]]
    with ParserCommon[ir.LogicalPlan]
    with LocationTracking {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.WithKnownLocationRange[ir.LogicalPlan] =
    withLocationRangeFromParseTree(currentNode.getRuleContext) {
      ir.UnresolvedRelation(ruleText = ruleText, message = message)
    }

  // Concrete visitors

  override def visitSelectStatement(ctx: SelectStatementContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          // Note that the optional select clauses may be null on very simple statements
          // such as SELECT 1;
          withLocationRangeFromRuleContext(ctx) {
            val select = Option(ctx.selectOptionalClauses()).map(_.accept(this)).getOrElse(ir.NoTable())
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

              // NOte that we must cater for error recovery where neither clause is present
              case _ => (None, null, Seq.empty)
            }
            val expressions = selectListElements.map(_.accept(vc.expressionBuilder))

            if (Option(allOrDistinct).exists(_.DISTINCT() != null)) {
              buildTop(top, buildDistinct(relation, expressions))
            } else {
              ir.Project(buildTop(top, relation), expressions /*, Some(Origin.fromParserRuleContext(ctx))*/ )
            }
          }
      }
    }
  }

  private def buildLimitOffset(
      ctx: LimitClauseContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        if (ctx.LIMIT() != null) {
          val limit = ir.Limit(input, ctx.expr(0).accept(vc.expressionBuilder))
          if (ctx.OFFSET() != null) {
            ir.Offset(limit, ctx.expr(1).accept(vc.expressionBuilder))
          } else {
            limit
          }
        } else {
          ir.Offset(input, ctx.expr(0).accept(vc.expressionBuilder))
        }
      }
    }
  }

  private def buildDistinct(input: ir.LogicalPlan, projectExpressions: Seq[ir.Expression]): ir.LogicalPlan = {
    val columnNames = projectExpressions.collect {
      case ir.Id(i, _) => i
      case ir.Column(_, c) => c
      case ir.Alias(_, a) => a
    }
    ir.Deduplicate(input, projectExpressions, columnNames.isEmpty, within_watermark = false)
  }

  private def buildTop(ctxOpt: Option[TopClauseContext], input: ir.LogicalPlan): ir.LogicalPlan =
    ctxOpt.fold(input) { top =>
      ir.Limit(input, top.expr().accept(vc.expressionBuilder))
    }

  override def visitSelectOptionalClauses(
      ctx: SelectOptionalClausesContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val from = Option(ctx.fromClause()).map(_.accept(this)).getOrElse(ir.NoTable())
          buildOrderBy(
            ctx.orderByClause(),
            buildQualify(
              ctx.qualifyClause(),
              buildHaving(ctx.havingClause(), buildGroupBy(ctx.groupByClause(), buildWhere(ctx.whereClause(), from)))))
      }
    }
  }

  override def visitFromClause(ctx: FromClauseContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val tableSources = visitMany(ctx.tableSources().tableSource())
          // The tableSources seq cannot be empty (as empty FROM clauses are not allowed
          tableSources match {
            case Seq(tableSource) => tableSource
            case sources =>
              sources.reduce(
                ir.Join(
                  _,
                  _,
                  None,
                  ir.InnerJoin,
                  Seq(),
                  ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
          }
      }
    }
  }

  private def buildFilter[A <: ParserRuleContext](
      ctx: A,
      conditionRule: A => ParserRuleContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] =
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        ir.Filter(input, conditionRule(ctx).accept(vc.expressionBuilder))
      }
    }

  private def buildHaving(ctx: HavingClauseContext, input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] =
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        buildFilter[HavingClauseContext](ctx, _.searchCondition(), input)
      }
    }

  private def buildQualify(
      ctx: QualifyClauseContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] =
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        buildFilter[QualifyClauseContext](ctx, _.expr(), input)
      }
    }

  private def buildWhere(ctx: WhereClauseContext, from: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] =
    if (ctx == null) {
      from.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        buildFilter[WhereClauseContext](ctx, _.searchCondition(), from)
      }
    }

  private def buildGroupBy(
      ctx: GroupByClauseContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        val groupingExpressions =
          Option(ctx.groupByList()).toSeq
            .flatMap(_.groupByElem().asScala)
            .map(_.accept(vc.expressionBuilder))
        val groupType = if (ctx.ALL() != null) ir.GroupByAll else ir.GroupBy
        val aggregate =
          ir.Aggregate(child = input, group_type = groupType, grouping_expressions = groupingExpressions, pivot = None)
        buildHaving(ctx.havingClause(), aggregate)
      }
    }
  }

  private def buildOrderBy(
      ctx: OrderByClauseContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        val sortOrders = ctx.orderItem().asScala.map(vc.expressionBuilder.visitOrderItem)
        ir.Sort(input, sortOrders, is_global = false)
      }
    }
  }

  override def visitObjRefTableFunc(ctx: ObjRefTableFuncContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val tableFunc = ir.TableFunction(ctx.functionCall().accept(vc.expressionBuilder))
          buildSubqueryAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), tableFunc))
      }
    }
  }

  // @see https://docs.snowflake.com/en/sql-reference/functions/flatten
  // @see https://docs.snowflake.com/en/sql-reference/functions-table
  override def visitObjRefSubquery(ctx: ObjRefSubqueryContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val relation = ctx match {
            case c if c.subquery() != null => c.subquery().accept(this)
            case c if c.functionCall() != null => ir.TableFunction(c.functionCall().accept(vc.expressionBuilder))
          }
          val maybeLateral = if (ctx.LATERAL() != null) {
            ir.Lateral(relation)
          } else {
            relation
          }
          buildSubqueryAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), maybeLateral))
      }
    }
  }

  private def buildSubqueryAlias(
      ctx: TableAliasContext,
      input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        ir.SubqueryAlias(
          input,
          vc.expressionBuilder.buildId(ctx.alias().id()),
          ctx.id().asScala.map(vc.expressionBuilder.buildId))
      }
    }
  }

  override def visitValuesTable(ctx: ValuesTableContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          ctx.valuesTableBody().accept(this)
      }
    }
  }

  override def visitValuesTableBody(ctx: ValuesTableBodyContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val expressions =
            ctx
              .exprListInParentheses()
              .asScala
              .map(l => vc.expressionBuilder.visitMany(l.exprList().expr()))
          ir.Values(expressions)
      }
    }
  }

  override def visitObjRefDefault(ctx: ObjRefDefaultContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          buildTableAlias(ctx.tableAlias(), buildPivotOrUnpivot(ctx.pivotUnpivot(), ctx.dotIdentifier().accept(this)))
      }
    }
  }

  override def visitTableRef(ctx: TableRefContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val table = ctx.dotIdentifier().accept(this)
          Option(ctx.asAlias())
            .map { a =>
              ir.TableAlias(table, a.alias().getText, Seq())
            }
            .getOrElse(table)
      }
    }
  }

  override def visitDotIdentifier(ctx: DotIdentifierContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val tableName = ctx.id().asScala.map(vc.expressionBuilder.buildId).map(_.id).mkString(".")
          ir.NamedTable(tableName, Map.empty, is_streaming = false)
      }
    }
  }

  override def visitObjRefValues(ctx: ObjRefValuesContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val values = ctx.valuesTable().accept(this)
          buildTableAlias(ctx.tableAlias(), values)
      }
    }
  }

  private def buildTableAlias(
      ctx: TableAliasContext,
      relation: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      relation.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        val alias = ctx.alias().getText
        val columns = Option(ctx.id()).map(_.asScala.map(vc.expressionBuilder.buildId)).getOrElse(Seq.empty)
        ir.TableAlias(relation, alias, columns)
      }
    }
  }

  private def buildPivotOrUnpivot(
      ctx: PivotUnpivotContext,
      relation: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      relation.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        if (ctx.PIVOT() != null) {
          buildPivot(ctx, relation)
        } else {
          buildUnpivot(ctx, relation)
        }
      }
    }
  }

  private def buildPivot(
      ctx: PivotUnpivotContext,
      relation: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      val pivotValues: Seq[ir.Literal] =
        vc.expressionBuilder.visitMany(ctx.values).collect { case lit: ir.Literal => lit }
      val argument = ir.Column(None, vc.expressionBuilder.buildId(ctx.pivotColumn))
      val column = ir.Column(None, vc.expressionBuilder.buildId(ctx.valueColumn))
      val aggFunc = vc.expressionBuilder.buildId(ctx.aggregateFunc)
      val aggregateFunction = vc.functionBuilder.buildFunction(aggFunc, Seq(argument))
      ir.Aggregate(
        child = relation,
        group_type = ir.Pivot,
        grouping_expressions = Seq(aggregateFunction),
        pivot = Some(ir.Pivot(column, pivotValues)))
    }
  }

  private def buildUnpivot(
      ctx: PivotUnpivotContext,
      relation: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      val unpivotColumns = ctx
        .columnList()
        .columnName()
        .asScala
        .map(_.accept(vc.expressionBuilder))
      val variableColumnName = vc.expressionBuilder.buildId(ctx.valueColumn)
      val valueColumnName = vc.expressionBuilder.buildId(ctx.nameColumn)
      ir.Unpivot(
        child = relation,
        ids = unpivotColumns,
        values = None,
        variable_column_name = variableColumnName,
        value_column_name = valueColumnName)
    }
  }

  override def visitTableSource(ctx: TableSourceContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val tableSource = ctx match {
            case c if c.tableSourceItemJoined() != null => c.tableSourceItemJoined().accept(this)
            case c if c.tableSource() != null => c.tableSource().accept(this)
          }
          buildSample(ctx.sample(), tableSource)
      }
    }
  }

  override def visitTableSourceItemJoined(
      ctx: TableSourceItemJoinedContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          val left = ctx.objectRef().accept(this).asInstanceOf[ir.LogicalPlan]
          ctx.joinClause().asScala.foldLeft(left)(buildJoin)
      }
    }
  }

  private def buildJoin(left: ir.LogicalPlan, right: JoinClauseContext): ir.Join = {
    val usingColumns = Option(right.columnList()).map(_.columnName().asScala.map(_.getText)).getOrElse(Seq())
    val joinType = if (right.NATURAL() != null) {
      ir.NaturalJoin(translateOuterJoinType(right.outerJoin()))
    } else if (right.CROSS() != null) {
      ir.CrossJoin
    } else {
      translateJoinType(right.joinType())
    }
    ir.Join(
      left,
      right.objectRef().accept(this),
      Option(right.searchCondition()).map(_.accept(vc.expressionBuilder)),
      joinType,
      usingColumns,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))

  }

  private[snowflake] def translateJoinType(joinType: JoinTypeContext): ir.JoinType = {
    Option(joinType)
      .map { jt =>
        if (jt.INNER() != null) {
          ir.InnerJoin
        } else {
          translateOuterJoinType(jt.outerJoin())
        }
      }
      .getOrElse(ir.UnspecifiedJoin)
  }

  private def translateOuterJoinType(ctx: OuterJoinContext): ir.JoinType = {
    Option(ctx)
      .collect {
        case c if c.LEFT() != null => ir.LeftOuterJoin
        case c if c.RIGHT() != null => ir.RightOuterJoin
        case c if c.FULL() != null => ir.FullOuterJoin
      }
      .getOrElse(ir.UnspecifiedJoin)
  }

  override def visitCTETable(ctx: CTETableContext): ir.WithKnownLocationRange[ir.LogicalPlan] =
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx).getOrElse {
        val tableName = vc.expressionBuilder.buildId(ctx.tableName)
        val columns = ctx.columnList() match {
          case null => Seq.empty[ir.Id]
          case c => c.columnName().asScala.flatMap(_.id.asScala.map(vc.expressionBuilder.buildId))
        }

        val query = ctx.selectStatement().accept(this)
        ir.SubqueryAlias(query, tableName, columns)

      }
    }

  override def visitCTEColumn(ctx: CTEColumnContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      InlineColumnExpression(vc.expressionBuilder.buildId(ctx.id()), ctx.expr().accept(vc.expressionBuilder))
    }
  }

  private def buildSampleMethod(ctx: SampleMethodContext): ir.SamplingMethod = {
    ctx match {
      case c: SampleMethodRowFixedContext => ir.RowSamplingFixedAmount(BigDecimal(c.INT().getText))
      case c: SampleMethodRowProbaContext => ir.RowSamplingProbabilistic(BigDecimal(c.INT().getText))
      case c: SampleMethodBlockContext => ir.BlockSampling(BigDecimal(c.INT().getText))
    }
  }

  private def buildSample(ctx: SampleContext, input: ir.LogicalPlan): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    if (ctx == null) {
      input.asInstanceOf[ir.WithKnownLocationRange[ir.LogicalPlan]]
    } else {
      withLocationRangeFromRuleContext(ctx) {
        val seed = Option(ctx.sampleSeed()).map(s => BigDecimal(s.INT().getText))
        val sampleMethod = buildSampleMethod(ctx.sampleMethod())
        ir.TableSample(input, sampleMethod, seed)
      }
    }
  }

  override def visitTableOrQuery(ctx: TableOrQueryContext): ir.WithKnownLocationRange[ir.LogicalPlan] = {
    withLocationRangeFromRuleContext(ctx) {
      errorCheck(ctx) match {
        case Some(errorResult) => errorResult
        case None =>
          ctx match {
            case c if c.tableRef() != null => c.tableRef().accept(this)
            case c if c.subquery() != null =>
              val subquery = c.subquery().accept(this)
              Option(c.asAlias())
                .map { a =>
                  ir.SubqueryAlias(subquery, vc.expressionBuilder.buildId(a.alias().id()), Seq())
                }
                .getOrElse(subquery)

          }
      }
    }
  }
}
