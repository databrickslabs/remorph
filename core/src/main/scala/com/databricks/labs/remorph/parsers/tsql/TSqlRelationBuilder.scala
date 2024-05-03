package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{IncompleteParser, intermediate => ir}
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._

import scala.collection.JavaConverters._

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] with IncompleteParser[ir.Relation] {

  protected override def wrapUnresolvedInput(unparsedInput: String): ir.Relation = ir.UnresolvedRelation(unparsedInput)

  override def visitTableSourceItem(ctx: TableSourceItemContext): ir.Relation = {
    val table = ctx.fullTableName().getText
    // [TODO]: Handle Table Alias ctx.tableAlias().getText
    ir.NamedTable(table, Map.empty, is_streaming = false)
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val left = ctx.tableSourceItem().accept(this)
    // [TODO]: Handle Table Alias ctx.tableAlias().getText
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoin)
    }
  }

  private def translateJoinType(ctx: JoinOnContext): ir.JoinType = {
    val joinType = ctx.joinType()
    if (joinType == null || joinType.outerJoin() == null || joinType.INNER() != null) {
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
  private def buildJoin(left: ir.Relation, right: JoinPartContext): ir.Join = {
    val joinExpression = right.joinOn()
    val rightRelation = joinExpression.tableSource().accept(this)
    val joinCondition = joinExpression.searchCondition().accept(new TSqlExpressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq(),
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }
}
