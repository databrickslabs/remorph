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

  /**
   * Note that SELECT a, b, c FROM x, y, z is equivalent to SELECT a, b, c FROM x CROSS JOIN y CROSS JOIN z
   * @param ctx
   *   the parse tree
   */
  override def visitTableSources(ctx: TSqlParser.TableSourcesContext): ir.Relation = {
    val relations = ctx.tableSource().asScala.toList.map(_.accept(this)).collect { case r: ir.Relation => r }
    relations match {
      case head :: Nil => head
      case head :: tail =>
        tail.foldLeft(head)((acc, relation) =>
          ir.Join(
            acc,
            relation,
            None,
            ir.CrossJoin,
            Seq.empty,
            ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
      case Nil => ir.NoTable()
    }
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val left = ctx.tableSourceItem().accept(this)
    // [TODO]: Handle Table Alias ctx.tableAlias().getText
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoin)
    }
  }

  private def translateJoinType(ctx: JoinOnContext): ir.JoinType = ctx.joinType() match {
    case jt if jt == null || jt.outerJoin() == null || jt.INNER() != null => ir.InnerJoin
    case jt if jt.outerJoin().LEFT() != null => ir.LeftOuterJoin
    case jt if jt.outerJoin().RIGHT() != null => ir.RightOuterJoin
    case jt if jt.outerJoin().FULL() != null => ir.FullOuterJoin
    case _ => ir.UnspecifiedJoin
  }

  private def buildJoin(left: ir.Relation, right: JoinPartContext): ir.Join = {
    val joinExpression = right.joinOn()
    val rightRelation = joinExpression.tableSource().accept(this)
    val joinCondition = joinExpression.searchCondition().accept(new TSqlColumnBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }
}
