package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{GenericOption, OptionAuto, OptionExpression, OptionOff, OptionOn, OptionString, ParserCommon, intermediate => ir}
import com.databricks.labs.remorph.utils.ParsingUtils

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlDDLBuilder(optionBuilder: OptionBuilder)
    extends TSqlParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog] {

  private val dataTypeBuilder: DataTypeBuilder = new DataTypeBuilder

  override def visitCreateTable(ctx: TSqlParser.CreateTableContext): ir.Catalog =
    ctx match {
      case ci if ci.createInternal() != null => ci.createInternal().accept(this)
      case ct if ct.createExternal() != null => ct.createExternal().accept(this)
      case _ => ir.UnresolvedCatalog(ctx.getText)
    }

  override def visitCreateInternal(ctx: TSqlParser.CreateInternalContext): ir.Catalog = {
    val tableName = ctx.tableName().getText
    val columns = Seq.newBuilder[ir.StructField]
    val constraints = Seq.newBuilder[ir.Constraint]
    val indices = Seq.newBuilder[ir.CreateIndex]

    ctx.columnDefTableConstraints().columnDefTableConstraint().asScala.map {
      case constraint if constraint.columnDefinition() != null =>
        val col = buildColumnDeclaration(constraint.columnDefinition())
        columns += (col.name -> col)
      case constraint if constraint.computedColumnDefinition() != null =>
        val col = buildComputedColumn(constraint.computedColumnDefinition())
        columns += (col.name -> col)
      case constraint if constraint.tableConstraint() != null =>
        constraints += constraint.tableConstraint().accept(this)
      case constraint if constraint.tableIndices() != null =>
        indices += constraint.tableIndices().accept(this)
    }

    val schema = ir.StructType(columns.result())

    val indicesResult = indices.result()
    val createTable = indicesResult match {
      case i if i.isEmpty => ir.CreateTable(tableName, None, None, None, Some(columns.values.toSeq), None)
      case _ =>
        ir.WithIndices(ir.CreateTable(tableName, None, None, None, Some(columns.values.toSeq), None), indicesResult)
    }
    val lock = Option(ctx.simpleId()).map(_.accept(this))
    val ctas = Option(ctx.createTableAs()).map(_.accept(this))
    val options = Option(ctx.tableOptions(1)).map(_.accept(this))
    val partitionOn = Option(ctx.onPartitionOrFilegroup()).map(_.accept(this))

    ir.UnresolvedCatalog(ctx.getText)
  }

  override def visitCreateExternal(ctx: TSqlParser.CreateExternalContext): ir.Catalog = {
//    val tableName = ctx.tableName().getText
//    val columns = ctx.columnDefTableConstraints().columnDefTableConstraint().asScala.map(_.accept(this))
    // TODO: build options
    ir.UnresolvedCatalog(ctx.getText)
  }

  /**
   * Because TSQL is a LOT more involved than databricks, we need to build a more complex representation of column
   * declarations than we would in Databricks SQL and then transform these complex definitions into the simpler
   * Databricks SQL representation higher up.
   *
   * @param context
   *   parser context
   * @return
   *   a complex column declaration
   */
  private def buildColumnDeclaration(context: TSqlParser.ColumnDefinitionContext): ir.ColumnDeclaration = {

    val options = Seq.newBuilder[GenericOption]
    val constraints = Seq.newBuilder[ir.Constraint]
    val tableConstraints = Seq.newBuilder[ir.Constraint]

    var nullable: Option[Boolean] = None
    var defaultValue: Option[ir.Expression] = None

    if (context.columnDefinitionElement() != null) {
      context.columnDefinitionElement().asScala.foreach { element =>
        element match {
          case rg if rg.ROWGUIDCOL() != null =>
            // ROWGUID is supported in Databricks SQL
            options += OptionOn("ROWGUIDCOL")

          case d if d.defaultValue() != null =>
            // Databricks SQL does not support the naming of the DEFAULT CONSTRAINT, so we will just use the default
            // expression we are given, but if there is a name, we will store it as a comment
            defaultValue = Some(d.defaultValue().expression().accept(expressionBuilder))
            if (d.defaultValue().id() != null) {
              options += OptionUnresolved(
                s"Databricks SQL cannot name the DEFAULT CONSTRAINT ${d.defaultValue().id().getText}")
            }

          case c if c.columnConstraint() != null =>
            // For some reason TSQL supports the naming of NOT NULL constraints, but if it is named
            // we can generate a check constraint that is named to enforce the NOT NULL constraint.
            if (c.columnConstraint().NULL() != null) {
              nullable = if (c.columnConstraint().NOT() != null) {

                if (c.columnConstraint().id() != null) {
                  // If the nullable constraint is named, then we will generate a table level CHECK constraint
                  // to enforce it.
                  // So we will use true here so NOT NULL it is not specified in the column definition, then the
                  // table level CHECK can be named and therefore altered and dropped from the table as per TSQL.
                  tableConstraints += ir.NamedConstraint(
                    c.columnConstraint().id().getText,
                    ir.CheckConstraint(ir.IsNotNull(ir.Column(None, ir.Id(context.id().getText)))))
                  Some(true)
                } else {
                  Some(false)
                }
              } else {
                Some(true)
              }
            } else {
              constraints += buildColumnConstraint(c.columnConstraint())
            }

          case d if d.identityColumn() != null =>
            // IDENTITY is supported in Databricks SQL but is done via GENERATED constraint
            constraints += ir.IdentityConstraint(d.identityColumn().INT(0).getText, d.identityColumn().INT(1).getText)

          // Unsupported stuff
          case m if m.MASKED() != null =>
            // MASKED WITH FUNCTION = 'functionName' is not supported in Databricks SQL
            options += OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(m)}")

          case f if f.ENCRYPTED() != null =>
            // ENCRYPTED WITH ... is not supported in Databricks SQL
            options += OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(f)}")

          case o if o.genericOption() != null =>
            options += OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(o)}")
        }
      }
    }
    val dataType = dataTypeBuilder.build(context.dataType())
    val sf = ir.StructField(context.id().getText, dataType, nullable.getOrElse(true))

    // TODO: index options

    ir.ColumnDeclaration(sf, defaultValue, constraints.result(), options.result())
  }

  /**
   * Builds a column constraint such as PRIMARY KEY, UNIQUE, FOREIGN KEY, CHECK
   *
   * Note that TSQL is way more involved than Databricks SQL and we must record all the different options so that we can
   * at least generate a comment.
   *
   * @param ctx
   *   the parser context
   * @return
   *   a constraint definition
   */
  private def buildColumnConstraint(ctx: TSqlParser.ColumnConstraintContext): ir.Constraint = {
    val options = Seq.newBuilder[GenericOption]

    ctx match {
      case pu if pu.PRIMARY() != null || pu.UNIQUE() != null =>
        // Primary or unique key construction.
        if (pu.CLUSTERED() != null) {
          options += OptionUnresolved("CLUSTERED")
        }
        if (pu.NONCLUSTERED() != null) {
          options += OptionUnresolved("NONCLUSTERED")
        }

        if (pu.columnNameList() != null) {
          options += OptionUnresolved(s"Cannot use multiple columns in a PRIMARY KEY column constraint: ${ParsingUtils
              .getTextFromParserRuleContext(pu.columnNameList())}")
        }

        if (pu.primaryKeyOptions() != null) {
          options ++= buildPKOptions(pu.primaryKeyOptions())
        }

        val c = if (pu.PRIMARY() != null) {
          ir.PrimaryKey(options.result())
        } else {
          ir.Unique(options.result())
        }
        if (ctx.id() != null) {
          ir.NamedConstraint(ctx.id().getText, c)
        } else {
          c
        }

      case fk if fk.FOREIGN() != null =>
        // Foreign key construction
        val refObject = fk.id().getText
        val refCols = fk.columnNameList().id().asScala.map(_.getText).mkString(",")
        if (fk.foreignKeyOptions().onDelete() != null) {
          options += buildFkOnDelete(fk.foreignKeyOptions().onDelete())
        }
        if (fk.foreignKeyOptions().onUpdate() != null) {
          options += buildFkOnUpdate(fk.foreignKeyOptions().onUpdate())
        }
        if (ctx.id() != null) {
          ir.NamedConstraint(ctx.id().getText, ir.ForeignKey(refObject, refCols, options.result()))
        } else {
          ir.ForeignKey(refObject, refCols, options.result())
        }

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction
        val expr = cc.checkConstraint().expression().accept(expressionBuilder)
        if (ctx.id() != null) {
          ir.NamedConstraint(ctx.id().getText, ir.CheckConstraint(expr))
        } else {
          ir.CheckConstraint(expr)
        }

      case _ => ir.UnresolvedConstraint(ctx.getText)
    }
  }

  private def buildFkOnDelete(ctx: TSqlParser.OnDeleteContext): GenericOption = {
    ctx match {
      case c if c.CASCADE() != null => OptionUnresolved("ON DELETE CASCADE")
      case c if (c.NULL() != null) => OptionUnresolved("ON DELETE SET NULL")
      case c if (c.DEFAULT() != null) => OptionUnresolved("ON DELETE SET DEFAULT")
      case c if c.NO() != null => OptionString("ON DELETE", "NO ACTION")
    }
  }

  private def buildFkOnUpdate(ctx: TSqlParser.OnUpdateContext): GenericOption = {
    ctx match {
      case c if c.CASCADE() != null => OptionUnresolved("ON UPDATE CASCADE")
      case c if (c.NULL() != null) => OptionUnresolved("ON UPDATE SET NULL")
      case c if (c.DEFAULT() != null) => OptionUnresolved("ON UPDATE SET DEFAULT")
      case c if c.NO() != null => OptionString("ON UPDATE", "NO ACTION")
    }
  }

  private def buildPKOptions(ctx: TSqlParser.PrimaryKeyOptionsContext): Seq[GenericOption] = {
    val options = Seq.newBuilder[GenericOption]
    if (ctx.FILLFACTOR() != null) {
      options += OptionUnresolved(s"WITH FILLFACTOR = ${ctx.getText()}")
    }
    // TODO: index options
    // TODO: partition options
    options.result()
  }

  private def buildComputedColumn(context: TSqlParser.ComputedColumnDefinitionContext): ir.ColumnDeclaration = {
    null
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
