package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.{Result, WorkflowStage, intermediate => ir}

class LogicalPlanGenerator(
    val expr: ExpressionGenerator,
    val optGen: OptionGenerator,
    val explicitDistinct: Boolean = false)
    extends Generator[ir.LogicalPlan, String] {

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): SQL = tree match {
    case b: ir.Batch => batch(ctx, b)
    case w: ir.WithCTE => cte(ctx, w)
    case p: ir.Project => project(ctx, p)
    case ir.NamedTable(id, _, _) => Result.Success(id)
    case ir.Filter(input, condition) =>
      sql"${generate(ctx, input)} WHERE ${expr.generate(ctx, condition)}"
    case ir.Limit(input, limit) =>
      sql"${generate(ctx, input)} LIMIT ${expr.generate(ctx, limit)}"
    case ir.Offset(child, offset) =>
      sql"${generate(ctx, child)} OFFSET ${expr.generate(ctx, offset)}"
    case ir.Values(data) =>
      sql"VALUES ${data.map(_.map(expr.generate(ctx, _)).mkSql("(", ",", ")")).mkSql(", ")}"
    case agg: ir.Aggregate => aggregate(ctx, agg)
    case sort: ir.Sort => orderBy(ctx, sort)
    case join: ir.Join => generateJoin(ctx, join)
    case setOp: ir.SetOperation => setOperation(ctx, setOp)
    case mergeIntoTable: ir.MergeIntoTable => merge(ctx, mergeIntoTable)
    case withOptions: ir.WithOptions => generateWithOptions(ctx, withOptions)
    case s: ir.SubqueryAlias => subQueryAlias(ctx, s)
    case t: ir.TableAlias => tableAlias(ctx, t)
    case d: ir.Deduplicate => deduplicate(ctx, d)
    case u: ir.UpdateTable => update(ctx, u)
    case i: ir.InsertIntoTable => insert(ctx, i)
    case ir.DeleteFromTable(target, None, where, None, None) => delete(ctx, target, where)
    case c: ir.CreateTableCommand => createTable(ctx, c)
    case t: ir.TableSample => tableSample(ctx, t)
    case a: ir.AlterTableCommand => alterTable(ctx, a)
    case l: ir.Lateral => lateral(ctx, l)
    case c: ir.CreateTableParams => createTableParams(ctx, c)
    case ir.NoopNode => sql""
    //  TODO We should always generate an unresolved node, our plan should never be null
    case null => sql"" // don't fail transpilation if the plan is null
    case x => unknown(x)
  }

  private def batch(ctx: GeneratorContext, b: ir.Batch): SQL = {
    val seqSql = b.children
      .map {
        case u: ir.UnresolvedCommand =>
          sql"-- ${u.ruleText.stripSuffix(";")}"
        case query => sql"${generate(ctx, query)}"
      }
      .filter(_.isSuccess)
    if (seqSql.nonEmpty) {
      seqSql.mkSql("", ";\n", ";")
    } else {
      sql""
    }
  }

  private def createTableParams(ctx: GeneratorContext, crp: ir.CreateTableParams): SQL = {

    // We build the overall table creation statement differently depending on whether the primitive is
    // a CREATE TABLE or a CREATE TABLE AS (SELECT ...)
    crp.create match {
      case ct: ir.CreateTable =>
        // we build the columns using the raw column declarations, adding in any col constraints
        // and any column options
        val columns = ct.schema match {
          case ir.StructType(fields) =>
            fields
              .map { col =>
                val constraints = crp.colConstraints.getOrElse(col.name, Seq.empty)
                val options = crp.colOptions.getOrElse(col.name, Seq.empty)
                genColumnDecl(ctx, col, constraints, options)
              }
              .mkSql(", ")
        }

        // We now generate any table level constraints
        val tableConstraintStr = crp.constraints.map(constraint(ctx, _)).mkSql(", ")
        val tableConstraintStrWithComma = if (tableConstraintStr.nonEmpty) sql", $tableConstraintStr" else sql""

        // record any table level options
        val tableOptions = crp.options.map(_.map(optGen.generateOption(ctx, _)).mkSql("\n   ")).getOrElse(sql"")

        val tableOptionsComment =
          if (tableOptions.isEmpty) sql"" else sql"   The following options are unsupported:\n\n   $tableOptions\n"
        val indicesStr = crp.indices.map(constraint(ctx, _)).mkSql("   \n")
        val indicesComment =
          if (indicesStr.isEmpty) sql""
          else sql"   The following index directives are unsupported:\n\n   $indicesStr*/\n"
        val leadingComment = (tableOptionsComment, indicesComment) match {
          case (Result.Success(""), Result.Success("")) => Result.Success("")
          case (a, Result.Success("")) => sql"/*\n$a*/\n"
          case (Result.Success(""), b) => sql"/*\n$b*/\n"
          case (a, b) => sql"/*\n$a\n$b*/\n"
        }

        sql"${leadingComment}CREATE TABLE ${ct.table_name} (${columns}${tableConstraintStrWithComma})"

      case ctas: ir.CreateTableAsSelect => sql"CREATE TABLE ${ctas.table_name} AS ${generate(ctx, ctas.query)}"
    }
  }

  private def genColumnDecl(
      ctx: GeneratorContext,
      col: ir.StructField,
      constraints: Seq[ir.Constraint],
      options: Seq[ir.GenericOption]): SQL = {
    val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
    val dataTypeStr = if (!col.nullable) sql"$dataType NOT NULL" else dataType
    val constraintsStr = constraints.map(constraint(ctx, _)).mkSql(" ")
    val constraintsGen = if (constraintsStr.nonEmpty) sql" $constraintsStr" else sql""
    val optionsStr = options.map(optGen.generateOption(ctx, _)).mkSql(" ")
    val optionsComment = if (optionsStr.nonEmpty) sql" /* $optionsStr */" else sql""
    sql"${col.name} ${dataTypeStr}${constraintsGen}${optionsComment}"
  }

  private def alterTable(ctx: GeneratorContext, a: ir.AlterTableCommand): SQL = {
    val operation = buildTableAlteration(ctx, a.alterations)
    sql"ALTER TABLE  ${a.tableName} $operation"
  }

  private def buildTableAlteration(ctx: GeneratorContext, alterations: Seq[ir.TableAlteration]): SQL = {
    // docs:https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table.html#parameters
    // docs:https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table#syntax
    // ADD COLUMN can be Seq[ir.TableAlteration]
    // DROP COLUMN will be ir.TableAlteration since it stored the list of columns
    // DROP CONSTRAINTS BY NAME is ir.TableAlteration
    // RENAME COLUMN/ RENAME CONSTRAINTS Always be ir.TableAlteration
    // ALTER COLUMN IS A Seq[ir.TableAlternations] Data Type Change, Constraint Changes etc
    alterations map {
      case ir.AddColumn(columns) => sql"ADD COLUMN ${buildAddColumn(ctx, columns)}"
      case ir.DropColumns(columns) => sql"DROP COLUMN ${columns.mkString(", ")}"
      case ir.DropConstraintByName(constraints) => sql"DROP CONSTRAINT ${constraints}"
      case ir.RenameColumn(oldName, newName) => sql"RENAME COLUMN ${oldName} to ${newName}"
      case x => Result.Failure(WorkflowStage.GENERATE, ir.UnexpectedTableAlteration(x))
    } mkSql ", "
  }

  private def buildAddColumn(ctx: GeneratorContext, columns: Seq[ir.ColumnDeclaration]): SQL = {
    columns
      .map { c =>
        val dataType = DataTypeGenerator.generateDataType(ctx, c.dataType)
        val constraints = c.constraints.map(constraint(ctx, _)).mkSql(" ")
        sql"${c.name} $dataType $constraints"
      }
      .mkSql(", ")
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view.html
  private def lateral(ctx: GeneratorContext, lateral: ir.Lateral): SQL = lateral match {
    case ir.Lateral(ir.TableFunction(fn), isOuter, isView) =>
      val outer = if (isOuter) " OUTER" else ""
      val view = if (isView) " VIEW" else ""
      sql"LATERAL$view$outer ${expr.generate(ctx, fn)}"
    case _ => Result.Failure(WorkflowStage.GENERATE, ir.UnexpectedNode(lateral))
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-sampling.html
  private def tableSample(ctx: GeneratorContext, t: ir.TableSample): SQL = {
    val sampling = t.samplingMethod match {
      case ir.RowSamplingProbabilistic(probability) => s"$probability PERCENT"
      case ir.RowSamplingFixedAmount(amount) => s"$amount ROWS"
      case ir.BlockSampling(probability) => s"BUCKET $probability OUT OF 1"
    }
    val seed = t.seed.map(s => s" REPEATABLE ($s)").getOrElse("")
    sql"(${generate(ctx, t.child)}) TABLESAMPLE ($sampling)$seed"
  }

  private def createTable(ctx: GeneratorContext, createTable: ir.CreateTableCommand): SQL = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
        val constraints = col.constraints.map(constraint(ctx, _)).mkSql(" ")
        sql"${col.name} $dataType $constraints"
      }
    sql"CREATE TABLE ${createTable.name} (${columns.mkSql(", ")})"
  }

  private def constraint(ctx: GeneratorContext, c: ir.Constraint): SQL = c match {
    case unique: ir.Unique => generateUniqueConstraint(ctx, unique)
    case ir.Nullability(nullable) => Result.Success(if (nullable) "NULL" else "NOT NULL")
    case pk: ir.PrimaryKey => generatePrimaryKey(ctx, pk)
    case fk: ir.ForeignKey => generateForeignKey(ctx, fk)
    case ir.NamedConstraint(name, unnamed) => sql"CONSTRAINT $name ${constraint(ctx, unnamed)}"
    case ir.UnresolvedConstraint(inputText) => sql"/** $inputText **/"
    case ir.CheckConstraint(e) => sql"CHECK (${expr.generate(ctx, e)})"
    case ir.DefaultValueConstraint(value) => sql"DEFAULT ${expr.generate(ctx, value)}"
    case ir.IdentityConstraint(seed, step) => sql"IDENTITY ($seed, $step)"
  }

  private def generateForeignKey(ctx: GeneratorContext, fk: ir.ForeignKey): SQL = {
    val colNames = fk.tableCols match {
      case "" => ""
      case cols => s"(${cols}) "
    }
    val commentOptions = optGen.generateOptionList(ctx, fk.options) match {
      case "" => ""
      case options => s" /* Unsupported:  $options */"
    }
    sql"FOREIGN KEY ${colNames}REFERENCES ${fk.refObject}(${fk.refCols})$commentOptions"
  }

  private def generatePrimaryKey(context: GeneratorContext, key: ir.PrimaryKey): SQL = {
    val columns = key.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val commentOptions = optGen.generateOptionList(context, key.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    val columnsStr = if (columns.isEmpty) "" else s" $columns"
    sql"PRIMARY KEY${columnsStr}${commentOptions}"
  }

  private def generateUniqueConstraint(ctx: GeneratorContext, unique: ir.Unique): SQL = {
    val columns = unique.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val columnStr = if (columns.isEmpty) "" else s" $columns"
    val commentOptions = optGen.generateOptionList(ctx, unique.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    sql"UNIQUE${columnStr}${commentOptions}"
  }

  private def project(ctx: GeneratorContext, proj: ir.Project): SQL = {
    val fromClause = if (proj.input != ir.NoTable()) {
      sql" FROM ${generate(ctx, proj.input)}"
    } else {
      sql""
    }
    sql"SELECT ${proj.expressions.map(expr.generate(ctx, _)).mkSql(", ")}$fromClause"
  }

  private def orderBy(ctx: GeneratorContext, sort: ir.Sort): SQL = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        val dir = direction match {
          case ir.Ascending => ""
          case ir.Descending => " DESC"
        }
        sql"${expr.generate(ctx, child)}$dir ${nulls.sql}"
      }

    sql"${generate(ctx, sort.child)} ORDER BY ${orderStr.mkSql(", ")}"
  }

  private def isLateralView(lp: ir.LogicalPlan): Boolean = {
    lp.find {
      case ir.Lateral(_, _, isView) => isView
      case _ => false
    }.isDefined
  }

  private def generateJoin(ctx: GeneratorContext, join: ir.Join): SQL = {
    val left = generate(ctx, join.left)
    val right = generate(ctx, join.right)
    if (join.join_condition.isEmpty && join.using_columns.isEmpty && join.join_type == ir.InnerJoin) {
      if (isLateralView(join.right)) {
        sql"$left $right"
      } else {
        sql"$left, $right"
      }
    } else {
      val joinType = generateJoinType(join.join_type)
      val joinClause = if (joinType.isEmpty) { "JOIN" }
      else { joinType + " JOIN" }
      val conditionOpt = join.join_condition.map(expr.generate(ctx, _))
      val condition = join.join_condition match {
        case None => sql""
        case Some(_: ir.And) | Some(_: ir.Or) => sql"ON (${conditionOpt.get})"
        case Some(_) => sql"ON ${conditionOpt.get}"
      }
      val usingColumns = join.using_columns.mkString(", ")
      val using = if (usingColumns.isEmpty) "" else s"USING ($usingColumns)"
      for {
        l <- left
        r <- right
        cond <- condition
      } yield {
        Seq(l, joinClause, r, cond, using).filterNot(_.isEmpty).mkString(" ")
      }
    }
  }

  private def generateJoinType(joinType: ir.JoinType): String = joinType match {
    case ir.InnerJoin => "INNER"
    case ir.FullOuterJoin => "FULL OUTER"
    case ir.LeftOuterJoin => "LEFT"
    case ir.LeftSemiJoin => "LEFT SEMI"
    case ir.LeftAntiJoin => "LEFT ANTI"
    case ir.RightOuterJoin => "RIGHT"
    case ir.CrossJoin => "CROSS"
    case ir.NaturalJoin(ir.UnspecifiedJoin) => "NATURAL"
    case ir.NaturalJoin(jt) => s"NATURAL ${generateJoinType(jt)}"
    case ir.UnspecifiedJoin => ""
  }

  private def setOperation(ctx: GeneratorContext, setOp: ir.SetOperation): SQL = {
    if (setOp.allow_missing_columns) {
      return Result.Failure(WorkflowStage.GENERATE, ir.UnexpectedNode(setOp))
    }
    if (setOp.by_name) {
      return Result.Failure(WorkflowStage.GENERATE, ir.UnexpectedNode(setOp))
    }
    val op = setOp.set_op_type match {
      case ir.UnionSetOp => "UNION"
      case ir.IntersectSetOp => "INTERSECT"
      case ir.ExceptSetOp => "EXCEPT"
      case _ => return Result.Failure(WorkflowStage.GENERATE, ir.UnexpectedNode(setOp))
    }
    val duplicates = if (setOp.is_all) " ALL" else if (explicitDistinct) " DISTINCT" else ""
    sql"(${generate(ctx, setOp.left)}) $op$duplicates (${generate(ctx, setOp.right)})"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-insert-into.html
  private def insert(ctx: GeneratorContext, insert: ir.InsertIntoTable): SQL = {
    val target = generate(ctx, insert.target)
    val columns =
      insert.columns.map(cols => cols.map(expr.generate(ctx, _)).mkSql("(", ", ", ")")).getOrElse(sql"")
    val values = generate(ctx, insert.values)
    val output = insert.outputRelation.map(generate(ctx, _)).getOrElse(sql"")
    val options = insert.options.map(expr.generate(ctx, _)).getOrElse(sql"")
    val overwrite = if (insert.overwrite) "OVERWRITE TABLE" else "INTO"
    sql"INSERT $overwrite $target $columns $values$output$options"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-update.html
  private def update(ctx: GeneratorContext, update: ir.UpdateTable): SQL = {
    val target = generate(ctx, update.target)
    val set = update.set.map(expr.generate(ctx, _)).mkSql(", ")
    val where = update.where.map(cond => sql" WHERE ${expr.generate(ctx, cond)}").getOrElse("")
    sql"UPDATE $target SET $set$where"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-delete-from.html
  private def delete(ctx: GeneratorContext, target: ir.LogicalPlan, where: Option[ir.Expression]): SQL = {
    val whereStr = where.map(cond => sql" WHERE ${expr.generate(ctx, cond)}").getOrElse(sql"")
    sql"DELETE FROM ${generate(ctx, target)}$whereStr"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html
  private def merge(ctx: GeneratorContext, mergeIntoTable: ir.MergeIntoTable): SQL = {
    val target = generate(ctx, mergeIntoTable.targetTable)
    val source = generate(ctx, mergeIntoTable.sourceTable)
    val condition = expr.generate(ctx, mergeIntoTable.mergeCondition)
    val matchedActions =
      mergeIntoTable.matchedActions.map { action =>
        val conditionText = action.condition.map(cond => sql" AND ${expr.generate(ctx, cond)}").getOrElse(sql"")
        sql" WHEN MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkSql

    val notMatchedActions =
      mergeIntoTable.notMatchedActions.map { action =>
        val conditionText = action.condition.map(cond => sql" AND ${expr.generate(ctx, cond)}").getOrElse(sql"")
        sql" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkSql
    val notMatchedBySourceActions =
      mergeIntoTable.notMatchedBySourceActions.map { action =>
        val conditionText = action.condition.map(cond => sql" AND ${expr.generate(ctx, cond)}").getOrElse(sql"")
        sql" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkSql
    sql"""MERGE INTO $target
       |USING $source
       |ON $condition
       |$matchedActions
       |$notMatchedActions
       |$notMatchedBySourceActions
       |""".map(_.stripMargin)
  }

  private def aggregate(ctx: GeneratorContext, aggregate: ir.Aggregate): SQL = {
    val child = generate(ctx, aggregate.child)
    val expressions = aggregate.grouping_expressions.map(expr.generate(ctx, _)).mkSql(", ")
    aggregate.group_type match {
      case ir.GroupBy =>
        sql"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(ctx, pivot.col)
        val values = pivot.values.map(expr.generate(ctx, _)).mkSql(" IN(", ", ", ")")
        sql"$child PIVOT($expressions FOR $col$values)"
      case a => Result.Failure(WorkflowStage.GENERATE, ir.UnsupportedGroupType(a))
    }
  }
  private def generateWithOptions(ctx: GeneratorContext, withOptions: ir.WithOptions): SQL = {
    val optionComments = expr.generate(ctx, withOptions.options)
    val plan = generate(ctx, withOptions.input)
    sql"${optionComments}${plan}"
  }

  private def cte(ctx: GeneratorContext, withCte: ir.WithCTE): SQL = {
    val ctes = withCte.ctes
      .map {
        case ir.SubqueryAlias(child, alias, cols) =>
          val columns = cols.map(expr.generate(ctx, _)).mkSql("(", ", ", ")")
          val columnsStr = if (cols.isEmpty) sql"" else sql" $columns"
          val id = expr.generate(ctx, alias)
          val sub = generate(ctx, child)
          sql"$id$columnsStr AS ($sub)"
        case x => generate(ctx, x)
      }
    val query = generate(ctx, withCte.query)
    sql"WITH ${ctes.mkSql(", ")} $query"
  }

  private def subQueryAlias(ctx: GeneratorContext, subQAlias: ir.SubqueryAlias): SQL = {
    val subquery = subQAlias.child match {
      case l: ir.Lateral => lateral(ctx, l)
      case _ => sql"(${generate(ctx, subQAlias.child)})"
    }
    val tableName = expr.generate(ctx, subQAlias.alias)
    val table =
      if (subQAlias.columnNames.isEmpty) {
        sql"AS $tableName"
      } else {
        // Added this to handle the case for POS Explode
        // We have added two columns index and value as an alias for pos explode default columns (pos, col)
        // these column will be added to the databricks query
        subQAlias.columnNames match {
          case Seq(ir.Id("value", _), ir.Id("index", _)) =>
            val columnNamesStr =
              subQAlias.columnNames.sortBy(_.nodeName).reverse.map(expr.generate(ctx, _))
            sql"$tableName AS ${columnNamesStr.mkSql(", ")}"
          case _ =>
            val columnNamesStr = subQAlias.columnNames.map(expr.generate(ctx, _))
            sql"AS $tableName${columnNamesStr.mkSql("(", ", ", ")")}"
        }
      }
    sql"$subquery $table"
  }

  private def tableAlias(ctx: GeneratorContext, alias: ir.TableAlias): SQL = {
    val target = generate(ctx, alias.child)
    val columns = if (alias.columns.isEmpty) { sql"" }
    else {
      alias.columns.map(expr.generate(ctx, _)).mkSql("(", ", ", ")")
    }
    sql"$target AS ${alias.alias}$columns"
  }

  private def deduplicate(ctx: GeneratorContext, dedup: ir.Deduplicate): SQL = {
    val table = generate(ctx, dedup.child)
    val columns = if (dedup.all_columns_as_keys) { sql"*" }
    else {
      dedup.column_names.map(expr.generate(ctx, _)).mkSql(", ")
    }
    sql"SELECT DISTINCT $columns FROM $table"
  }
}
