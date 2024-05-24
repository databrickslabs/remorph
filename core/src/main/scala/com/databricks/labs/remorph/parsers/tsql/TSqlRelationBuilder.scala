package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlRelationBuilder extends TSqlParserBaseVisitor[ir.Relation] {

  override def visitSelectStatementStandalone(ctx: TSqlParser.SelectStatementStandaloneContext): ir.Relation = {

    // TODO: Process ctx.WithExpression
    ctx.selectStatement().accept(this)
  }

  override def visitSelectStatement(ctx: TSqlParser.SelectStatementContext): ir.Relation = {
    // TODO: val orderByClause = Option(ctx.selectOrderByClause).map(_.accept(this))
    // TODO: val forClause = Option(ctx.forClause).map(_.accept(this))
    // TODO: val optionClause = Option(ctx.optionClause).map(_.accept(this))

    ctx.queryExpression.accept(this)
  }

  override def visitQuerySpecification(ctx: TSqlParser.QuerySpecificationContext): ir.Relation = {

    // TODO: Process all the other elements of a query specification

    val columns =
      ctx.selectListElem().asScala.map(_.accept(new TSqlExpressionBuilder()))
    val from = Option(ctx.tableSources()).map(_.accept(new TSqlRelationBuilder)).getOrElse(ir.NoTable)

    ir.Project(from, columns)
  }

  override def visitTableName(ctx: TableNameContext): ir.NamedTable = {
    val linkedServer = Option(ctx.linkedServer).map(_.getText)
    val ids = ctx.ids.asScala.map(_.getText).mkString(".")
    val fullName = linkedServer.fold(ids)(ls => s"$ls..$ids")
    ir.NamedTable(fullName, Map.empty, is_streaming = false)
  }

  /**
   * Note that SELECT a, b, c FROM x, y, z is equivalent to SELECT a, b, c FROM x CROSS JOIN y CROSS JOIN z
   * @param ctx
   *   the parse tree
   */
  override def visitTableSources(ctx: TSqlParser.TableSourcesContext): ir.Relation = {
    val relations = ctx.tableSource().asScala.toList.map(_.accept(this)).collect { case r: ir.Relation => r }
    relations match {
      case head :: tail =>
        tail.foldLeft(head)((acc, relation) =>
          ir.Join(
            acc,
            relation,
            None,
            ir.CrossJoin,
            Seq.empty,
            ir.JoinDataType(is_left_struct = false, is_right_struct = false)))
      case _ => ir.NoTable
    }
  }

  override def visitTableSource(ctx: TableSourceContext): ir.Relation = {
    val left = ctx.tableSourceItem().accept(this)
    ctx match {
      case c if c.joinPart() != null => c.joinPart().asScala.foldLeft(left)(buildJoin)
    }
  }

  // TODO: note that not all table source items have fullTableName
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
    val joinCondition = joinExpression.searchCondition().accept(new TSqlExpressionBuilder)

    ir.Join(
      left,
      rightRelation,
      Some(joinCondition),
      translateJoinType(joinExpression),
      Seq.empty,
      ir.JoinDataType(is_left_struct = false, is_right_struct = false))
  }
}
