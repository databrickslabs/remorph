package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.Relation
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] {

  private val expressionBuilder = new TSqlExpressionBuilder

  override def visitCommonTableExpression(ctx: CommonTableExpressionContext): Relation = {
    val tableName = ctx.id().getText
    // Column list can be empty if the select specifies distinct column names
    val columns =
      Option(ctx.columnNameList())
        .map(_.id().asScala.map(id => ir.Column(None, expressionBuilder.visitId(id))))
        .getOrElse(List.empty)
    val query = ctx.selectStatement().accept(this)
    ir.CTEDefinition(tableName, columns, query)
  }

  override def visitSelectStatementStandalone(ctx: TSqlParser.SelectStatementStandaloneContext): ir.Relation = {
    val query = ctx.selectStatement().accept(this)
    Option(ctx.withExpression())
      .map { withExpression =>
        val ctes = withExpression.commonTableExpression().asScala.map(_.accept(this))
        ir.WithCTE(ctes, query)
      }
      .getOrElse(query)
  }

  override def visitSelectStatement(ctx: TSqlParser.SelectStatementContext): ir.Relation = {
    // TODO: val forClause = Option(ctx.forClause).map(_.accept(this))
    // TODO: val optionClause = Option(ctx.optionClause).map(_.accept(this))

    ctx.queryExpression.accept(this)
  }

  override def visitQuerySpecification(ctx: TSqlParser.QuerySpecificationContext): ir.Relation = {

    // TODO: Check the logic here for all the elements of a query specification
    val select = ctx.selectOptionalClauses().accept(this)

    val columns =
      ctx.selectListElem().asScala.map(_.accept(expressionBuilder))
    // Note that ALL is the default so we don't need to check for it
    ctx match {
      case c if c.DISTINCT() != null =>
        buildDistinct(select, columns)
      case _ =>
        ir.Project(select, columns)
    }
  }

  override def visitSelectOptionalClauses(ctx: SelectOptionalClausesContext): ir.Relation = {
    val from = Option(ctx.fromClause()).map(_.accept(this)).getOrElse(ir.NoTable())
    buildOrderBy(
      ctx.selectOrderByClause(),
      buildHaving(ctx.havingClause(), buildGroupBy(ctx.groupByClause(), buildWhere(ctx.whereClause(), from))))
  }

  private def buildFilter[A](ctx: A, conditionRule: A => ParserRuleContext, input: ir.Relation): ir.Relation =
    Option(ctx).fold(input) { c =>
      ir.Filter(input, conditionRule(c).accept(expressionBuilder))
    }
  private def buildHaving(ctx: HavingClauseContext, input: ir.Relation): ir.Relation =
    buildFilter[HavingClauseContext](ctx, _.searchCondition(), input)

  private def buildWhere(ctx: WhereClauseContext, from: ir.Relation): ir.Relation =
    buildFilter[WhereClauseContext](ctx, _.searchCondition(), from)

  // TODO: We are not catering for GROUPING SETS here, or in Snowflake
  private def buildGroupBy(ctx: GroupByClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val groupingExpressions =
        c.expression()
          .asScala
          .map(_.accept(expressionBuilder))
      ir.Aggregate(input = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
    }
  }

  // TODO: COLLATE in OrderBy expression
  // TODO: OFFSET and FETCH in selectOrderByClause
  private def buildOrderBy(ctx: SelectOrderByClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.orderByClause().orderByExpression().asScala.map { orderItem =>
        val expression = orderItem.expression(0).accept(expressionBuilder) // expression(1) is COLLATE
        if (orderItem.DESC() == null) {
          ir.SortOrder(expression, ir.AscendingSortDirection, ir.SortNullsUnspecified)
        } else {
          ir.SortOrder(expression, ir.DescendingSortDirection, ir.SortNullsUnspecified)
        }
      }
      ir.Sort(input = input, order = sortOrders, is_global = false)
    }
  }

  override def visitFromClause(ctx: FromClauseContext): ir.Relation = {
    val tableSources = ctx.tableSources().tableSource().asScala.map(_.accept(this))
    // The tableSources seq cannot be empty (as empty FROM clauses are not allowed
    tableSources match {
      case Seq(tableSource) => tableSource
      case sources =>
        sources.reduce(
          ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
    }
  }

  private def buildDistinct(from: ir.Relation, columns: Seq[ir.Expression]): ir.Relation = {
    val columnNames = columns.collect {
      case ir.Column(_, c) => Seq(c)
      case ir.Alias(_, a, _) => a
      // Note that the ir.Star(None) is not matched so that we set all_columns_as_keys to true
    }.flatten
    ir.Project(
      ir.Deduplicate(from, columnNames, all_columns_as_keys = columnNames.isEmpty, within_watermark = false),
      columns)
  }

  override def visitTableName(ctx: TableNameContext): ir.NamedTable = {
    val linkedServer = Option(ctx.linkedServer).map(_.getText)
    val ids = ctx.ids.asScala.map(_.getText).mkString(".")
    val fullName = linkedServer.fold(ids)(ls => s"$ls..$ids")
    ir.NamedTable(fullName, Map.empty, is_streaming = false)
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val left = ctx.tableSourceItem().accept(this)
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoin)
    }
  }

  // TODO: note that not all table source items have tableName
  override def visitTableSourceItem(ctx: TableSourceItemContext): ir.Relation =
    Option(ctx.asTableAlias())
      .map(alias => ir.TableAlias(ctx.tableName().accept(this), alias.id.getText))
      .getOrElse(ctx.tableName().accept(this))

  private[tsql] def translateJoinType(ctx: JoinOnContext): ir.JoinType = ctx.joinType() match {
    case jt if jt == null || jt.outerJoin() == null || jt.INNER() != null => ir.InnerJoin
    case jt if jt.outerJoin().LEFT() != null => ir.LeftOuterJoin
    case jt if jt.outerJoin().RIGHT() != null => ir.RightOuterJoin
    case jt if jt.outerJoin().FULL() != null => ir.FullOuterJoin
    case _ => ir.UnspecifiedJoin
  }

  private def buildJoin(left: ir.Relation, right: JoinPartContext): ir.Join = {
    val joinExpression = right.joinOn()
    val rightRelation = joinExpression.tableSource().accept(this)
    val joinCondition = joinExpression.searchCondition().accept(expressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }
}
