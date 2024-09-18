package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.{ParserCommon, intermediate => ir}
import com.databricks.labs.remorph.utils.ParsingUtils

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlDDLBuilder(
    optionBuilder: OptionBuilder,
    expressionBuilder: TSqlExpressionBuilder,
    relationBuilder: TSqlRelationBuilder)
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

    val (columns, virtualColumns, constraints, indices) = Option(ctx.columnDefTableConstraints()).toSeq
      .flatMap(_.columnDefTableConstraint().asScala)
      .foldLeft((Seq.empty[TSqlColDef], Seq.empty[TSqlColDef], Seq.empty[ir.Constraint], Seq.empty[ir.Constraint])) {
        case ((cols, virtualCols, cons, inds), constraint) =>
          val newCols = constraint.columnDefinition() match {
            case null => cols
            case columnDef =>
              cols :+ buildColumnDeclaration(columnDef)
          }

          val newVirtualCols = constraint.computedColumnDefinition() match {
            case null => virtualCols
            case computedCol =>
              virtualCols :+ buildComputedColumn(computedCol)
          }

          val newCons = constraint.tableConstraint() match {
            case null => cons
            case tableCons => cons :+ buildTableConstraint(tableCons)
          }

          val newInds = constraint.tableIndices() match {
            case null => inds
            case tableInds => inds :+ buildIndex(tableInds)
          }

          (newCols, newVirtualCols, newCons, newInds)
      }

    // At this point we have all the columns, constraints and indices, so we can build the schema
    val schema = ir.StructType((columns ++ virtualColumns).map(_.structField))

    // Now we can build the create table statement or the create table as select statement

    val createTable = ctx.createTableAs() match {
      case null => ir.CreateTable(tableName, None, None, None, schema)
      case ctas if ctas.selectStatementStandalone() != null =>
        ir.CreateTableAsSelect(tableName, ctas.selectStatementStandalone().accept(relationBuilder), None, None, None)
      case _ => ir.UnresolvedCatalog(ctx.getText)
    }

    // But because TSQL is so much more complicated than Databricks SQL, we need to build the table alterations
    // in a wrapper above the raw create statement.

    // First we want to iterate all the columns and build a map of all the column constraints where the key is the
    // element structField.name and the value is the TSqlColDef.constraints
    val columnConstraints = (columns ++ virtualColumns).map { colDef =>
      colDef.structField.name -> colDef.constraints
    }.toMap

    // Next we create another map all options for each column where the key is the element structField.name and the
    // value is the TSqlColDef.options
    val columnOptions = (columns ++ virtualColumns).map { colDef =>
      colDef.structField.name -> colDef.options
    }.toMap

    // And we want to collect any table level constraints that were generated in the TSqlColDef.tableConstraints
    // by iterating columns and virtualColumns and gathering any TSqlColDef tableConstraints and
    // creating a single Seq that also includes the constraints
    // that were already accumulated above
    val tableConstraints = constraints ++ (columns ++ virtualColumns).flatMap(_.tableConstraints)

    // We may have table level options as well as for each constraint and column
    val options: Option[Seq[ir.GenericOption]] = Option(ctx.tableOptions).map { tableOptions =>
      tableOptions.asScala.flatMap { el =>
        el.tableOption().asScala.map(buildOption)
      }
    }

    val partitionOn = Option(ctx.onPartitionOrFilegroup()).map(_.getText)

    // Now we can build the table additions that wrap the primitive create table statement
    createTable match {
      case ct: ir.UnresolvedCatalog =>
        ct
      case _ =>
        ir.CreateTableParams(
          createTable,
          columnConstraints,
          columnOptions,
          tableConstraints,
          indices,
          partitionOn,
          options)
    }
  }

  override def visitCreateExternal(ctx: TSqlParser.CreateExternalContext): ir.Catalog = {
    ir.UnresolvedCatalog(ctx.getText)
  }

  /**
   * There seems to be no options given to TSQL: CREATE TABLE that make any sense in Databricks SQL, so we will just
   * create them all as OptionUnresolved and store them as comments. If there turns out to be any compatibility, we can
   * override the generation here.
   * @param ctx the parse tree
   * @return the option we have parsed
   */
  private def buildOption(ctx: TSqlParser.TableOptionContext): ir.GenericOption = {
    ir.OptionUnresolved(ctx.getText)
  }

  private case class TSqlColDef(
      structField: ir.StructField,
      computedValue: Option[ir.Expression],
      constraints: Seq[ir.Constraint],
      tableConstraints: Seq[ir.Constraint],
      options: Seq[ir.GenericOption])

  private def buildColumnDeclaration(ctx: TSqlParser.ColumnDefinitionContext): TSqlColDef = {

    val options = Seq.newBuilder[ir.GenericOption]
    val constraints = Seq.newBuilder[ir.Constraint]
    val tableConstraints = Seq.newBuilder[ir.Constraint]
    var nullable: Option[Boolean] = None

    if (ctx.columnDefinitionElement() != null) {
      ctx.columnDefinitionElement().asScala.foreach {
        case rg if rg.ROWGUIDCOL() != null =>
          // ROWGUID is supported in Databricks SQL
          options += ir.OptionOn("ROWGUIDCOL")

        case d if d.defaultValue() != null =>
          // Databricks SQL does not support the naming of the DEFAULT CONSTRAINT, so we will just use the default
          // expression we are given, but if there is a name, we will store it as a comment
          constraints += ir.DefaultValueConstraint(d.defaultValue().expression().accept(expressionBuilder))
          if (d.defaultValue().id() != null) {
            options += ir.OptionUnresolved(
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
                  ir.CheckConstraint(ir.IsNotNull(ir.Column(None, ir.Id(ctx.id().getText)))))
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
          options += ir.OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(m)}")

        case f if f.ENCRYPTED() != null =>
          // ENCRYPTED WITH ... is not supported in Databricks SQL
          options += ir.OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(f)}")

        case o if o.genericOption() != null =>
          options += ir.OptionUnresolved(s"Unsupported Option: ${ParsingUtils.getTextFromParserRuleContext(o)}")
      }
    }
    val dataType = dataTypeBuilder.build(ctx.dataType())
    val sf = ir.StructField(ctx.id().getText, dataType, nullable.getOrElse(true))

    // TODO: index options

    TSqlColDef(sf, None, constraints.result(), tableConstraints.result(), options.result())
  }

  /**
   * builds a table constraint such as PRIMARY KEY, UNIQUE, FOREIGN KEY
   */
  private def buildTableConstraint(ctx: TSqlParser.TableConstraintContext): ir.Constraint = {

    val options = Seq.newBuilder[ir.GenericOption]

    val constraint = ctx match {

      case pu if pu.PRIMARY() != null || pu.UNIQUE() != null =>
        if (pu.clustered() != null) {
          if (pu.clustered().CLUSTERED() != null) {
            options += ir.OptionUnresolved(pu.clustered().getText)
          }
        }
        val colNames = ctx.columnNameListWithOrder().columnNameWithOrder().asScala.map { cnwo =>
          val colName = cnwo.id().getText
          if (cnwo.DESC() != null || cnwo.ASC() != null) {
            options += ir.OptionUnresolved(s"Cannot specify primary key order ASC/DESC on: $colName")
          }
          colName
        }
        options ++= buildPKOptions(pu.primaryKeyOptions())
        if (pu.PRIMARY() != null) {
          ir.PrimaryKey(options.result(), Some(colNames))
        } else {
          ir.Unique(options.result(), Some(colNames))
        }

      case fk if fk.FOREIGN() != null =>
        val refObject = fk.foreignKeyOptions().tableName().getText
        val tableCols = fk.columnNameList().id().asScala.map(_.getText).mkString(", ")
        val refCols = Option(fk.foreignKeyOptions())
          .map(_.columnNameList().id().asScala.map(_.getText).mkString(", "))
          .getOrElse("")
        if (fk.foreignKeyOptions().onDelete() != null) {
          options += buildFkOnDelete(fk.foreignKeyOptions().onDelete())
        }
        if (fk.foreignKeyOptions().onUpdate() != null) {
          options += buildFkOnUpdate(fk.foreignKeyOptions().onUpdate())
        }
        ir.ForeignKey(tableCols, refObject, refCols, options.result())

      case cc if cc.CONNECTION() != null =>
        // CONNECTION is not supported in Databricks SQL
        ir.UnresolvedConstraint(ctx.getText)

      case defVal if defVal.DEFAULT() != null =>
        // DEFAULT is not supported in Databricks SQL at TABLE constraint level
        ir.UnresolvedConstraint(ctx.getText)

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction
        val expr = cc.checkConstraint().searchCondition().accept(expressionBuilder)
        if (cc.checkConstraint().NOT() != null) {
          options += ir.OptionUnresolved("NOT FOR REPLICATION")
        }
        ir.CheckConstraint(expr)

      case _ => ir.UnresolvedConstraint(ctx.getText)
    }

    // Name the constraint if it is named and not unresolved
    ctx.CONSTRAINT() match {
      case null => constraint
      case _ =>
        constraint match {
          case _: ir.UnresolvedConstraint => constraint
          case _ => ir.NamedConstraint(ctx.cid.getText, constraint)
        }
    }

  }

  /**
   * Builds a column constraint such as PRIMARY KEY, UNIQUE, FOREIGN KEY, CHECK
   *
   * Note that TSQL is way more involved than Databricks SQL. We must record all the different options so that we can
   * at least generate a comment.
   *
   * @param ctx
   *   the parser context
   * @return
   *   a constraint definition
   */
  private def buildColumnConstraint(ctx: TSqlParser.ColumnConstraintContext): ir.Constraint = {
    val options = Seq.newBuilder[ir.GenericOption]
    val constraint = ctx match {
      case pu if pu.PRIMARY() != null || pu.UNIQUE() != null =>
        // Primary or unique key construction.
        if (pu.clustered() != null) {
          options += ir.OptionUnresolved(pu.clustered().getText)
        }

        if (pu.primaryKeyOptions() != null) {
          options ++= buildPKOptions(pu.primaryKeyOptions())
        }

        if (pu.PRIMARY() != null) {
          ir.PrimaryKey(options.result())
        } else {
          ir.Unique(options.result())
        }

      case fk if fk.FOREIGN() != null =>
        // Foreign key construction
        val refObject = fk.foreignKeyOptions().tableName().getText
        val refCols = Option(fk.foreignKeyOptions())
          .map(_.columnNameList().id().asScala.map(_.getText).mkString(","))
          .getOrElse("")
        if (fk.foreignKeyOptions().onDelete() != null) {
          options += buildFkOnDelete(fk.foreignKeyOptions().onDelete())
        }
        if (fk.foreignKeyOptions().onUpdate() != null) {
          options += buildFkOnUpdate(fk.foreignKeyOptions().onUpdate())
        }
        ir.ForeignKey(refObject, "", refCols, options.result())

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction
        val expr = cc.checkConstraint().searchCondition().accept(expressionBuilder)
        if (cc.checkConstraint().NOT() != null) {
          options += ir.OptionUnresolved("NOT FOR REPLICATION")
        }
        ir.CheckConstraint(expr)

      case _ => ir.UnresolvedConstraint(ctx.getText)
    }

    // Name the constraint if it is named and not unresolved
    ctx.CONSTRAINT() match {
      case null => constraint
      case _ =>
        constraint match {
          case _: ir.UnresolvedConstraint => constraint
          case _ => ir.NamedConstraint(ctx.id.getText, constraint)
        }
    }
  }

  private def buildFkOnDelete(ctx: TSqlParser.OnDeleteContext): ir.GenericOption = {
    ctx match {
      case c if c.CASCADE() != null => ir.OptionUnresolved("ON DELETE CASCADE")
      case c if c.NULL() != null => ir.OptionUnresolved("ON DELETE SET NULL")
      case c if c.DEFAULT() != null => ir.OptionUnresolved("ON DELETE SET DEFAULT")
      case c if c.NO() != null => ir.OptionString("ON DELETE", "NO ACTION")
    }
  }

  private def buildFkOnUpdate(ctx: TSqlParser.OnUpdateContext): ir.GenericOption = {
    ctx match {
      case c if c.CASCADE() != null => ir.OptionUnresolved("ON UPDATE CASCADE")
      case c if c.NULL() != null => ir.OptionUnresolved("ON UPDATE SET NULL")
      case c if c.DEFAULT() != null => ir.OptionUnresolved("ON UPDATE SET DEFAULT")
      case c if c.NO() != null => ir.OptionString("ON UPDATE", "NO ACTION")
    }
  }

  private def buildPKOptions(ctx: TSqlParser.PrimaryKeyOptionsContext): Seq[ir.GenericOption] = {
    val options = Seq.newBuilder[ir.GenericOption]
    if (ctx.FILLFACTOR() != null) {
      options += ir.OptionUnresolved(s"WITH FILLFACTOR = ${ctx.getText}")
    }
    // TODO: index options
    // TODO: partition options
    options.result()
  }

  private def buildComputedColumn(ctx: TSqlParser.ComputedColumnDefinitionContext): TSqlColDef = {
    null
  }

  /**
   * Abstracted out here but Spark/Databricks SQL does not support indexes, as it is not a database and cannot reliably
   * monitor data updates in external systems anyway. So it becomes an unresolved constraint here, but perhaps
   * we do something moore with it later.
   *
   * @param ctx the parse tree
   * @return An unresolved constraint representing the index syntax
   */
  private def buildIndex(ctx: TSqlParser.TableIndicesContext): ir.UnresolvedConstraint = {
    ir.UnresolvedConstraint(ctx.getText)
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
          case ir.OptionString("DISK", value) =>
            (value.stripPrefix("'").stripSuffix("'") :: disks, boolFlags, autoFlags, values)
          case ir.OptionOn(id) => (disks, boolFlags + (id -> true), autoFlags, values)
          case ir.OptionOff(id) => (disks, boolFlags + (id -> false), autoFlags, values)
          case ir.OptionAuto(id) => (disks, boolFlags, id :: autoFlags, values)
          case ir.OptionExpression(id, expr, _) => (disks, boolFlags, autoFlags, values + (id -> expr))
          case _ => (disks, boolFlags, autoFlags, values)
        }
    }
    // Default flags generally don't need to be specified as they are by definition, the default
    BackupDatabase(database, disks, boolFlags, autoFlags, values)
  }

}
