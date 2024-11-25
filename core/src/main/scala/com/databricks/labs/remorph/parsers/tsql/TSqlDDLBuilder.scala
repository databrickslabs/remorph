package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.intermediate.Catalog
import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.{intermediate => ir}

import scala.collection.JavaConverters.asScalaBufferConverter

class TSqlDDLBuilder(override val vc: TSqlVisitorCoordinator)
    extends TSqlParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Catalog =
    ir.UnresolvedCatalog(ruleText = ruleText, message = message)

  // Concrete visitors

  override def visitCreateTable(ctx: TSqlParser.CreateTableContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case ci if ci.createInternal() != null => ci.createInternal().accept(this)
        case ct if ct.createExternal() != null => ct.createExternal().accept(this)
        case _ =>
          ir.UnresolvedCatalog(
            ruleText = contextText(ctx),
            message = "Unknown CREATE TABLE variant",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
      }
  }

  override def visitCreateInternal(ctx: TSqlParser.CreateInternalContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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
          ir.CreateTableAsSelect(
            tableName,
            ctas.selectStatementStandalone().accept(vc.relationBuilder),
            None,
            None,
            None)
        case _ =>
          ir.UnresolvedCatalog(
            ruleText = contextText(ctx),
            message = "Unknown variant of CREATE TABLE is not yet supported",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
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

  override def visitCreateExternal(ctx: TSqlParser.CreateExternalContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ir.UnresolvedCatalog(
        ruleText = contextText(ctx),
        message = "CREATE EXTERNAL TABLE is not yet supported",
        ruleName = vc.ruleName(ctx),
        tokenName = Some(tokenName(ctx.getStart)))
  }

  /**
   * There seems to be no options given to TSQL: CREATE TABLE that make any sense in Databricks SQL, so we will just
   * create them all as OptionUnresolved and store them as comments. If there turns out to be any compatibility, we can
   * override the generation here.
   * @param ctx the parse tree
   * @return the option we have parsed
   */
  private def buildOption(ctx: TSqlParser.TableOptionContext): ir.GenericOption = {
    ir.OptionUnresolved(contextText(ctx))
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
          constraints += ir
            .IdentityConstraint(Some(d.identityColumn().INT(0).getText), Some(d.identityColumn().INT(1).getText))

        // Unsupported stuff
        case m if m.MASKED() != null =>
          // MASKED WITH FUNCTION = 'functionName' is not supported in Databricks SQL
          options += ir.OptionUnresolved(s"Unsupported Option: ${contextText(m)}")

        case f if f.ENCRYPTED() != null =>
          // ENCRYPTED WITH ... is not supported in Databricks SQL
          options += ir.OptionUnresolved(s"Unsupported Option: ${contextText(f)}")

        case o if o.genericOption() != null =>
          options += ir.OptionUnresolved(s"Unsupported Option: ${contextText(o)}")
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
            options += ir.OptionUnresolved(contextText(pu.clustered()))
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
        ir.UnresolvedConstraint(contextText(ctx))

      case defVal if defVal.DEFAULT() != null =>
        // DEFAULT is not supported in Databricks SQL at TABLE constraint level
        ir.UnresolvedConstraint(contextText(ctx))

      case cc if cc.checkConstraint() != null =>
        // Check constraint construction
        val expr = cc.checkConstraint().searchCondition().accept(vc.expressionBuilder)
        if (cc.checkConstraint().NOT() != null) {
          options += ir.OptionUnresolved("NOT FOR REPLICATION")
        }
        ir.CheckConstraint(expr)

      case _ => ir.UnresolvedConstraint(contextText(ctx))
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
          options += ir.OptionUnresolved(contextText(pu.clustered()))
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

      case _ => ir.UnresolvedConstraint(contextText(ctx))
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
    ir.UnresolvedConstraint(contextText(ctx))
  }

  /**
   * This is not actually implemented but was a quick way to exercise the genericOption builder before we had other
   * syntax implemented to test it with.
   *
   * @param ctx
   *   the parse tree
   */
  override def visitBackupStatement(ctx: TSqlParser.BackupStatementContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx.backupDatabase().accept(this)
  }

  override def visitBackupDatabase(ctx: TSqlParser.BackupDatabaseContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
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

  override def visitDdlClause(ctx: TSqlParser.DdlClauseContext): Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case c if c.alterApplicationRole() != null => c.alterApplicationRole().accept(this)
        case c if c.alterAssembly() != null => c.alterAssembly().accept(this)
        case c if c.alterAsymmetricKey() != null => c.alterAsymmetricKey().accept(this)
        case c if c.alterAuthorization() != null => c.alterAuthorization().accept(this)
        case c if c.alterAvailabilityGroup() != null => c.alterAvailabilityGroup().accept(this)
        case c if c.alterCertificate() != null => c.alterCertificate().accept(this)
        case c if c.alterColumnEncryptionKey() != null => c.alterColumnEncryptionKey().accept(this)
        case c if c.alterCredential() != null => c.alterCredential().accept(this)
        case c if c.alterCryptographicProvider() != null => c.alterCryptographicProvider().accept(this)
        case c if c.alterDatabase() != null => c.alterDatabase().accept(this)
        case c if c.alterDatabaseAuditSpecification() != null => c.alterDatabaseAuditSpecification().accept(this)
        case c if c.alterDbRole() != null => c.alterDbRole().accept(this)
        case c if c.alterEndpoint() != null => c.alterEndpoint().accept(this)
        case c if c.alterExternalDataSource() != null => c.alterExternalDataSource().accept(this)
        case c if c.alterExternalLibrary() != null => c.alterExternalLibrary().accept(this)
        case c if c.alterExternalResourcePool() != null => c.alterExternalResourcePool().accept(this)
        case c if c.alterFulltextCatalog() != null => c.alterFulltextCatalog().accept(this)
        case c if c.alterFulltextStoplist() != null => c.alterFulltextStoplist().accept(this)
        case c if c.alterIndex() != null => c.alterIndex().accept(this)
        case c if c.alterLoginAzureSql() != null => c.alterLoginAzureSql().accept(this)
        case c if c.alterLoginAzureSqlDwAndPdw() != null => c.alterLoginAzureSqlDwAndPdw().accept(this)
        case c if c.alterLoginSqlServer() != null => c.alterLoginSqlServer().accept(this)
        case c if c.alterMasterKeyAzureSql() != null => c.alterMasterKeyAzureSql().accept(this)
        case c if c.alterMasterKeySqlServer() != null => c.alterMasterKeySqlServer().accept(this)
        case c if c.alterMessageType() != null => c.alterMessageType().accept(this)
        case c if c.alterPartitionFunction() != null => c.alterPartitionFunction().accept(this)
        case c if c.alterPartitionScheme() != null => c.alterPartitionScheme().accept(this)
        case c if c.alterRemoteServiceBinding() != null => c.alterRemoteServiceBinding().accept(this)
        case c if c.alterResourceGovernor() != null => c.alterResourceGovernor().accept(this)
        case c if c.alterSchemaAzureSqlDwAndPdw() != null => c.alterSchemaAzureSqlDwAndPdw().accept(this)
        case c if c.alterSchemaSql() != null => c.alterSchemaSql().accept(this)
        case c if c.alterSequence() != null => c.alterSequence().accept(this)
        case c if c.alterServerAudit() != null => c.alterServerAudit().accept(this)
        case c if c.alterServerAuditSpecification() != null => c.alterServerAuditSpecification().accept(this)
        case c if c.alterServerConfiguration() != null => c.alterServerConfiguration().accept(this)
        case c if c.alterServerRole() != null => c.alterServerRole().accept(this)
        case c if c.alterServerRolePdw() != null => c.alterServerRolePdw().accept(this)
        case c if c.alterService() != null => c.alterService().accept(this)
        case c if c.alterServiceMasterKey() != null => c.alterServiceMasterKey().accept(this)
        case c if c.alterSymmetricKey() != null => c.alterSymmetricKey().accept(this)
        case c if c.alterTable() != null => c.alterTable().accept(this)
        case c if c.alterUser() != null => c.alterUser().accept(this)
        case c if c.alterUserAzureSql() != null => c.alterUserAzureSql().accept(this)
        case c if c.alterWorkloadGroup() != null => c.alterWorkloadGroup().accept(this)
        case c if c.alterXmlSchemaCollection() != null => c.alterXmlSchemaCollection().accept(this)
        case c if c.createApplicationRole() != null => c.createApplicationRole().accept(this)
        case c if c.createAssembly() != null => c.createAssembly().accept(this)
        case c if c.createAsymmetricKey() != null => c.createAsymmetricKey().accept(this)
        case c if c.createColumnEncryptionKey() != null => c.createColumnEncryptionKey().accept(this)
        case c if c.createColumnMasterKey() != null => c.createColumnMasterKey().accept(this)
        case c if c.createColumnstoreIndex() != null => c.createColumnstoreIndex().accept(this)
        case c if c.createCredential() != null => c.createCredential().accept(this)
        case c if c.createCryptographicProvider() != null => c.createCryptographicProvider().accept(this)
        case c if c.createDatabaseScopedCredential() != null => c.createDatabaseScopedCredential().accept(this)
        case c if c.createDatabase() != null => c.createDatabase().accept(this)
        case c if c.createDatabaseAuditSpecification() != null => c.createDatabaseAuditSpecification().accept(this)
        case c if c.createDbRole() != null => c.createDbRole().accept(this)
        case c if c.createEndpoint() != null => c.createEndpoint().accept(this)
        case c if c.createEventNotification() != null => c.createEventNotification().accept(this)
        case c if c.createExternalLibrary() != null => c.createExternalLibrary().accept(this)
        case c if c.createExternalResourcePool() != null => c.createExternalResourcePool().accept(this)
        case c if c.createExternalDataSource() != null => c.createExternalDataSource().accept(this)
        case c if c.createFulltextCatalog() != null => c.createFulltextCatalog().accept(this)
        case c if c.createFulltextStoplist() != null => c.createFulltextStoplist().accept(this)
        case c if c.createIndex() != null => c.createIndex().accept(this)
        case c if c.createLoginAzureSql() != null => c.createLoginAzureSql().accept(this)
        case c if c.createLoginPdw() != null => c.createLoginPdw().accept(this)
        case c if c.createLoginSqlServer() != null => c.createLoginSqlServer().accept(this)
        case c if c.createMasterKeyAzureSql() != null => c.createMasterKeyAzureSql().accept(this)
        case c if c.createMasterKeySqlServer() != null => c.createMasterKeySqlServer().accept(this)
        case c if c.createNonclusteredColumnstoreIndex() != null => c.createNonclusteredColumnstoreIndex().accept(this)
        case c if c.createOrAlterBrokerPriority() != null => c.createOrAlterBrokerPriority().accept(this)
        case c if c.createOrAlterEventSession() != null => c.createOrAlterEventSession().accept(this)
        case c if c.createPartitionFunction() != null => c.createPartitionFunction().accept(this)
        case c if c.createPartitionScheme() != null => c.createPartitionScheme().accept(this)
        case c if c.createRemoteServiceBinding() != null => c.createRemoteServiceBinding().accept(this)
        case c if c.createResourcePool() != null => c.createResourcePool().accept(this)
        case c if c.createRoute() != null => c.createRoute().accept(this)
        case c if c.createRule() != null => c.createRule().accept(this)
        case c if c.createSchema() != null => c.createSchema().accept(this)
        case c if c.createSchemaAzureSqlDwAndPdw() != null => c.createSchemaAzureSqlDwAndPdw().accept(this)
        case c if c.createSearchPropertyList() != null => c.createSearchPropertyList().accept(this)
        case c if c.createSecurityPolicy() != null => c.createSecurityPolicy().accept(this)
        case c if c.createSequence() != null => c.createSequence().accept(this)
        case c if c.createServerAudit() != null => c.createServerAudit().accept(this)
        case c if c.createServerAuditSpecification() != null => c.createServerAuditSpecification().accept(this)
        case c if c.createServerRole() != null => c.createServerRole().accept(this)
        case c if c.createService() != null => c.createService().accept(this)
        case c if c.createStatistics() != null => c.createStatistics().accept(this)
        case c if c.createSynonym() != null => c.createSynonym().accept(this)
        case c if c.createTable() != null => c.createTable().accept(this)
        case c if c.createType() != null => c.createType().accept(this)
        case c if c.createUser() != null => c.createUser().accept(this)
        case c if c.createUserAzureSqlDw() != null => c.createUserAzureSqlDw().accept(this)
        case c if c.createWorkloadGroup() != null => c.createWorkloadGroup().accept(this)
        case c if c.createXmlIndex() != null => c.createXmlIndex().accept(this)
        case c if c.createXmlSchemaCollection() != null => c.createXmlSchemaCollection().accept(this)
        case c if c.triggerDisEn() != null => c.triggerDisEn().accept(this)
        case c if c.dropAggregate() != null => c.dropAggregate().accept(this)
        case c if c.dropApplicationRole() != null => c.dropApplicationRole().accept(this)
        case c if c.dropAssembly() != null => c.dropAssembly().accept(this)
        case c if c.dropAsymmetricKey() != null => c.dropAsymmetricKey().accept(this)
        case c if c.dropAvailabilityGroup() != null => c.dropAvailabilityGroup().accept(this)
        case c if c.dropBrokerPriority() != null => c.dropBrokerPriority().accept(this)
        case c if c.dropCertificate() != null => c.dropCertificate().accept(this)
        case c if c.dropColumnEncryptionKey() != null => c.dropColumnEncryptionKey().accept(this)
        case c if c.dropColumnMasterKey() != null => c.dropColumnMasterKey().accept(this)
        case c if c.dropContract() != null => c.dropContract().accept(this)
        case c if c.dropCredential() != null => c.dropCredential().accept(this)
        case c if c.dropCryptograhicProvider() != null => c.dropCryptograhicProvider().accept(this)
        case c if c.dropDatabase() != null => c.dropDatabase().accept(this)
        case c if c.dropDatabaseAuditSpecification() != null => c.dropDatabaseAuditSpecification().accept(this)
        case c if c.dropDatabaseEncryptionKey() != null => c.dropDatabaseEncryptionKey().accept(this)
        case c if c.dropDatabaseScopedCredential() != null => c.dropDatabaseScopedCredential().accept(this)
        case c if c.dropDbRole() != null => c.dropDbRole().accept(this)
        case c if c.dropDefault() != null => c.dropDefault().accept(this)
        case c if c.dropEndpoint() != null => c.dropEndpoint().accept(this)
        case c if c.dropEventNotifications() != null => c.dropEventNotifications().accept(this)
        case c if c.dropEventSession() != null => c.dropEventSession().accept(this)
        case c if c.dropExternalDataSource() != null => c.dropExternalDataSource().accept(this)
        case c if c.dropExternalFileFormat() != null => c.dropExternalFileFormat().accept(this)
        case c if c.dropExternalLibrary() != null => c.dropExternalLibrary().accept(this)
        case c if c.dropExternalResourcePool() != null => c.dropExternalResourcePool().accept(this)
        case c if c.dropExternalTable() != null => c.dropExternalTable().accept(this)
        case c if c.dropFulltextCatalog() != null => c.dropFulltextCatalog().accept(this)
        case c if c.dropFulltextIndex() != null => c.dropFulltextIndex().accept(this)
        case c if c.dropFulltextStoplist() != null => c.dropFulltextStoplist().accept(this)
        case c if c.dropFunction() != null => c.dropFunction().accept(this)
        case c if c.dropIndex() != null => c.dropIndex().accept(this)
        case c if c.dropLogin() != null => c.dropLogin().accept(this)
        case c if c.dropMasterKey() != null => c.dropMasterKey().accept(this)
        case c if c.dropMessageType() != null => c.dropMessageType().accept(this)
        case c if c.dropPartitionFunction() != null => c.dropPartitionFunction().accept(this)
        case c if c.dropPartitionScheme() != null => c.dropPartitionScheme().accept(this)
        case c if c.dropProcedure() != null => c.dropProcedure().accept(this)
        case c if c.dropQueue() != null => c.dropQueue().accept(this)
        case c if c.dropRemoteServiceBinding() != null => c.dropRemoteServiceBinding().accept(this)
        case c if c.dropResourcePool() != null => c.dropResourcePool().accept(this)
        case c if c.dropRoute() != null => c.dropRoute().accept(this)
        case c if c.dropRule() != null => c.dropRule().accept(this)
        case c if c.dropSchema() != null => c.dropSchema().accept(this)
        case c if c.dropSearchPropertyList() != null => c.dropSearchPropertyList().accept(this)
        case c if c.dropSecurityPolicy() != null => c.dropSecurityPolicy().accept(this)
        case c if c.dropSequence() != null => c.dropSequence().accept(this)
        case c if c.dropServerAudit() != null => c.dropServerAudit().accept(this)
        case c if c.dropServerAuditSpecification() != null => c.dropServerAuditSpecification().accept(this)
        case c if c.dropServerRole() != null => c.dropServerRole().accept(this)
        case c if c.dropService() != null => c.dropService().accept(this)
        case c if c.dropSignature() != null => c.dropSignature().accept(this)
        case c if c.dropStatistics() != null => c.dropStatistics().accept(this)
        case c if c.dropStatisticsNameAzureDwAndPdw() != null => c.dropStatisticsNameAzureDwAndPdw().accept(this)
        case c if c.dropSymmetricKey() != null => c.dropSymmetricKey().accept(this)
        case c if c.dropSynonym() != null => c.dropSynonym().accept(this)
        case c if c.dropTable() != null => c.dropTable().accept(this)
        case c if c.dropTrigger() != null => c.dropTrigger().accept(this)
        case c if c.dropType() != null => c.dropType().accept(this)
        case c if c.dropUser() != null => c.dropUser().accept(this)
        case c if c.dropView() != null => c.dropView().accept(this)
        case c if c.dropWorkloadGroup() != null => c.dropWorkloadGroup().accept(this)
        case c if c.dropXmlSchemaCollection() != null => c.dropXmlSchemaCollection().accept(this)
        case c if c.triggerDisEn() != null => c.triggerDisEn().accept(this)
        case c if c.lockTable() != null => c.lockTable().accept(this)
        case c if c.truncateTable() != null => c.truncateTable().accept(this)
        case c if c.updateStatistics() != null => c.updateStatistics().accept(this)
        case _ =>
          ir.UnresolvedCatalog(
            ruleText = contextText(ctx),
            message = "Unknown DDL clause",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
      }
  }
}
