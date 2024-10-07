package com.databricks.labs.remorph.parsers.snowflake

import SnowflakeParser._
import com.databricks.labs.remorph.parsers.intermediate.IRHelpers
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}

import scala.collection.JavaConverters._

class SnowflakeDMLBuilder
    extends SnowflakeParserBaseVisitor[ir.Modification]
    with ParserCommon[ir.Modification]
    with IRHelpers {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val relationBuilder = new SnowflakeRelationBuilder

  override def visitInsertStatement(ctx: InsertStatementContext): ir.Modification = {
    val table = ctx.objectName().accept(relationBuilder)
    val columns = Option(ctx.ids).map(_.asScala).filter(_.nonEmpty).map(_.map(expressionBuilder.visitId))
    val values = ctx match {
      case c if c.queryStatement() != null => c.queryStatement().accept(relationBuilder)
      case c if c.valuesTableBody() != null => c.valuesTableBody().accept(relationBuilder)
    }
    val overwrite = ctx.OVERWRITE() != null
    ir.InsertIntoTable(table, columns, values, None, None, overwrite)
  }

  override def visitDeleteStatement(ctx: DeleteStatementContext): ir.Modification = {
    val target = ctx.tableRef().accept(relationBuilder)
    val where = Option(ctx.predicate()).map(_.accept(expressionBuilder))
    Option(ctx.tablesOrQueries()) match {
      case Some(value) =>
        val relation = relationBuilder.visit(value)
        ir.MergeIntoTable(target, relation, where.getOrElse(ir.Noop), matchedActions = Seq(ir.DeleteAction(None)))
      case None => ir.DeleteFromTable(target, where = where)
    }
  }

  override def visitUpdateStatement(ctx: UpdateStatementContext): ir.Modification = {
    val target = ctx.tableRef().accept(relationBuilder)
    val set = expressionBuilder.visitMany(ctx.setColumnValue())
    val sources =
      Option(ctx.tableSources()).map(t => relationBuilder.visitMany(t.tableSource()).foldLeft(target)(crossJoin))
    val where = Option(ctx.predicate()).map(_.accept(expressionBuilder))
    ir.UpdateTable(target, sources, set, where, None, None)
  }

  override def visitMergeStatement(ctx: MergeStatementContext): ir.Modification = {
    val target = ctx.tableRef().accept(relationBuilder)
    val relation = ctx.tableSource().accept(relationBuilder)
    val predicate = ctx.predicate().accept(expressionBuilder)
    val matchedActions = ctx
      .mergeCond()
      .mergeCondMatch()
      .asScala
      .map(buildMergeAction)

    val notMatchedActions = ctx
      .mergeCond()
      .mergeCondNotMatch()
      .asScala
      .map(buildInsertAction)

    ir.MergeIntoTable(
      target,
      relation,
      predicate,
      matchedActions = matchedActions,
      notMatchedActions = notMatchedActions)
  }

  private def buildMergeAction(ctx: MergeCondMatchContext): ir.MergeAction = {
    val condition = Option(ctx.predicate().accept(expressionBuilder))

    ctx match {
      case d if d.mergeUpdateDelete().DELETE() != null =>
        ir.DeleteAction(condition)
      case u if u.mergeUpdateDelete().UPDATE() != null =>
        val assign = u
          .mergeUpdateDelete()
          .setColumnValue()
          .asScala
          .map(expressionBuilder.visitSetColumnValue)
          .map { case a: ir.Assign =>
            a
          }
        ir.UpdateAction(condition, assign)
    }

  }

  private def buildInsertAction(ctx: MergeCondNotMatchContext): ir.MergeAction = {
    val condition = Option(ctx.predicate().accept(expressionBuilder))
    val assignments = Option(
      ctx
        .mergeInsert()
        .columnList()
        .columnName()
        .asScala
        .map(_.accept(expressionBuilder))
        .zip(
          ctx
            .mergeInsert()
            .exprList()
            .expr()
            .asScala
            .map(_.accept(expressionBuilder)))
        .map { case (col, value) =>
          ir.Assign(col, value)
        }).getOrElse(Seq.empty[ir.Assign])

    ir.InsertAction(condition, assignments)
  }

}
