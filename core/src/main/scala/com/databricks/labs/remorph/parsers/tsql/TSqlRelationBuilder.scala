package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IncompleteParser, intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

import scala.collection.JavaConverters._

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] with IncompleteParser[ir.Relation] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.Relation = ir.UnresolvedRelation(unparsedInput)

  override def visitTable_source_item(ctx: Table_source_itemContext): ir.Relation = {
    val table = ctx.full_table_name().getText
    // [TODO]: Handle Table Alias ctx.table_alias().getText
    ir.NamedTable(table, Map.empty, is_streaming = false)
  }

  override def visitTable_source(ctx: Table_sourceContext): ir.Relation = {
    val left = ctx.table_source_item().accept(this)
    // [TODO]: Handle Table Alias ctx.table_alias().getText
    ctx match {
      case c if c.join_part() != null => c.join_part().asScala.foldLeft(left)(buildJoin)
    }
  }

  private def translateJoinType(ctx: Join_onContext): ir.JoinType = {
    val joinType = ctx.join_type()
    if (joinType == null || joinType.outer_join() == null || joinType.INNER() != null) {
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
  private def buildJoin(left: ir.Relation, right: Join_partContext): ir.Join = {
    val joinExpression = right.join_on()
    val rightRelation = joinExpression.table_source().accept(this)
    val joinCondition = joinExpression.search_condition().accept(new TSqlExpressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq(),
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }

}
