package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder extends SnowflakeParserBaseVisitor[ir.LogicalPlan] with ParserCommon[ir.LogicalPlan] {

  private val relationBuilder = new SnowflakeRelationBuilder
  private val ddlBuilder = new SnowflakeDDLBuilder
  private val dmlBuilder = new SnowflakeDMLBuilder
  private val commandBuilder = new SnowflakeCommandBuilder

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(msg: String): ir.LogicalPlan = {
    ir.UnresolvedRelation(msg)
  }

  // Concrete visitors

  override def visitSnowflakeFile(ctx: SnowflakeFileContext): ir.LogicalPlan =
    Option(ctx.batch()).map(_.accept(this)).getOrElse(ir.Batch(Seq.empty))

  override def visitBatch(ctx: BatchContext): ir.LogicalPlan =
    ir.Batch(visitMany(ctx.sqlCommand()))

  override def visitSqlCommand(ctx: SqlCommandContext): ir.LogicalPlan = {
    ctx match {
      case c if c.ddlCommand() != null => c.ddlCommand().accept(this)
      case c if c.dmlCommand() != null => c.dmlCommand().accept(this)
      case c if c.showCommand() != null => c.showCommand().accept(this)
      case c if c.useCommand() != null => c.useCommand().accept(this)
      case c if c.describeCommand() != null => c.describeCommand().accept(this)
      case c if c.otherCommand() != null => c.otherCommand().accept(this)
      case c if c.snowSqlCommand() != null => c.snowSqlCommand().accept(this)
      case _ => ir.UnresolvedCommand(contextText(ctx))
    }
  }

  // TODO: Sort out where to visitSubquery
  override def visitQueryStatement(ctx: QueryStatementContext): ir.LogicalPlan = {
    val select = ctx.selectStatement().accept(relationBuilder)
    val withCTE = buildCTE(ctx.withExpression(), select)
    ctx.setOperators().asScala.foldLeft(withCTE)(buildSetOperator)
  }

  override def visitDdlCommand(ctx: DdlCommandContext): ir.LogicalPlan =
    ctx.accept(ddlBuilder)

  private def buildCTE(ctx: WithExpressionContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    if (ctx == null) {
      return relation
    }
    val ctes = relationBuilder.visitMany(ctx.commonTableExpression())
    ir.WithCTE(ctes, relation)
  }

  private def buildSetOperator(left: ir.LogicalPlan, ctx: SetOperatorsContext): ir.LogicalPlan = {
    val right = ctx.selectStatement().accept(relationBuilder)
    val (isAll, setOp) = ctx match {
      case c if c.UNION() != null =>
        (c.ALL() != null, ir.UnionSetOp)
      case c if c.MINUS_() != null || c.EXCEPT() != null =>
        (false, ir.ExceptSetOp)
      case c if c.INTERSECT() != null =>
        (false, ir.IntersectSetOp)
    }
    ir.SetOperation(left, right, setOp, is_all = isAll, by_name = false, allow_missing_columns = false)
  }

  override def visitDmlCommand(ctx: DmlCommandContext): ir.LogicalPlan = ctx match {
    case c if c.queryStatement() != null => c.queryStatement().accept(this)
    case c => c.accept(dmlBuilder)
  }

  override def visitOtherCommand(ctx: OtherCommandContext): ir.LogicalPlan = {
    ctx.accept(commandBuilder)
  }

  override def visitSnowSqlCommand(ctx: SnowSqlCommandContext): ir.LogicalPlan = {
    ir.UnresolvedCommand(contextText(ctx))
  }
}
