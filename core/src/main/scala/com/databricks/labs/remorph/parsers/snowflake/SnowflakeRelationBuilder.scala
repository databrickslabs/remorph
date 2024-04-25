package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.{IncompleteParser, intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters._

class SnowflakeRelationBuilder extends SnowflakeParserBaseVisitor[ir.Relation] with IncompleteParser[ir.Relation] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.Relation = ir.UnresolvedRelation(unparsedInput)
  override def visitSelect_statement(ctx: Select_statementContext): ir.Relation = {
    val select = ctx.select_optional_clauses().accept(this)
    val relation = buildLimitOffset(ctx.limit_clause(), select)
    val (top, allOrDistinct, selectListElements) = ctx match {
      case c if ctx.select_clause() != null =>
        (
          None,
          c.select_clause().select_list_no_top().all_distinct(),
          c.select_clause().select_list_no_top().select_list().select_list_elem().asScala)
      case c if ctx.select_top_clause() != null =>
        (
          Option(c.select_top_clause().select_list_top().top_clause()),
          c.select_top_clause().select_list_top().all_distinct(),
          c.select_top_clause().select_list_top().select_list().select_list_elem().asScala)
    }
    val expressions = selectListElements.map(_.accept(new SnowflakeExpressionBuilder))
    ir.Project(buildTop(top, buildDistinct(allOrDistinct, relation, expressions)), expressions)

  }

  private def buildLimitOffset(ctx: Limit_clauseContext, input: ir.Relation): ir.Relation = {
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
      ctx: All_distinctContext,
      input: ir.Relation,
      projectExpressions: Seq[ir.Expression]): ir.Relation =
    if (Option(ctx).exists(_.DISTINCT() != null)) {
      val columnNames = projectExpressions.collect {
        case ir.Column(c) => Seq(c)
        case ir.Alias(_, a, _) => a
      }.flatten
      ir.Deduplicate(input, columnNames, all_columns_as_keys = columnNames.isEmpty, within_watermark = false)
    } else {
      input
    }

  private def buildTop(ctxOpt: Option[Top_clauseContext], input: ir.Relation): ir.Relation =
    ctxOpt.fold(input) { top =>
      ir.Limit(input, top.num().getText.toInt)
    }

  override def visitSelect_optional_clauses(ctx: Select_optional_clausesContext): ir.Relation = {
    val from = ctx.from_clause().accept(this)
    buildOrderBy(
      ctx.order_by_clause(),
      buildQualify(
        ctx.qualify_clause(),
        buildHaving(ctx.having_clause(), buildGroupBy(ctx.group_by_clause(), buildWhere(ctx.where_clause(), from)))))
  }

  private def buildFilter[A](ctx: A, conditionRule: A => ParserRuleContext, input: ir.Relation): ir.Relation =
    Option(ctx).fold(input) { c =>
      ir.Filter(input, conditionRule(c).accept(new SnowflakeExpressionBuilder))
    }
  private def buildHaving(ctx: Having_clauseContext, input: ir.Relation): ir.Relation =
    buildFilter[Having_clauseContext](ctx, _.search_condition(), input)

  private def buildQualify(ctx: Qualify_clauseContext, input: ir.Relation): ir.Relation =
    buildFilter[Qualify_clauseContext](ctx, _.expr(), input)
  private def buildWhere(ctx: Where_clauseContext, from: ir.Relation): ir.Relation =
    buildFilter[Where_clauseContext](ctx, _.search_condition(), from)

  private def buildGroupBy(ctx: Group_by_clauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val groupingExpressions =
        c.group_by_list().group_by_elem().asScala.map(_.accept(new SnowflakeExpressionBuilder))
      val aggregate =
        ir.Aggregate(input = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
      buildHaving(c.having_clause(), aggregate)
    }
  }

  private def buildOrderBy(ctx: Order_by_clauseContext, input: ir.Relation): ir.Relation = {
    Option(ctx).fold(input) { c =>
      val sortOrders = c.order_item().asScala.map { orderItem =>
        val expression = orderItem.accept(new SnowflakeExpressionBuilder)
        if (orderItem.DESC() == null) {
          if (orderItem.NULLS() != null && orderItem.FIRST() != null) {
            ir.SortOrder(expression, ir.AscendingSortDirection, ir.SortNullsFirst)
          } else {
            ir.SortOrder(expression, ir.AscendingSortDirection, ir.SortNullsLast)
          }
        } else {
          if (orderItem.NULLS() != null && orderItem.FIRST() != null) {
            ir.SortOrder(expression, ir.DescendingSortDirection, ir.SortNullsFirst)
          } else {
            ir.SortOrder(expression, ir.DescendingSortDirection, ir.SortNullsLast)
          }
        }
      }
      ir.Sort(input = input, order = sortOrders, is_global = false)
    }
  }

  override def visitObject_ref(ctx: Object_refContext): ir.Relation = {
    val tableName = ctx.object_name().id_(0).getText
    val table = ir.NamedTable(tableName, Map.empty, is_streaming = false)
    buildPivotOrUnpivot(ctx.pivot_unpivot(), table)
  }

  private def buildPivotOrUnpivot(ctx: Pivot_unpivotContext, relation: ir.Relation): ir.Relation = {
    if (ctx == null) {
      relation
    } else if (ctx.PIVOT() != null) {
      buildPivot(ctx, relation)
    } else {
      buildUnpivot(ctx, relation)
    }
  }

  private def buildPivot(ctx: Pivot_unpivotContext, relation: ir.Relation): ir.Relation = {
    val pivotValues: Seq[ir.Literal] = ctx.literal().asScala.map(_.accept(new SnowflakeExpressionBuilder)).collect {
      case lit: ir.Literal => lit
    }
    val pivotColumn = ir.Column(ctx.id_(2).getText)
    val aggregateFunction = translateAggregateFunction(ctx.id_(0), ctx.id_(1))
    ir.Aggregate(
      input = relation,
      group_type = ir.Pivot,
      grouping_expressions = Seq(aggregateFunction),
      pivot = Some(ir.Pivot(pivotColumn, pivotValues)))
  }

  private def buildUnpivot(ctx: Pivot_unpivotContext, relation: ir.Relation): ir.Relation = {
    val unpivotColumns = ctx.column_list().column_name().asScala.map(_.accept(new SnowflakeExpressionBuilder))
    val variableColumnName = ctx.id_(0).getText
    val valueColumnName = ctx.column_name().id_(0).getText
    ir.Unpivot(
      input = relation,
      ids = unpivotColumns,
      values = None,
      variable_column_name = variableColumnName,
      value_column_name = valueColumnName)
  }

  private def translateAggregateFunction(aggFunc: Id_Context, parameter: Id_Context): ir.Expression = {
    val column = ir.Column(parameter.getText)
    if (aggFunc.builtin_function() != null) {
      if (aggFunc.builtin_function().SUM() != null) {
        ir.Sum(column)
      } else if (aggFunc.builtin_function().AVG() != null) {
        ir.Avg(column)
      } else if (aggFunc.builtin_function().COUNT() != null) {
        ir.Count(column)
      } else if (aggFunc.builtin_function().MIN() != null) {
        ir.Min(column)
      } else {
        null
      }
    } else {
      null
    }
  }
  override def visitTable_source_item_joined(ctx: Table_source_item_joinedContext): ir.Relation = {

    def buildJoin(left: ir.Relation, right: Join_clauseContext): ir.Join = {

      ir.Join(
        left,
        right.object_ref().accept(this),
        None,
        translateJoinType(right.join_type()),
        Seq(),
        ir.JoinDataType(is_left_struct = false, is_right_struct = false))
    }
    val left = ctx.object_ref().accept(this)
    ctx.join_clause().asScala.foldLeft(left)(buildJoin)
  }

  private def translateJoinType(joinType: Join_typeContext): ir.JoinType = {
    if (joinType == null || joinType.outer_join() == null) {
      ir.InnerJoin
    } else if (joinType.outer_join().LEFT() != null) {
      ir.LeftOuterJoin
    } else if (joinType.outer_join().RIGHT() != null) {
      ir.RightOuterJoin
    } else if (joinType.outer_join().FULL() != null) {
      ir.FullOuterJoin
    } else {
      ir.UnspecifiedJoin
    }
  }

  override def visitCommon_table_expression(ctx: Common_table_expressionContext): ir.Relation = {
    val tableName = ctx.id_().getText
    val columns = ctx.column_list().column_name().asScala.map(_.accept(new SnowflakeExpressionBuilder))
    val query = ctx.select_statement().accept(this)
    ir.CTEDefinition(tableName, columns, query)
  }
}
