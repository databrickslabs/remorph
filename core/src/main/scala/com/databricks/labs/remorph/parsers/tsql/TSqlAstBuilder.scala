package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.intermediate.TreeNode
import com.databricks.labs.remorph.parsers.tsql.TSqlParser.{DmlClauseContext, SelectStatementStandaloneContext}
import com.databricks.labs.remorph.parsers.{OptionAuto, OptionExpression, OptionOff, OptionOn, OptionString, intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

/**
 * @see
 *   org.apache.spark.sql.catalyst.parser.AstBuilder
 */
class TSqlAstBuilder extends TSqlParserBaseVisitor[ir.TreeNode] {

  private val relationBuilder = new TSqlRelationBuilder
  private val optionBuilder = new OptionBuilder(new TSqlExpressionBuilder)

  override def visitTSqlFile(ctx: TSqlParser.TSqlFileContext): ir.TreeNode = {
    Option(ctx.batch()).map(_.accept(this)).getOrElse(ir.Batch(List()))
  }

  override def visitBatch(ctx: TSqlParser.BatchContext): ir.TreeNode = {
    // TODO: Rework the tsqlFile rule
    ir.Batch(ctx.sqlClauses().asScala.map(_.accept(this)).collect { case p: ir.Plan => p })
  }

  override def visitSqlClauses(ctx: TSqlParser.SqlClausesContext): ir.TreeNode = {
    ctx match {
      case dml if dml.dmlClause() != null => dml.dmlClause().accept(this)
      case cfl if cfl.cflStatement() != null => cfl.cflStatement().accept(this)
      case another if another.anotherStatement() != null => another.anotherStatement().accept(this)
      case ddl if ddl.ddlClause() != null => ddl.ddlClause().accept(this)
      case dbcc if dbcc.dbccClause() != null => dbcc.dbccClause().accept(this)
      case backup if backup.backupStatement() != null => backup.backupStatement().accept(this)
    }
  }

  override def visitDmlClause(ctx: DmlClauseContext): ir.TreeNode = {
    // TODO: Implement the rest of the DML clauses
    ctx.selectStatementStandalone().accept(this)
  }

  /**
   * Build a complete AST for a select statement.
   * @param ctx
   *   the parse tree
   */
  override def visitSelectStatementStandalone(ctx: SelectStatementStandaloneContext): ir.TreeNode =
    ctx.accept(relationBuilder)

  override def visitBackupStatement(ctx: TSqlParser.BackupStatementContext): TreeNode = {
    ctx.backupDatabase().accept(this)
  }

  override def visitBackupDatabase(ctx: TSqlParser.BackupDatabaseContext): ir.TreeNode = {
    val database = ctx.id().getText
    val opts = ctx.optionList()
    val options = opts.asScala.flatMap(_.genericOption().asScala).toList.map(optionBuilder.buildOption)
    val (disks, boolFlags, autoFlags, values) = options.foldLeft(
      (List.empty[String], Map.empty[String, Boolean], List.empty[String], Map.empty[String, ir.Expression])) {
      case ((disks, boolFlags, autoFlags, values), option) =>
        option match {
          case OptionString("DISK", value) =>
            (value.stripPrefix("'").stripSuffix("'") :: disks, boolFlags, autoFlags, values)
          case OptionOn(id) => (disks, boolFlags + (id -> true), autoFlags, values)
          case OptionOff(id) => (disks, boolFlags + (id -> false), autoFlags, values)
          case OptionAuto(id) => (disks, boolFlags, id :: autoFlags, values)
          case OptionExpression(id, expr, _) => (disks, boolFlags, autoFlags, values + (id -> expr))
          case _ => (disks, boolFlags, autoFlags, values)
        }
    }
    // Default flags generally don't need to be specified as they are by definition, the default

    ir.BackupDatabase(database, disks, boolFlags, autoFlags, values)
  }
}
