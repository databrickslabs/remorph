package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{OptionAuto, OptionExpression, OptionOff, OptionOn, OptionString, ParserCommon, intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlDDLBuilder(optionBuilder: OptionBuilder)
    extends TSqlParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog] {

  override def visitCreateTable(ctx: TSqlParser.CreateTableContext): ir.Catalog =
    ctx match {
      case ci if ci.createInternal() != null => ci.createInternal().accept(this)
      case ct if ct.createExternal() != null => ct.createExternal().accept(this)
      case _ => ir.UnresolvedCatalog(ctx.getText)
    }

  override def visitCreateInternal(ctx: TSqlParser.CreateInternalContext): ir.Catalog = {
//    val tableName = ctx.tableName().getText
//    val columns = ctx.columnDefTableConstraints().columnDefTableConstraint().asScala.map(_.accept(this))
//    val lock = Option(ctx.simpleId()).map(_.accept(this))
//    val ctas = Option(ctx.createTableAs()).map(_.accept(this))
//    val options = Option(ctx.tableOptions(1)).map(_.accept(this))
//    val partitionOn = Option(ctx.onPartitionOrFilegroup()).map(_.accept(this))

    // TODO: Where are we getting CreateTable ir from? The current one in Catalog seesm wrong and the one for
    //       Snowflake is not close to covering everything that TSQL has.
    ir.UnresolvedCatalog(ctx.getText)
  }

  override def visitCreateExternal(ctx: TSqlParser.CreateExternalContext): ir.Catalog = {
//    val tableName = ctx.tableName().getText
//    val columns = ctx.columnDefTableConstraints().columnDefTableConstraint().asScala.map(_.accept(this))
    // TODO: build options
    ir.UnresolvedCatalog(ctx.getText)
  }

  /**
   * This is not actually implemented but was a quick way to exercise the genericOption builder before we had other
   * syntax implemented to test it with.
   *
   * @param ctx
   *   the parse tree
   */
  override def visitBackupStatement(ctx: TSqlParser.BackupStatementContext): ir.Catalog =
    ctx.backupDatabase().accept(this)

  override def visitBackupDatabase(ctx: TSqlParser.BackupDatabaseContext): ir.Catalog = {
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
    BackupDatabase(database, disks, boolFlags, autoFlags, values)
  }

}
