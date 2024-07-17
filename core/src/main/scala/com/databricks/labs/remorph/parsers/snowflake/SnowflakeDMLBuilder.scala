package com.databricks.labs.remorph.parsers.snowflake

import SnowflakeParser._
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}
import scala.collection.JavaConverters._

class SnowflakeDMLBuilder extends SnowflakeParserBaseVisitor[ir.Modification] with ParserCommon[ir.Modification] {

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
    val otherSources = ctx.tableOrQuery().asScala.map(_.accept(relationBuilder))
    val source = if (otherSources.nonEmpty) {
      Some(
        otherSources.foldLeft(target)(
          ir.Join(_, _, None, ir.CrossJoin, Seq(), ir.JoinDataType(is_left_struct = false, is_right_struct = false))))
    } else {
      None
    }
    ir.DeleteFromTable(target, source, where, None, None)
  }
}
