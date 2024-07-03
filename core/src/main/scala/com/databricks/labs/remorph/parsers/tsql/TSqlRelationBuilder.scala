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
    // TODO: The FOR clause of TSQL is not supported in Databricks SQL as XML and JSON are not supported
    //       in the same way. We probably need to raise an error here that can be used by some sort of linter

    // We visit the OptionClause because in the future, we may be able to glean information from it
    // as an aid to migration, however the clause is not used in the AST or translation.
    Option(ctx.optionClause).map(_.accept(expressionBuilder))

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
        ir.Project(buildTop(Option(ctx.topClause()), buildDistinct(select, columns)), columns)
      case _ =>
        ir.Project(buildTop(Option(ctx.topClause()), select), columns)
    }
  }

  private def buildTop(ctxOpt: Option[TSqlParser.TopClauseContext], input: ir.Relation): ir.Relation =
    ctxOpt.fold(input) { top =>
      ir.Limit(
        input,
        top.expression().accept(expressionBuilder),
        is_percentage = top.PERCENT() != null,
        with_ties = top.TIES() != null)
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

  private def buildOrderBy(ctx: SelectOrderByClauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.orderByClause().orderByExpression().asScala.map { orderItem =>
        val expression = orderItem.expression(0).accept(expressionBuilder)
        // orderItem.expression(1) is COLLATE - we will not support that, but should either add a comment in the
        // translated source or raise some kind of linting alert.
        if (orderItem.DESC() == null) {
          ir.SortOrder(expression, ir.AscendingSortDirection, ir.SortNullsUnspecified)
        } else {
          ir.SortOrder(expression, ir.DescendingSortDirection, ir.SortNullsUnspecified)
        }
      }
      val sorted = ir.Sort(input = input, order = sortOrders, is_global = false)

      // Having created the IR for ORDER BY, we now need to apply any OFFSET, and then any FETCH
      if (ctx.OFFSET() != null) {
        val offset = ir.Offset(sorted, ctx.expression(0).accept(expressionBuilder))
        if (ctx.FETCH() != null) {
          ir.Limit(offset, ctx.expression(1).accept(expressionBuilder))
        } else {
          offset
        }
      } else {
        sorted
      }
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
    ir.Deduplicate(from, columnNames, all_columns_as_keys = columnNames.isEmpty, within_watermark = false),
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
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoinPart)
    }
  }

  // TODO: note that not all table source items have tableName
  override def visitTableSourceItem(ctx: TableSourceItemContext): ir.Relation =
    Option(ctx.asTableAlias())
      .map(alias => ir.TableAlias(ctx.tableName().accept(this), alias.id.getText))
      .getOrElse(ctx.tableName().accept(this))

  private def buildJoinPart(left: ir.Relation, ctx: JoinPartContext): ir.Relation = {
    ctx match {
      case c if c.joinOn() != null => buildJoinOn(left, c.joinOn())
      case c if c.crossJoin() != null => buildCrossJoin(left, c.crossJoin())
      case c if c.apply() != null => buildApply(left, c.apply())
      case c if c.pivot() != null => buildPivot(left, c.pivot())
      case _ => buildUnpivot(left, ctx.unpivot()) // Only case left
    }
  }

  private def buildUnpivot(left: Relation, ctx: UnpivotContext): ir.Relation = {
    val unpivotColumns = ctx
      .unpivotClause()
      .fullColumnNameList()
      .fullColumnName()
      .asScala
      .map(_.accept(expressionBuilder))
    val variableColumnName = expressionBuilder.visitId(ctx.unpivotClause().id(0))
    val valueColumnName = expressionBuilder.visitId(ctx.unpivotClause().id(1))
    ir.Unpivot(
      input = left,
      ids = unpivotColumns,
      values = None,
      variable_column_name = variableColumnName,
      value_column_name = valueColumnName)
  }

  private def buildPivot(left: Relation, ctx: PivotContext): ir.Relation = {
    // Though the pivotClause allows expression, it must be a function call and we require
    // correct source code to be given to remorph.
    val aggregateFunction = ctx.pivotClause().expression().accept(expressionBuilder)
    val column = ctx.pivotClause().fullColumnName().accept(expressionBuilder)
    val values = ctx.pivotClause().columnAliasList().columnAlias().asScala.map(c => buildLiteral(c.getText))
    ir.Aggregate(
      input = left,
      group_type = ir.Pivot,
      grouping_expressions = Seq(aggregateFunction),
      pivot = Some(ir.Pivot(column, values)))
  }

  private def buildLiteral(str: String): ir.Literal =
    ir.Literal(string = Some(removeQuotesAndBrackets(str)))

  private def buildApply(left: Relation, ctx: ApplyContext): ir.Relation = {
    val rightRelation = ctx.tableSourceItem().accept(this)
    ir.Join(
      left,
      rightRelation,
      None,
      if (ctx.CROSS() != null) ir.CrossApply else ir.OuterApply,
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private def buildCrossJoin(left: Relation, ctx: CrossJoinContext): ir.Relation = {
    val rightRelation = ctx.tableSourceItem().accept(this)
    ir.Join(
      left,
      rightRelation,
      None,
      ir.CrossJoin,
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private def buildJoinOn(left: ir.Relation, ctx: JoinOnContext): ir.Join = {
    val rightRelation = ctx.tableSource().accept(this)
    val joinCondition = ctx.searchCondition().accept(expressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(ctx),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

  private[tsql] def translateJoinType(ctx: JoinOnContext): ir.JoinType = ctx.joinType() match {
    case jt if jt == null || jt.outerJoin() == null || jt.INNER() != null => ir.InnerJoin
    case jt if jt.outerJoin().LEFT() != null => ir.LeftOuterJoin
    case jt if jt.outerJoin().RIGHT() != null => ir.RightOuterJoin
    case jt if jt.outerJoin().FULL() != null => ir.FullOuterJoin
    case _ => ir.UnspecifiedJoin
  }

  private def removeQuotesAndBrackets(str: String): String = {
    val quotations = Map('\'' -> "'", '"' -> "\"", '[' -> "]", '\\' -> "\\")
    str match {
      case s if s.length < 2 => s
      case s =>
        quotations.get(s.head).fold(s) { closingQuote =>
          if (s.endsWith(closingQuote)) {
            s.substring(1, s.length - 1)
          } else {
            s
          }
        }
    }
  }
}
