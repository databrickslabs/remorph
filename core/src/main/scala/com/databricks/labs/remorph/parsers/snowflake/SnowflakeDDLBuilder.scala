package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.ParserCommon
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.{StringContext => StrContext, _}
import com.databricks.labs.remorph.{intermediate => ir}

import java.util.Locale
import scala.collection.JavaConverters._
class SnowflakeDDLBuilder(override val vc: SnowflakeVisitorCoordinator)
    extends SnowflakeParserBaseVisitor[ir.Catalog]
    with ParserCommon[ir.Catalog] {

  // The default result is returned when there is no visitor implemented, and we produce an unresolved
  // object to represent the input that we have no visitor for.
  protected override def unresolved(ruleText: String, message: String): ir.Catalog =
    ir.UnresolvedCatalog(ruleText = ruleText, message = message)

  // Concrete visitors

  private def extractString(ctx: StrContext): String =
    ctx.accept(vc.expressionBuilder) match {
      case ir.StringLiteral(s) => s
      // TODO: Do not throw an error here - we need to generate an UnresolvedCatalog for it
      //       However, it is likely that we will neveer see this in the wild
      case e => throw new IllegalArgumentException(s"Expected a string literal, got $e")
    }

  override def visitDdlCommand(ctx: DdlCommandContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case a if a.alterCommand() != null => a.alterCommand().accept(this)
        case c if c.createCommand() != null => c.createCommand().accept(this)
        case d if d.dropCommand() != null => d.dropCommand().accept(this)
        case u if u.undropCommand() != null => u.undropCommand().accept(this)
      }
  }

  override def visitCreateCommand(ctx: CreateCommandContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case c if c.createAccount() != null => c.createAccount().accept(this)
        case c if c.createAlert() != null => c.createAlert().accept(this)
        case c if c.createApiIntegration() != null => c.createApiIntegration().accept(this)
        case c if c.createObjectClone() != null => c.createObjectClone().accept(this)
        case c if c.createConnection() != null => c.createConnection().accept(this)
        case c if c.createDatabase() != null => c.createDatabase().accept(this)
        case c if c.createDynamicTable() != null => c.createDynamicTable().accept(this)
        case c if c.createEventTable() != null => c.createEventTable().accept(this)
        case c if c.createExternalFunction() != null => c.createExternalFunction().accept(this)
        case c if c.createExternalTable() != null => c.createExternalTable().accept(this)
        case c if c.createFailoverGroup() != null => c.createFailoverGroup().accept(this)
        case c if c.createFileFormat() != null => c.createFileFormat().accept(this)
        case c if c.createFunction() != null => c.createFunction().accept(this)
        case c if c.createManagedAccount() != null => c.createManagedAccount().accept(this)
        case c if c.createMaskingPolicy() != null => c.createMaskingPolicy().accept(this)
        case c if c.createMaterializedView() != null => c.createMaterializedView().accept(this)
        case c if c.createNetworkPolicy() != null => c.createNetworkPolicy().accept(this)
        case c if c.createNotificationIntegration() != null => c.createNotificationIntegration().accept(this)
        case c if c.createPipe() != null => c.createPipe().accept(this)
        case c if c.createProcedure() != null => c.createProcedure().accept(this)
        case c if c.createReplicationGroup() != null => c.createReplicationGroup().accept(this)
        case c if c.createResourceMonitor() != null => c.createResourceMonitor().accept(this)
        case c if c.createRole() != null => c.createRole().accept(this)
        case c if c.createRowAccessPolicy() != null => c.createRowAccessPolicy().accept(this)
        case c if c.createSchema() != null => c.createSchema().accept(this)
        case c if c.createSecurityIntegrationExternalOauth() != null =>
          c.createSecurityIntegrationExternalOauth().accept(this)
        case c if c.createSecurityIntegrationSnowflakeOauth() != null =>
          c.createSecurityIntegrationSnowflakeOauth().accept(this)
        case c if c.createSecurityIntegrationSaml2() != null => c.createSecurityIntegrationSaml2().accept(this)
        case c if c.createSecurityIntegrationScim() != null => c.createSecurityIntegrationScim().accept(this)
        case c if c.createSequence() != null => c.createSequence().accept(this)
        case c if c.createSessionPolicy() != null => c.createSessionPolicy().accept(this)
        case c if c.createShare() != null => c.createShare().accept(this)
        case c if c.createStage() != null => c.createStage().accept(this)
        case c if c.createStorageIntegration() != null => c.createStorageIntegration().accept(this)
        case c if c.createStream() != null => c.createStream().accept(this)
        case c if c.createTable() != null => c.createTable().accept(this)
        case c if c.createTableAsSelect() != null => c.createTableAsSelect().accept(this)
        case c if c.createTableLike() != null => c.createTableLike().accept(this)
        case c if c.createTag() != null => c.createTag().accept(this)
        case c if c.createTask() != null => c.createTask().accept(this)
        case c if c.createUser() != null => c.createUser().accept(this)
        case c if c.createView() != null => c.createView().accept(this)
        case c if c.createWarehouse() != null => c.createWarehouse().accept(this)
        case _ =>
          ir.UnresolvedCatalog(ruleText = contextText(ctx), "Unknown CREATE XXX command", ruleName = "createCommand")
      }
  }

  override def visitCreateFunction(ctx: CreateFunctionContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val runtime = Option(ctx.id()).map(_.getText.toLowerCase(Locale.ROOT)).getOrElse("sql")
      val runtimeInfo =
        runtime match {
          case r if r == "java" => buildJavaUDF(ctx)
          case r if r == "python" => buildPythonUDF(ctx)
          case r if r == "javascript" => ir.JavaScriptRuntimeInfo
          case r if r == "scala" => buildScalaUDF(ctx)
          case _ => ir.SQLRuntimeInfo(ctx.MEMOIZABLE() != null)
        }
      val name = ctx.dotIdentifier().getText
      val returnType = vc.typeBuilder.buildDataType(ctx.dataType())
      val parameters = ctx.argDecl().asScala.map(buildParameter)
      val acceptsNullParameters = ctx.CALLED() != null
      val body = buildFunctionBody(ctx.functionDefinition())
      val comment = Option(ctx.com).map(extractString)
      ir.CreateInlineUDF(name, returnType, parameters, runtimeInfo, acceptsNullParameters, comment, body)
  }

  private def buildParameter(ctx: ArgDeclContext): ir.FunctionParameter =
    ir.FunctionParameter(
      name = ctx.id().getText,
      dataType = vc.typeBuilder.buildDataType(ctx.dataType()),
      defaultValue = Option(ctx.expr()).map(_.accept(vc.expressionBuilder)))

  private def buildFunctionBody(ctx: FunctionDefinitionContext): String = extractString(ctx.string()).trim

  private def buildJavaUDF(ctx: CreateFunctionContext): ir.RuntimeInfo = buildJVMUDF(ctx)(ir.JavaRuntimeInfo.apply)
  private def buildScalaUDF(ctx: CreateFunctionContext): ir.RuntimeInfo = buildJVMUDF(ctx)(ir.ScalaRuntimeInfo.apply)

  private def buildJVMUDF(ctx: CreateFunctionContext)(
      ctr: (Option[String], Seq[String], String) => ir.RuntimeInfo): ir.RuntimeInfo = {
    val imports =
      ctx
        .stringList()
        .asScala
        .find(occursBefore(ctx.IMPORTS(), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ctr(extractRuntimeVersion(ctx), imports, extractHandler(ctx))
  }
  private def extractRuntimeVersion(ctx: CreateFunctionContext): Option[String] = ctx.string().asScala.collectFirst {
    case c if occursBefore(ctx.RUNTIME_VERSION(), c) => extractString(c)
  }

  private def extractHandler(ctx: CreateFunctionContext): String =
    Option(ctx.HANDLER()).flatMap(h => ctx.string().asScala.find(occursBefore(h, _))).map(extractString).get

  private def buildPythonUDF(ctx: CreateFunctionContext): ir.PythonRuntimeInfo = {
    val packages =
      ctx
        .stringList()
        .asScala
        .find(occursBefore(ctx.PACKAGES(0), _))
        .map(_.string().asScala.map(extractString))
        .getOrElse(Seq())
    ir.PythonRuntimeInfo(extractRuntimeVersion(ctx), packages, extractHandler(ctx))
  }

  override def visitCreateTable(ctx: CreateTableContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val tableName = ctx.dotIdentifier().getText
      val columns = buildColumnDeclarations(
        ctx
          .createTableClause()
          .columnDeclItemListParen()
          .columnDeclItemList()
          .columnDeclItem()
          .asScala)
      if (ctx.REPLACE() != null) {
        ir.ReplaceTableCommand(tableName, columns, true)
      } else {
        ir.CreateTableCommand(tableName, columns)
      }

  }

  override def visitCreateTableAsSelect(ctx: CreateTableAsSelectContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val tableName = ctx.dotIdentifier().getText
      val selectStatement = ctx.queryStatement().accept(vc.relationBuilder)
      // Currently TableType is not used in the IR and Databricks doesn't support Temporary Tables
      val create = if (ctx.REPLACE() != null) {
        ir.ReplaceTableAsSelect(tableName, selectStatement, Map.empty[String, String], true, false)
      } else {
        ir.CreateTableAsSelect(tableName, selectStatement, None, None, None)
      }
      // Wrapping the CreateTableAsSelect in a CreateTableParams to maintain implementation consistency
      // TODO Capture other Table Properties
      val colConstraints = Map.empty[String, Seq[ir.Constraint]]
      val colOptions = Map.empty[String, Seq[ir.GenericOption]]
      val constraints = Seq.empty[ir.Constraint]
      val indices = Seq.empty[ir.Constraint]
      val partition = None
      val options = None
      ir.CreateTableParams(create, colConstraints, colOptions, constraints, indices, partition, options)
  }

  override def visitCreateStream(ctx: CreateStreamContext): ir.Catalog =
    ir.UnresolvedCommand(
      ruleText = contextText(ctx),
      "CREATE STREAM UNSUPPORTED",
      ruleName = contextRuleName(ctx),
      tokenName = Some("STREAM"))

  override def visitCreateTask(ctx: CreateTaskContext): ir.Catalog = {
    ir.UnresolvedCommand(
      ruleText = contextText(ctx),
      "CREATE TASK UNSUPPORTED",
      ruleName = "createTask",
      tokenName = Some("TASK"))
  }

  private def buildColumnDeclarations(ctx: Seq[ColumnDeclItemContext]): Seq[ir.ColumnDeclaration] = {
    // According to the grammar, either ctx.fullColDecl or ctx.outOfLineConstraint is non-null.
    val columns = ctx.collect {
      case c if c.fullColDecl() != null => buildColumnDeclaration(c.fullColDecl())
    }
    // An out-of-line constraint may apply to one or many columns
    // When an out-of-line constraint applies to multiple columns,
    // we record a column-name -> constraint mapping for each.
    val outOfLineConstraints: Seq[(String, ir.Constraint)] = ctx.collect {
      case c if c.outOfLineConstraint() != null => buildOutOfLineConstraints(c.outOfLineConstraint())
    }.flatten

    // Finally, for every column, we "inject" the relevant out-of-line constraints
    columns.map { col =>
      val additionalConstraints = outOfLineConstraints.collect {
        case (columnName, constraint) if columnName == col.name => constraint
      }
      col.copy(constraints = col.constraints ++ additionalConstraints)
    }
  }

  private def buildColumnDeclaration(ctx: FullColDeclContext): ir.ColumnDeclaration = {
    val name = ctx.colDecl().columnName().getText
    val dataType = vc.typeBuilder.buildDataType(ctx.colDecl().dataType())
    val constraints = ctx.inlineConstraint().asScala.map(buildInlineConstraint)
    val identityConstraints = if (ctx.defaultValue() != null) {
      ctx.defaultValue().asScala.map(buildDefaultValue)
    } else {
      Seq()
    }
    val nullability = if (ctx.NULL().isEmpty) {
      Seq()
    } else {
      Seq(ir.Nullability(ctx.NOT() == null))
    }
    ir.ColumnDeclaration(
      name,
      dataType,
      virtualColumnDeclaration = None,
      nullability ++ constraints ++ identityConstraints)
  }

  private def buildDefaultValue(ctx: DefaultValueContext): ir.Constraint = {
    ctx match {
      case c if c.DEFAULT() != null => ir.DefaultValueConstraint(c.expr().accept(vc.expressionBuilder))
      case c if c.AUTOINCREMENT() != null => ir.IdentityConstraint(None, None, always = true)
      case c if c.IDENTITY() != null =>
        ir.IdentityConstraint(Some(ctx.startWith().getText), Some(ctx.incrementBy().getText), false, true)
    }
  }

  private[snowflake] def buildOutOfLineConstraints(ctx: OutOfLineConstraintContext): Seq[(String, ir.Constraint)] = {
    val columnNames = ctx.columnListInParentheses(0).columnList().columnName().asScala.map(_.getText)
    val repeatForEveryColumnName = List.fill[ir.UnnamedConstraint](columnNames.size)(_)
    val unnamedConstraints = ctx match {
      case c if c.UNIQUE() != null => repeatForEveryColumnName(ir.Unique(Seq.empty))
      case c if c.primaryKey() != null => repeatForEveryColumnName(ir.PrimaryKey(Seq.empty))
      case c if c.foreignKey() != null =>
        val referencedObject = c.dotIdentifier().getText
        val references =
          c.columnListInParentheses(1).columnList().columnName().asScala.map(referencedObject + "." + _.getText)
        references.map(ref => ir.ForeignKey("", ref, "", Seq.empty))
      case c => repeatForEveryColumnName(ir.UnresolvedConstraint(c.getText))
    }
    val constraintNameOpt = Option(ctx.id()).map(_.getText)
    val constraints = constraintNameOpt.fold[Seq[ir.Constraint]](unnamedConstraints) { name =>
      unnamedConstraints.map(ir.NamedConstraint(name, _))
    }
    columnNames.zip(constraints)
  }

  private[snowflake] def buildInlineConstraint(ctx: InlineConstraintContext): ir.Constraint = ctx match {
    case c if c.UNIQUE() != null => ir.Unique()
    case c if c.primaryKey() != null => ir.PrimaryKey()
    case c if c.foreignKey() != null =>
      val references = c.dotIdentifier().getText + Option(ctx.columnName()).map("." + _.getText).getOrElse("")
      ir.ForeignKey("", references, "", Seq.empty)
    case c => ir.UnresolvedConstraint(c.getText)
  }

  override def visitCreateUser(ctx: CreateUserContext): ir.Catalog =
    ir.UnresolvedCommand(
      ruleText = contextText(ctx),
      message = "CREATE USER UNSUPPORTED",
      ruleName = "createUser",
      tokenName = Some("USER"))

  override def visitAlterCommand(ctx: AlterCommandContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      ctx match {
        case c if c.alterTable() != null => c.alterTable().accept(this)
        case _ =>
          ir.UnresolvedCommand(
            ruleText = contextText(ctx),
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)),
            message = s"Unknown ALTER command variant")
      }
  }

  override def visitAlterTable(ctx: AlterTableContext): ir.Catalog = errorCheck(ctx) match {
    case Some(errorResult) => errorResult
    case None =>
      val tableName = ctx.dotIdentifier(0).getText
      ctx match {
        case c if c.tableColumnAction() != null =>
          ir.AlterTableCommand(tableName, buildColumnActions(c.tableColumnAction()))
        case c if c.constraintAction() != null =>
          ir.AlterTableCommand(tableName, buildConstraintActions(c.constraintAction()))
        case _ =>
          ir.UnresolvedCommand(
            ruleText = contextText(ctx),
            message = "Unknown ALTER TABLE variant",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart)))
      }
  }

  private[snowflake] def buildColumnActions(ctx: TableColumnActionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      Seq(ir.AddColumn(c.fullColDecl().asScala.map(buildColumnDeclaration)))
    case c if !c.alterColumnClause().isEmpty =>
      c.alterColumnClause().asScala.map(buildColumnAlterations)
    case c if c.DROP() != null =>
      Seq(ir.DropColumns(c.columnList().columnName().asScala.map(_.getText)))
    case c if c.RENAME() != null =>
      Seq(ir.RenameColumn(c.columnName(0).getText, c.columnName(1).getText))
    case _ =>
      Seq(
        ir.UnresolvedTableAlteration(
          ruleText = contextText(ctx),
          message = "Unknown COLUMN action variant",
          ruleName = vc.ruleName(ctx),
          tokenName = Some(tokenName(ctx.getStart))))
  }

  private[snowflake] def buildColumnAlterations(ctx: AlterColumnClauseContext): ir.TableAlteration = {
    val columnName = ctx.columnName().getText
    ctx match {
      case c if c.dataType() != null =>
        ir.ChangeColumnDataType(columnName, vc.typeBuilder.buildDataType(c.dataType()))
      case c if c.DROP() != null && c.NULL() != null =>
        ir.DropConstraint(Some(columnName), ir.Nullability(c.NOT() == null))
      case c if c.NULL() != null =>
        ir.AddConstraint(columnName, ir.Nullability(c.NOT() == null))
      case _ =>
        ir.UnresolvedTableAlteration(
          ruleText = contextText(ctx),
          message = "Unknown ALTER COLUMN variant",
          ruleName = vc.ruleName(ctx),
          tokenName = Some(tokenName(ctx.getStart)))
    }
  }

  private[snowflake] def buildConstraintActions(ctx: ConstraintActionContext): Seq[ir.TableAlteration] = ctx match {
    case c if c.ADD() != null =>
      buildOutOfLineConstraints(c.outOfLineConstraint()).map(ir.AddConstraint.tupled)
    case c if c.DROP() != null =>
      buildDropConstraints(c)
    case c if c.RENAME() != null =>
      Seq(ir.RenameConstraint(c.id(0).getText, c.id(1).getText))
    case c =>
      Seq(
        ir.UnresolvedTableAlteration(
          ruleText = contextText(c),
          message = "Unknown CONSTRAINT variant",
          ruleName = vc.ruleName(c),
          tokenName = Some(tokenName(ctx.getStart))))
  }

  private[snowflake] def buildDropConstraints(ctx: ConstraintActionContext): Seq[ir.TableAlteration] = {
    val columnListOpt = Option(ctx.columnListInParentheses())
    val affectedColumns = columnListOpt.map(_.columnList().columnName().asScala.map(_.getText)).getOrElse(Seq())
    ctx match {
      case c if c.primaryKey() != null => dropConstraints(affectedColumns, ir.PrimaryKey())
      case c if c.UNIQUE() != null => dropConstraints(affectedColumns, ir.Unique())
      case c if c.id.size() > 0 => Seq(ir.DropConstraintByName(c.id(0).getText))
      case _ =>
        Seq(
          ir.UnresolvedTableAlteration(
            ruleText = contextText(ctx),
            message = "Unknown DROP constraint variant",
            ruleName = vc.ruleName(ctx),
            tokenName = Some(tokenName(ctx.getStart))))
    }
  }

  private def dropConstraints(affectedColumns: Seq[String], constraint: ir.Constraint): Seq[ir.TableAlteration] = {
    if (affectedColumns.isEmpty) {
      Seq(ir.DropConstraint(None, constraint))
    } else {
      affectedColumns.map(col => ir.DropConstraint(Some(col), constraint))
    }
  }

}
