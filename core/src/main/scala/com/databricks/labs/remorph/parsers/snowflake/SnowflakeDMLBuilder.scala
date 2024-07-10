package com.databricks.labs.remorph.parsers.snowflake

import SnowflakeParser._
import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}
import scala.collection.JavaConverters._

class SnowflakeDMLBuilder extends SnowflakeParserBaseVisitor[ir.Command] with ParserCommon[ir.Command] {

  private val expressionBuilder = new SnowflakeExpressionBuilder
  private val relationBuilder = new SnowflakeRelationBuilder

  override def visitInsertStatement(ctx: InsertStatementContext): ir.Command = {
    val table = ctx.objectName().accept(expressionBuilder)
    val columns = Option(ctx.ids).map(_.asScala).getOrElse(Seq()).map(expressionBuilder.visitId)
    val values = ctx match {
      case c if c.queryStatement() != null => c.queryStatement().accept(relationBuilder)
      case c if c.valuesTableBody() != null => c.valuesTableBody().accept(relationBuilder)
    }
    val overwrite = ctx.OVERWRITE() != null
    ir.Insert(table, columns, values, overwrite)
  }
}
