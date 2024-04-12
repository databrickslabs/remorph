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

  override def visitSelect_statement(ctx: Select_statementContext): ir.TreeNode = {
    val relation = ctx.select_optional_clauses().accept(new SnowflakeRelationBuilder)
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

  override def visitSelect_optional_clauses(ctx: Select_optional_clausesContext): ir.Relation = {
    val from = ctx.from_clause().accept(this)
    val where = if (ctx.where_clause() != null) {
      val predicate = ctx.where_clause().search_condition().accept(new SnowflakePredicateBuilder)
      ir.Filter(from, predicate)
    } else {
      from
    }
    if (ctx.group_by_clause() != null) {
      val groupingExpressions =
        ctx.group_by_clause().group_by_list().group_by_elem().asScala.map(_.accept(new SnowflakeExpressionBuilder))
        ir.Aggregate(
          input = where,
          group_type = ir.GroupBy,
          grouping_expressions = groupingExpressions,
          pivot = None
        )

    } else {
      where
    }
  }
  override def visitObject_ref(ctx: SnowflakeParser.Object_refContext): ir.Relation = {
    val tableName = ctx.object_name().id_(0).getText
    ir.NamedTable(tableName, Map.empty, is_streaming = false)
  }

  override def visitTable_source_item_joined(ctx: Table_source_item_joinedContext): ir.Relation = {

    def translateJoinType(joinType: SnowflakeParser.Join_typeContext): ir.JoinType = {
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

    def buildJoin(left: ir.Relation, right: SnowflakeParser.Join_clauseContext): ir.Join = {




  override def visitSelect_list_elem(ctx: SnowflakeParser.Select_list_elemContext): ir.Expression = {
    if (ctx.column_elem() != null) {
      val column = ctx.column_elem().accept(this)
      if (ctx.as_alias() != null) {
        ctx.as_alias().accept(this) match {
          case ir.Alias(_, name, metadata) => ir.Alias(column, name, metadata)
          case _ => null
        }
      } else {
        column
      }
    } else if (ctx.expression_elem() != null) {
      ctx.expression_elem().accept(this)
    } else {
      null
    }
  }
  override def visitColumn_name(ctx: SnowflakeParser.Column_nameContext): ir.Expression = {
    ir.Column(ctx.id_(0).getText)
  }

  override def visitAs_alias(ctx: SnowflakeParser.As_aliasContext): ir.Expression = {
    val alias = ctx.alias().id_().getText
    ir.Alias(null, Seq(alias), None)
  }

  override def visitAggregate_function(ctx: Aggregate_functionContext): Expression = {
    val param = ctx.expr_list().accept(this)
    val functionName = ctx.id_().builtin_function()
    if (functionName.COUNT() != null) {
      ir.Count(param)
    } else {
      null
    }
  }


  override def visitPrimitive_expression(ctx: Primitive_expressionContext): ir.Expression = {
    val columnName = ctx.id_(0).getText
    ir.Column(columnName)
  }
}

class SnowflakePredicateBuilder extends SnowflakeParserBaseVisitor[ir.Predicate] {
  override def visitExpr(ctx: ExprContext): ir.Predicate = {

    def buildComparison(left: ir.Expression, right: ir.Expression, op: Comparison_operatorContext): ir.Predicate = {
      if (op.EQ() != null) {
        ir.Equals(left, right)
      } else if (op.NE() != null || op.LTGT() != null) {
        ir.NotEquals(left, right)
      } else if (op.GT() != null) {
        ir.GreaterThan(left, right)
      } else if (op.LT() != null) {
        ir.LesserThan(left, right)
      } else if (op.GE() != null) {
        ir.GreaterThanOrEqual(left, right)
      } else if (op.LE() != null) {
        ir.LesserThanOrEqual(left, right)
      } else {
        // TODO: better error management
        null
      }
    }

    if (ctx.AND() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.And(left, right)
    } else if (ctx.OR() != null) {
      val left = ctx.expr(0).accept(this)
      val right = ctx.expr(1).accept(this)
      ir.Or(left, right)
    } else if (ctx.comparison_operator() != null) {
      val left = ctx.expr(0).accept(new SnowflakeExpressionBuilder)
      val right = ctx.expr(1).accept(new SnowflakeExpressionBuilder)
      buildComparison(left, right, ctx.comparison_operator())
    } else {
      // TODO: better error management
      null
    }
  }

  override def visitSearch_condition(ctx: Search_conditionContext): ir.Predicate = {
    val pred = ctx.predicate().accept(this)
    // TODO: investigate why NOT() is a list here
    if (ctx.NOT().size() > 0) {
      ir.Not(pred)
    } else {
      pred
    }
  }

}
