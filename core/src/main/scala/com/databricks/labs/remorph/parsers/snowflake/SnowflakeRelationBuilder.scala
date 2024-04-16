package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.Relation
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._

import scala.collection.JavaConverters._

class SnowflakeRelationBuilder extends SnowflakeParserBaseVisitor[ir.Relation] {

  override def visitSelect_optional_clauses(ctx: Select_optional_clausesContext): ir.Relation = {
    val from = ctx.from_clause().accept(this)
    buildOrderBy(ctx, buildGroupBy(ctx, buildWhere(ctx, from)))
  }

  private def buildWhere(ctx: Select_optional_clausesContext, from: Relation): Relation =
    if (ctx.where_clause() != null) {
      val predicate = ctx.where_clause().search_condition().accept(new SnowflakePredicateBuilder)
      ir.Filter(from, predicate)
    } else {
      from
    }

  private def buildGroupBy(ctx: Select_optional_clausesContext, input: Relation): Relation =
    if (ctx.group_by_clause() != null) {
      val groupingExpressions =
        ctx.group_by_clause().group_by_list().group_by_elem().asScala.map(_.accept(new SnowflakeExpressionBuilder))
      ir.Aggregate(input = input, group_type = ir.GroupBy, grouping_expressions = groupingExpressions, pivot = None)
    } else {
      input
    }

  private def buildOrderBy(ctx: Select_optional_clausesContext, input: Relation): Relation =
    if (ctx.order_by_clause() != null) {
      val sortOrders = ctx.order_by_clause().order_item().asScala.map { orderItem =>
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
    } else {
      input
    }

  override def visitObject_ref(ctx: Object_refContext): ir.Relation = {
    val tableName = ctx.object_name().id_(0).getText
    ir.NamedTable(tableName, Map.empty, is_streaming = false)
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

}
