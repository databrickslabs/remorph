package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.intermediate.IRHelpers
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters._

class SnowflakeDMLBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.Modification]
    with ParserCommon[ir.Modification]
    with IRHelpers {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Modification =
    ir.UnresolvedModification(ruleText = ruleText, message = message)

  // Concrete visitors

  override def visitDmlCommand(ctx: DmlCommandContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case q if q.queryStatement() != null => q.queryStatement().accept(this)
        case i if i.insertStatement() != null => i.insertStatement().accept(this)
        case i if i.insertMultiTableStatement() != null => i.insertMultiTableStatement().accept(this)
        case u if u.updateStatement() != null => u.updateStatement().accept(this)
        case d if d.deleteStatement() != null => d.deleteStatement().accept(this)
        case m if m.mergeStatement() != null => m.mergeStatement().accept(this)
        case _ => unresolved("dmlCommand", "everything is null")
      }
  }

  override def visitInsertStatement(ctx: InsertStatementContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val table = ctx.dotIdentifier().accept(vc.relationBuilder)
      val columns = Option(ctx.ids).map(_.asScala).filter(_.nonEmpty).map(_.map(vc.expressionBuilder.buildId))
      val values = ctx match {
        case c if c.queryStatement() != null => c.queryStatement().accept(vc.relationBuilder)
        case c if c.valuesTableBody() != null => c.valuesTableBody().accept(vc.relationBuilder)
      }
      val overwrite = ctx.OVERWRITE() != null
      ir.InsertIntoTable(table, columns, values, None, None, overwrite)
  }

  override def visitDeleteStatement(ctx: DeleteStatementContext): ir.Modification =
    errorCheck(ctx) match {
      case Some(errorResult) => errorResult
      case None =>
        val target = ctx.tableRef().accept(vc.relationBuilder)
        val where = Option(ctx.searchCondition()).map(_.accept(vc.expressionBuilder))
        Option(ctx.tablesOrQueries()) match {
          case Some(value) =>
            val relation = vc.relationBuilder.visit(value)
            ir.MergeIntoTable(target, relation, where.getOrElse(ir.Noop), matchedActions = Seq(ir.DeleteAction(None)))
          case None => ir.DeleteFromTable(target, where = where)
        }
    }

  override def visitUpdateStatement(ctx: UpdateStatementContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val target = ctx.tableRef().accept(vc.relationBuilder)
      val set = vc.expressionBuilder.visitMany(ctx.setColumnValue())
      val sources =
        Option(ctx.tableSources()).map(t => vc.relationBuilder.visitMany(t.tableSource()).foldLeft(target)(crossJoin))
      val where = Option(ctx.searchCondition()).map(_.accept(vc.expressionBuilder))
      ir.UpdateTable(target, sources, set, where, None, None)
  }

  override def visitMergeStatement(ctx: MergeStatementContext): ir.Modification = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val target = ctx.tableRef().accept(vc.relationBuilder)
      val relation = ctx.tableSource().accept(vc.relationBuilder)
      val predicate = ctx.searchCondition().accept(vc.expressionBuilder)
      val matchedActions = ctx
        .mergeCond()
        .mergeCondMatch()
        .asScala
        .map(buildMatchAction)

      val notMatchedActions = ctx
        .mergeCond()
        .mergeCondNotMatch()
        .asScala
        .map(buildNotMatchAction)

      ir.MergeIntoTable(
        target,
        relation,
        predicate,
        matchedActions = matchedActions,
        notMatchedActions = notMatchedActions)
  }

  private def buildMatchAction(ctx: MergeCondMatchContext): ir.MergeAction = {
    val condition = ctx match {
      case c if c.searchCondition() != null => Some(c.searchCondition().accept(vc.expressionBuilder))
      case _ => None
    }

    ctx match {
      case d if d.mergeUpdateDelete().DELETE() != null =>
        ir.DeleteAction(condition)
      case u if u.mergeUpdateDelete().UPDATE() != null =>
        val assign = u
          .mergeUpdateDelete()
          .setColumnValue()
          .asScala
          .map(vc.expressionBuilder.visitSetColumnValue)
          .map { case a: ir.Assign =>
            a
          }
        ir.UpdateAction(condition, assign)
    }

  }

  private def buildNotMatchAction(ctx: MergeCondNotMatchContext): ir.MergeAction = {
    val condition = ctx match {
      case c if c.searchCondition() != null => Some(c.searchCondition().accept(vc.expressionBuilder))
      case _ => None
    }
    ctx match {
      case c if c.mergeInsert().columnList() != null =>
        val assignment = c
          .mergeInsert()
          .columnList()
          .columnName()
          .asScala
          .map(_.accept(vc.expressionBuilder))
          .zip(
            c
              .mergeInsert()
              .exprList()
              .expr()
              .asScala
              .map(_.accept(vc.expressionBuilder)))
          .map { case (col, value) =>
            ir.Assign(col, value)
          }

        ir.InsertAction(condition, assignment)

      case _ => ir.InsertAction(condition, Seq.empty[ir.Assign])
    }
  }
}
