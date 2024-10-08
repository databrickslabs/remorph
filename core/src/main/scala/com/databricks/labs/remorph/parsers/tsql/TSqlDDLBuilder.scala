package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.Catalog
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.{intermediate => ir}
import org.antlr.v4.runtime.ParserRuleContext

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlDDLBuilder(vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog] {

  override def visitCreateTable(ctx: TSqlParser.CreateTableContext): ir.Catalog =
    ctx match {
      case ci if ci.createInternal() != null => ci.createInternal().accept(this)
      case ct if ct.createExternal() != null => ct.createExternal().accept(this)
      case _ => ir.UnresolvedCatalog(getTextFromParserRuleContext(ctx))
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
        ir.CreateTableAsSelect(tableName, ctas.selectStatementStandalone().accept(vc.relationBuilder), None, None, None)
      case _ => ir.UnresolvedCatalog(getTextFromParserRuleContext(ctx))
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
    ir.UnresolvedCatalog(getTextFromParserRuleContext(ctx))
  }

  /**
   * There seems to be no options given to TSQL: CREATE TABLE that make any sense in Databricks SQL, so we will just
   * create them all as OptionUnresolved and store them as comments. If there turns out to be any compatibility, we can
   * override the generation here.
   * @param ctx the parse tree
   * @return the option we have parsed
   */
  private def buildOption(ctx: TSqlParser.TableOptionContext): ir.GenericOption = {
    ir.OptionUnresolved(getTextFromParserRuleContext(ctx))
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
          constraints += ir.DefaultValueConstraint(d.defaultValue().expression().accept(vc.expressionBuilder))
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
            val con = buildColumnConstraint(ctx.id().getText, c.columnConstraint())

            // TSQL allows FOREIGN KEY and CHECK constraints to be declared as column constraints,
            // but Databricks SQL does not so we need to gather them as table constraints

            if (c.columnConstraint().FOREIGN() != null || c.columnConstraint().checkConstraint() != null) {
              tableConstraints += con
            } else {
              constraints += con
            }
          }

        case d if d.identityColumn() != null =>
          // IDENTITY is supported in Databricks SQL but is done via GENERATED constraint
          constraints += ir.IdentityConstraint(d.identityColumn().INT(0).getText, d.identityColumn().INT(1).getText)

        // Unsupported stuff
        case m if m.MASKED() != null =>
          // MASKED WITH FUNCTION = 'functionName' is not supported in Databricks SQL
          options += ir.OptionUnresolved(s"Unsupported Option: ${getTextFromParserRuleContext(m)}")

        case f if f.ENCRYPTED() != null =>
          // ENCRYPTED WITH ... is not supported in Databricks SQL
          options += ir.OptionUnresolved(s"Unsupported Option: ${getTextFromParserRuleContext(f)}")

        case o if o.genericOption() != null =>
          options += ir.OptionUnresolved(s"Unsupported Option: ${getTextFromParserRuleContext(o)}")
      }
    }
    val dataType = vc.dataTypeBuilder.build(ctx.dataType())
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
            options += ir.OptionUnresolved(getTextFromParserRuleContext(pu.clustered()))
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
        ir.UnresolvedConstraint(getTextFromParserRuleContext(ctx))

      case defVal if defVal.DEFAULT() != null =>
        // DEFAULT is not supported in Databricks SQL at TABLE constraint level
        ir.UnresolvedConstraint(getTextFromParserRuleContext(ctx))

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction
        val expr = cc.checkConstraint().searchCondition().accept(vc.expressionBuilder)
        if (cc.checkConstraint().NOT() != null) {
          options += ir.OptionUnresolved("NOT FOR REPLICATION")
        }
        ir.CheckConstraint(expr)

      case _ => ir.UnresolvedConstraint(getTextFromParserRuleContext(ctx))
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
   * TSQL allows FOREIGN KEY and CHECK constraints to be declared as column constraints, but Databricks SQL does not
   * So the caller needs to check for those circumstances and handle them accordingly.
   *
   * @param ctx
   *   the parser context
   * @return
   *   a constraint definition
   */
  private def buildColumnConstraint(colName: String, ctx: TSqlParser.ColumnConstraintContext): ir.Constraint = {
    val options = Seq.newBuilder[ir.GenericOption]
    val constraint = ctx match {
      case pu if pu.PRIMARY() != null || pu.UNIQUE() != null =>
        // Primary or unique key construction.
        if (pu.clustered() != null) {
          options += ir.OptionUnresolved(getTextFromParserRuleContext(pu.clustered()))
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
        // Foreign key construction - note that this is a table level constraint in Databricks SQL
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
        ir.ForeignKey(colName, refObject, refCols, options.result())

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction (will be gathered as a table level constraint)
        val expr = cc.checkConstraint().searchCondition().accept(vc.expressionBuilder)
        if (cc.checkConstraint().NOT() != null) {
          options += ir.OptionUnresolved("NOT FOR REPLICATION")
        }
        ir.CheckConstraint(expr)

      case _ => ir.UnresolvedConstraint(getTextFromParserRuleContext(ctx))
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
    ir.UnresolvedConstraint(getTextFromParserRuleContext(ctx))
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
    val options = opts.asScala.flatMap(_.genericOption().asScala).toList.map(vc.optionBuilder.buildOption)
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

  override def visitDdlClause(ctx: TSqlParser.DdlClauseContext): Catalog = {

    val methods: Seq[() => ParserRuleContext] = Seq(
      ctx.alterApplicationRole _,
      ctx.alterAssembly _,
      ctx.alterAsymmetricKey _,
      ctx.alterAuthorization _,
      ctx.alterAvailabilityGroup _,
      ctx.alterCertificate _,
      ctx.alterColumnEncryptionKey _,
      ctx.alterCredential _,
      ctx.alterCryptographicProvider _,
      ctx.alterDatabase _,
      ctx.alterDatabaseAuditSpecification _,
      ctx.alterDbRole _,
      ctx.alterEndpoint _,
      ctx.alterExternalDataSource _,
      ctx.alterExternalLibrary _,
      ctx.alterExternalResourcePool _,
      ctx.alterFulltextCatalog _,
      ctx.alterFulltextStoplist _,
      ctx.alterIndex _,
      ctx.alterLoginAzureSql _,
      ctx.alterLoginAzureSqlDwAndPdw _,
      ctx.alterLoginSqlServer _,
      ctx.alterMasterKeyAzureSql _,
      ctx.alterMasterKeySqlServer _,
      ctx.alterMessageType _,
      ctx.alterPartitionFunction _,
      ctx.alterPartitionScheme _,
      ctx.alterRemoteServiceBinding _,
      ctx.alterResourceGovernor _,
      ctx.alterSchemaAzureSqlDwAndPdw _,
      ctx.alterSchemaSql _,
      ctx.alterSequence _,
      ctx.alterServerAudit _,
      ctx.alterServerAuditSpecification _,
      ctx.alterServerConfiguration _,
      ctx.alterServerRole _,
      ctx.alterServerRolePdw _,
      ctx.alterService _,
      ctx.alterServiceMasterKey _,
      ctx.alterSymmetricKey _,
      ctx.alterTable _,
      ctx.alterUser _,
      ctx.alterUserAzureSql _,
      ctx.alterWorkloadGroup _,
      ctx.alterXmlSchemaCollection _,
      ctx.createApplicationRole _,
      ctx.createAssembly _,
      ctx.createAsymmetricKey _,
      ctx.createColumnEncryptionKey _,
      ctx.createColumnMasterKey _,
      ctx.createColumnstoreIndex _,
      ctx.createCredential _,
      ctx.createCryptographicProvider _,
      ctx.createDatabaseScopedCredential _,
      ctx.createDatabase _,
      ctx.createDatabaseAuditSpecification _,
      ctx.createDbRole _,
      ctx.createEndpoint _,
      ctx.createEventNotification _,
      ctx.createExternalLibrary _,
      ctx.createExternalResourcePool _,
      ctx.createExternalDataSource _,
      ctx.createFulltextCatalog _,
      ctx.createFulltextStoplist _,
      ctx.createIndex _,
      ctx.createLoginAzureSql _,
      ctx.createLoginPdw _,
      ctx.createLoginSqlServer _,
      ctx.createMasterKeyAzureSql _,
      ctx.createMasterKeySqlServer _,
      ctx.createNonclusteredColumnstoreIndex _,
      ctx.createOrAlterBrokerPriority _,
      ctx.createOrAlterEventSession _,
      ctx.createPartitionFunction _,
      ctx.createPartitionScheme _,
      ctx.createRemoteServiceBinding _,
      ctx.createResourcePool _,
      ctx.createRoute _,
      ctx.createRule _,
      ctx.createSchema _,
      ctx.createSchemaAzureSqlDwAndPdw _,
      ctx.createSearchPropertyList _,
      ctx.createSecurityPolicy _,
      ctx.createSequence _,
      ctx.createServerAudit _,
      ctx.createServerAuditSpecification _,
      ctx.createServerRole _,
      ctx.createService _,
      ctx.createStatistics _,
      ctx.createSynonym _,
      ctx.createTable _,
      ctx.createType _,
      ctx.createUser _,
      ctx.createUserAzureSqlDw _,
      ctx.createWorkloadGroup _,
      ctx.createXmlIndex _,
      ctx.createXmlSchemaCollection _,
      ctx.triggerDisEn _,
      ctx.dropAggregate _,
      ctx.dropApplicationRole _,
      ctx.dropAssembly _,
      ctx.dropAsymmetricKey _,
      ctx.dropAvailabilityGroup _,
      ctx.dropBrokerPriority _,
      ctx.dropCertificate _,
      ctx.dropColumnEncryptionKey _,
      ctx.dropColumnMasterKey _,
      ctx.dropContract _,
      ctx.dropCredential _,
      ctx.dropCryptograhicProvider _,
      ctx.dropDatabase _,
      ctx.dropDatabaseAuditSpecification _,
      ctx.dropDatabaseEncryptionKey _,
      ctx.dropDatabaseScopedCredential _,
      ctx.dropDbRole _,
      ctx.dropDefault _,
      ctx.dropEndpoint _,
      ctx.dropEventNotifications _,
      ctx.dropEventSession _,
      ctx.dropExternalDataSource _,
      ctx.dropExternalFileFormat _,
      ctx.dropExternalLibrary _,
      ctx.dropExternalResourcePool _,
      ctx.dropExternalTable _,
      ctx.dropFulltextCatalog _,
      ctx.dropFulltextIndex _,
      ctx.dropFulltextStoplist _,
      ctx.dropFunction _,
      ctx.dropIndex _,
      ctx.dropLogin _,
      ctx.dropMasterKey _,
      ctx.dropMessageType _,
      ctx.dropPartitionFunction _,
      ctx.dropPartitionScheme _,
      ctx.dropProcedure _,
      ctx.dropQueue _,
      ctx.dropRemoteServiceBinding _,
      ctx.dropResourcePool _,
      ctx.dropRoute _,
      ctx.dropRule _,
      ctx.dropSchema _,
      ctx.dropSearchPropertyList _,
      ctx.dropSecurityPolicy _,
      ctx.dropSequence _,
      ctx.dropServerAudit _,
      ctx.dropServerAuditSpecification _,
      ctx.dropServerRole _,
      ctx.dropService _,
      ctx.dropSignature _,
      ctx.dropStatistics _,
      ctx.dropStatisticsNameAzureDwAndPdw _,
      ctx.dropSymmetricKey _,
      ctx.dropSynonym _,
      ctx.dropTable _,
      ctx.dropTrigger _,
      ctx.dropType _,
      ctx.dropUser _,
      ctx.dropView _,
      ctx.dropWorkloadGroup _,
      ctx.dropXmlSchemaCollection _,
      ctx.triggerDisEn _,
      ctx.lockTable _,
      ctx.truncateTable _,
      ctx.updateStatistics _)

    methods
      .collectFirst {
        case method if method() != null => method().accept(this)
      }
      .getOrElse(throw new IllegalArgumentException("No matching ddl clause found"))
  }
}
