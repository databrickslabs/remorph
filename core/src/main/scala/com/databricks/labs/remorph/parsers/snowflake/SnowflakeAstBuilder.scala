package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => _, _}
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters._

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class SnowflakeAstBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.LogicalPlan]
    with ParserCommon[ir.LogicalPlan] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.LogicalPlan =
    ir.UnresolvedRelation(ruleText = ruleText, message = message)

  // Concrete visitors

  override def visitSnowflakeFile(ctx: SnowflakeFileContext): ir.LogicalPlan = {
    // This very top level visitor does not ignore any valid statements for the batch, instead
    // we prepend any errors to the batch plan, so they are generated first in the output.
    val errors = errorCheck(ctx)
    val batchPlan = Option(ctx.batch()).map(buildBatch).getOrElse(Seq.empty)
    errors match {
      case Some(errorResult) => ir.Batch(errorResult +: batchPlan)
      case None => ir.Batch(batchPlan)
    }
  }

  private def buildBatch(ctx: BatchContext): Seq[ir.LogicalPlan] = {
    // This very top level visitor does not ignore any valid statements for the batch, instead
    // we prepend any errors to the batch plan, so they are generated first in the output.
    val errors = errorCheck(ctx)
    val statements = visitMany(ctx.sqlClauses())
    errors match {
      case Some(errorResult) => errorResult +: statements
      case None => statements
    }
  }

  override def visitSqlClauses(ctx: SqlClausesContext): ir.LogicalPlan = {
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        ctx match {
          case c if c.ddlCommand() != null => c.ddlCommand().accept(this)
          case c if c.dmlCommand() != null => c.dmlCommand().accept(this)
          case c if c.showCommand() != null => c.showCommand().accept(this)
          case c if c.useCommand() != null => c.useCommand().accept(this)
          case c if c.describeCommand() != null => c.describeCommand().accept(this)
          case c if c.otherCommand() != null => c.otherCommand().accept(this)
          case c if c.snowSqlCommand() != null => c.snowSqlCommand().accept(this)
          case _ =>
            ir.UnresolvedCommand(
              ruleText = contextText(ctx),
              ruleName = vc.ruleName(ctx),
              tokenName = Some(tokenName(ctx.getStart)),
              message = "Unknown command in SnowflakeAstBuilder.visitSqlCommand")
        }
    }
  }

  // TODO: Sort out where to visitSubquery
  override def visitQueryStatement(ctx: QueryStatementContext): ir.LogicalPlan = {
    errorCheck(ctx).getOrElse {
      val query = ctx.queryExpression().accept(this)
      Option(ctx.withExpression()).foldRight(query)(buildCTE)
    }
  }

  override def visitQueryInParenthesis(ctx: QueryInParenthesisContext): ir.LogicalPlan = {
    errorCheck(ctx).getOrElse(ctx.queryExpression().accept(this))
  }

  override def visitQueryIntersect(ctx: QueryIntersectContext): ir.LogicalPlan = {
    errorCheck(ctx).getOrElse {
      val Seq(lhs, rhs) = ctx.queryExpression().asScala.map(_.accept(this))
      ir.SetOperation(lhs, rhs, ir.IntersectSetOp, is_all = false, by_name = false, allow_missing_columns = false)
    }
  }

  override def visitQueryUnion(ctx: QueryUnionContext): ir.LogicalPlan = {
    errorCheck(ctx).getOrElse {
      val Seq(lhs, rhs) = ctx.queryExpression().asScala.map(_.accept(this))
      val setOp = ctx match {
        case u if u.UNION() != null => ir.UnionSetOp
        case e if e.EXCEPT() != null || e.MINUS_() != null => ir.ExceptSetOp
      }
      val isAll = ctx.ALL() != null
      ir.SetOperation(lhs, rhs, setOp, is_all = isAll, by_name = false, allow_missing_columns = false)
    }
  }

  override def visitQuerySimple(ctx: QuerySimpleContext): ir.LogicalPlan = {
    errorCheck(ctx).getOrElse(ctx.selectStatement().accept(vc.relationBuilder))
  }

  override def visitDdlCommand(ctx: DdlCommandContext): ir.LogicalPlan =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        ctx.accept(vc.ddlBuilder)
    }

  private def buildCTE(ctx: WithExpressionContext, relation: ir.LogicalPlan): ir.LogicalPlan = {
    if (ctx == null) {
      return relation
    }
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        if (ctx.RECURSIVE() == null) {
          val ctes = vc.relationBuilder.visitMany(ctx.commonTableExpression())
          ir.WithCTE(ctes, relation)
        } else {
          // TODO With Recursive CTE are not support by default, will require a custom implementation IR to be redefined
          val ctes = vc.relationBuilder.visitMany(ctx.commonTableExpression())
          ir.WithRecursiveCTE(ctes, relation)
        }
    }
  }

  override def visitDmlCommand(ctx: DmlCommandContext): ir.LogicalPlan =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        ctx match {
          case c if c.queryStatement() != null => c.queryStatement().accept(this)
          case c => c.accept(vc.dmlBuilder)
        }
    }

  override def visitOtherCommand(ctx: OtherCommandContext): ir.LogicalPlan =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        ctx.accept(vc.commandBuilder)
    }

  override def visitSnowSqlCommand(ctx: SnowSqlCommandContext): ir.LogicalPlan = {
    ir.UnresolvedCommand(
      ruleText = contextText(ctx),
      ruleName = vc.ruleName(ctx),
      tokenName = Some(tokenName(ctx.getStart)),
      message = "Unknown command in SnowflakeAstBuilder.visitSnowSqlCommand")
  }
}
