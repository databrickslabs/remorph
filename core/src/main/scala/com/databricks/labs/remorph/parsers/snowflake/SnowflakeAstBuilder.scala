package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder extends SnowflakeParserBaseVisitor[ir.TreeNode] {

  // TODO investigate why this is needed
  override protected def aggregateResult(aggregate: ir.TreeNode, nextResult: ir.TreeNode): ir.TreeNode = {
    if (nextResult == null) {
      aggregate
    } else {
      nextResult
    }
  }

  override def visitSelect_statement(ctx: SnowflakeParser.Select_statementContext): ir.TreeNode = {
    val relation = ctx.select_optional_clauses().from_clause().accept(new SnowflakeRelationBuilder)
    val selectListElements = ctx.select_clause().select_list_no_top().select_list().select_list_elem().asScala
    val expressionVisitor = new SnowflakeExpressionBuilder
    val expressions: Seq[ir.Expression] = selectListElements.map(_.accept(expressionVisitor))
    ir.Project(relation, expressions)
  }

  override def visitLiteral(ctx: LiteralContext): ir.Literal = if (ctx.STRING() != null) {
    ir.Literal(string = Some(ctx.STRING().getText))
  } else if (ctx.DECIMAL != null) {
    visitDecimal(ctx.DECIMAL.getText)
  } else if (ctx.true_false() != null) {
    visitTrue_false(ctx.true_false())
  } else if (ctx.NULL_() != null) {
    ir.Literal(nullType = Some(ir.NullType()))
  } else {
    ir.Literal(nullType = Some(ir.NullType()))
  }

  override def visitTrue_false(ctx: True_falseContext): ir.Literal = ctx.TRUE() match {
    case null => ir.Literal(boolean = Some(false))
    case _ => ir.Literal(boolean = Some(true))
  }

  private def visitDecimal(decimal: String) = BigDecimal(decimal) match {
    case d if d.isValidInt => ir.Literal(integer = Some(d.toInt))
    case d if d.isValidLong => ir.Literal(long = Some(d.toLong))
    case d if d.isValidShort => ir.Literal(short = Some(d.toShort))
    case d if d.isDecimalFloat || d.isExactFloat => ir.Literal(float = Some(d.toFloat))
    case d if d.isDecimalDouble || d.isExactDouble => ir.Literal(double = Some(d.toDouble))
    case _ => ir.Literal(decimal = Some(ir.Decimal(decimal, None, None)))
  }
}

class SnowflakeRelationBuilder extends SnowflakeParserBaseVisitor[ir.Relation] {
  override def visitObject_ref(ctx: SnowflakeParser.Object_refContext): ir.Relation = {
    val tableName = ctx.object_name().id_(0).getText
    ir.NamedTable(tableName, Map.empty, is_streaming = false)
  }

  override def visitTable_source_item_joined(ctx: Table_source_item_joinedContext): ir.Relation = {
    def buildJoin(left: ir.Relation, right: SnowflakeParser.Join_clauseContext): ir.Join = {
      ir.Join(left, right.object_ref().accept(this), None, ir.InnerJoin, Seq(), ir.JoinDataType(false, false))
    }
    val left = ctx.object_ref().accept(this)
    ctx.join_clause().asScala.foldLeft(left)(buildJoin)
  }

}

class SnowflakeExpressionBuilder extends SnowflakeParserBaseVisitor[ir.Expression] {

  override def visitSelect_list_elem(ctx: SnowflakeParser.Select_list_elemContext): ir.Expression = {
    val column = ctx.column_elem().accept(this)
    if (ctx.as_alias() != null) {
      ctx.as_alias().accept(this) match {
        case ir.Alias(_, name, metadata) => ir.Alias(column, name, metadata)
        case _ => null
      }
    } else {
      column
    }
  }
  override def visitColumn_name(ctx: SnowflakeParser.Column_nameContext): ir.Expression = {
    ir.Column(ctx.id_(0).getText)
  }

  override def visitAs_alias(ctx: SnowflakeParser.As_aliasContext): ir.Expression = {
    val alias = ctx.alias().id_().getText
    ir.Alias(null, Seq(alias), None)
  }
}
