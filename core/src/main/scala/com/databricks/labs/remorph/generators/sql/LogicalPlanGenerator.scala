package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, RemorphContext, TBA, TBAS, intermediate => ir}

class LogicalPlanGenerator(
    val expr: ExpressionGenerator,
    val optGen: OptionGenerator,
    val explicitDistinct: Boolean = false)
    extends BaseSQLGenerator[ir.LogicalPlan]
    with TBAS[RemorphContext] {

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): TBA[RemorphContext, String] = {

    val sql: TBA[RemorphContext, String] = tree match {
      case b: ir.Batch => batch(ctx, b)
      case w: ir.WithCTE => cte(ctx, w)
      case p: ir.Project => project(ctx, p)
      case ir.NamedTable(id, _, _) => lift(OkResult(id))
      case ir.Filter(input, condition) =>
        tba"${generate(ctx, input)} WHERE ${expr.generate(ctx, condition)}"
      case ir.Limit(input, limit) =>
        tba"${generate(ctx, input)} LIMIT ${expr.generate(ctx, limit)}"
      case ir.Offset(child, offset) =>
        tba"${generate(ctx, child)} OFFSET ${expr.generate(ctx, offset)}"
      case ir.Values(data) =>
        tba"VALUES ${data.map(_.map(expr.generate(ctx, _)).mkTba("(", ",", ")")).mkTba(", ")}"
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
      // We see an unresolved for parsing errors, when we have no visitor for a given rule,
      // when something went wrong with IR generation, or when we have a visitor but it is not
      // yet implemented.
      case u: ir.Unresolved[_] => describeError(u)
      case ir.NoopNode => tba""

      case null => tba"" // don't fail transpilation if the plan is null
      case x => partialResult(x)
    }

    update { case g: Generating =>
      g.copy(currentNode = tree)
    }.flatMap(_ => sql)
  }

  private def batch(ctx: GeneratorContext, b: ir.Batch): TBA[RemorphContext, String] = {
    val seqSql = b.children.map(generate(ctx, _)).sequence
    seqSql.map { seq =>
      seq
        .map { elem =>
          if (!elem.endsWith("*/")) s"$elem;"
          else elem
        }
        .mkString("\n")
    }
  }

  private def createTableParams(ctx: GeneratorContext, crp: ir.CreateTableParams): TBA[RemorphContext, String] = {

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
              .mkTba(", ")
        }

        // We now generate any table level constraints
        val tableConstraintStr = crp.constraints.map(constraint(ctx, _)).mkTba(", ")
        val tableConstraintStrWithComma =
          tableConstraintStr.nonEmpty.flatMap(nonEmpty => if (nonEmpty) tba", $tableConstraintStr" else tba"")

        // record any table level options
        val tableOptions = crp.options.map(_.map(optGen.generateOption(ctx, _)).mkTba("\n   ")).getOrElse(tba"")

        val tableOptionsComment = {
          tableOptions.isEmpty.flatMap { isEmpty =>
            if (isEmpty) tba"" else tba"   The following options are unsupported:\n\n   $tableOptions\n"
          }
        }
        val indicesStr = crp.indices.map(constraint(ctx, _)).mkTba("   \n")
        val indicesComment =
          indicesStr.isEmpty.flatMap { isEmpty =>
            if (isEmpty) tba""
            else tba"   The following index directives are unsupported:\n\n   $indicesStr*/\n"
          }
        val leadingComment = {
          for {
            toc <- tableOptionsComment
            ic <- indicesComment
          } yield (toc, ic) match {
            case ("", "") => ""
            case (a, "") => s"/*\n$a*/\n"
            case ("", b) => s"/*\n$b*/\n"
            case (a, b) => s"/*\n$a\n$b*/\n"
          }
        }

        tba"${leadingComment}CREATE TABLE ${ct.table_name} (${columns}${tableConstraintStrWithComma})"

      case ctas: ir.CreateTableAsSelect => tba"CREATE TABLE ${ctas.table_name} AS ${generate(ctx, ctas.query)}"
    }
  }

  private def genColumnDecl(
      ctx: GeneratorContext,
      col: ir.StructField,
      constraints: Seq[ir.Constraint],
      options: Seq[ir.GenericOption]): TBA[RemorphContext, String] = {
    val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
    val dataTypeStr = if (!col.nullable) tba"$dataType NOT NULL" else dataType
    val constraintsStr = constraints.map(constraint(ctx, _)).mkTba(" ")
    val constraintsGen = constraintsStr.nonEmpty.flatMap { nonEmpty => if (nonEmpty) tba" $constraintsStr" else tba"" }
    val optionsStr = options.map(optGen.generateOption(ctx, _)).mkTba(" ")
    val optionsComment = optionsStr.nonEmpty.flatMap { nonEmpty => if (nonEmpty) tba" /* $optionsStr */" else tba"" }
    tba"${col.name} ${dataTypeStr}${constraintsGen}${optionsComment}"
  }

  private def alterTable(ctx: GeneratorContext, a: ir.AlterTableCommand): TBA[RemorphContext, String] = {
    val operation = buildTableAlteration(ctx, a.alterations)
    tba"ALTER TABLE  ${a.tableName} $operation"
  }

  private def buildTableAlteration(
      ctx: GeneratorContext,
      alterations: Seq[ir.TableAlteration]): TBA[RemorphContext, String] = {
    // docs:https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table.html#parameters
    // docs:https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table#syntax
    // ADD COLUMN can be Seq[ir.TableAlteration]
    // DROP COLUMN will be ir.TableAlteration since it stored the list of columns
    // DROP CONSTRAINTS BY NAME is ir.TableAlteration
    // RENAME COLUMN/ RENAME CONSTRAINTS Always be ir.TableAlteration
    // ALTER COLUMN IS A Seq[ir.TableAlternations] Data Type Change, Constraint Changes etc
    alterations map {
      case ir.AddColumn(columns) => tba"ADD COLUMN ${buildAddColumn(ctx, columns)}"
      case ir.DropColumns(columns) => tba"DROP COLUMN ${columns.mkString(", ")}"
      case ir.DropConstraintByName(constraints) => tba"DROP CONSTRAINT ${constraints}"
      case ir.RenameColumn(oldName, newName) => tba"RENAME COLUMN ${oldName} to ${newName}"
      case x => partialResult(x, ir.UnexpectedTableAlteration(x.toString))
    } mkTba ", "
  }

  private def buildAddColumn(ctx: GeneratorContext, columns: Seq[ir.ColumnDeclaration]): TBA[RemorphContext, String] = {
    columns
      .map { c =>
        val dataType = DataTypeGenerator.generateDataType(ctx, c.dataType)
        val constraints = c.constraints.map(constraint(ctx, _)).mkTba(" ")
        tba"${c.name} $dataType $constraints"
      }
      .mkTba(", ")
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view.html
  private def lateral(ctx: GeneratorContext, lateral: ir.Lateral): TBA[RemorphContext, String] = lateral match {
    case ir.Lateral(ir.TableFunction(fn), isOuter, isView) =>
      val outer = if (isOuter) " OUTER" else ""
      val view = if (isView) " VIEW" else ""
      tba"LATERAL$view$outer ${expr.generate(ctx, fn)}"
    case _ => partialResult(lateral)
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-sampling.html
  private def tableSample(ctx: GeneratorContext, t: ir.TableSample): TBA[RemorphContext, String] = {
    val sampling = t.samplingMethod match {
      case ir.RowSamplingProbabilistic(probability) => s"$probability PERCENT"
      case ir.RowSamplingFixedAmount(amount) => s"$amount ROWS"
      case ir.BlockSampling(probability) => s"BUCKET $probability OUT OF 1"
    }
    val seed = t.seed.map(s => s" REPEATABLE ($s)").getOrElse("")
    tba"(${generate(ctx, t.child)}) TABLESAMPLE ($sampling)$seed"
  }

  private def createTable(ctx: GeneratorContext, createTable: ir.CreateTableCommand): TBA[RemorphContext, String] = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
        val constraints = col.constraints.map(constraint(ctx, _)).mkTba(" ")
        tba"${col.name} $dataType $constraints"
      }
    tba"CREATE TABLE ${createTable.name} (${columns.mkTba(", ")})"
  }

  private def constraint(ctx: GeneratorContext, c: ir.Constraint): TBA[RemorphContext, String] = c match {
    case unique: ir.Unique => generateUniqueConstraint(ctx, unique)
    case ir.Nullability(nullable) => lift(OkResult(if (nullable) "NULL" else "NOT NULL"))
    case pk: ir.PrimaryKey => generatePrimaryKey(ctx, pk)
    case fk: ir.ForeignKey => generateForeignKey(ctx, fk)
    case ir.NamedConstraint(name, unnamed) => tba"CONSTRAINT $name ${constraint(ctx, unnamed)}"
    case ir.UnresolvedConstraint(inputText) => tba"/** $inputText **/"
    case ir.CheckConstraint(e) => tba"CHECK (${expr.generate(ctx, e)})"
    case ir.DefaultValueConstraint(value) => tba"DEFAULT ${expr.generate(ctx, value)}"
    case ir.IdentityConstraint(seed, step) => tba"IDENTITY ($seed, $step)"
  }

  private def generateForeignKey(ctx: GeneratorContext, fk: ir.ForeignKey): TBA[RemorphContext, String] = {
    val colNames = fk.tableCols match {
      case "" => ""
      case cols => s"(${cols}) "
    }
    val commentOptions = optGen.generateOptionList(ctx, fk.options) match {
      case "" => ""
      case options => s" /* Unsupported:  $options */"
    }
    tba"FOREIGN KEY ${colNames}REFERENCES ${fk.refObject}(${fk.refCols})$commentOptions"
  }

  private def generatePrimaryKey(context: GeneratorContext, key: ir.PrimaryKey): TBA[RemorphContext, String] = {
    val columns = key.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val commentOptions = optGen.generateOptionList(context, key.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    val columnsStr = if (columns.isEmpty) "" else s" $columns"
    tba"PRIMARY KEY${columnsStr}${commentOptions}"
  }

  private def generateUniqueConstraint(ctx: GeneratorContext, unique: ir.Unique): TBA[RemorphContext, String] = {
    val columns = unique.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val columnStr = if (columns.isEmpty) "" else s" $columns"
    val commentOptions = optGen.generateOptionList(ctx, unique.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    tba"UNIQUE${columnStr}${commentOptions}"
  }

  private def project(ctx: GeneratorContext, proj: ir.Project): TBA[RemorphContext, String] = {
    val fromClause = if (proj.input != ir.NoTable()) {
      tba" FROM ${generate(ctx, proj.input)}"
    } else {
      tba""
    }

    // Don't put commas after unresolved expressions as they are error comments only
    val sqlParts = proj.expressions
      .map {
        case u: ir.Unresolved[_] => expr.generate(ctx, u)
        case exp: ir.Expression => expr.generate(ctx, exp).map(_ + ", ")
      }
      .sequence
      .map(_.mkString.stripSuffix(", "))

    tba"SELECT $sqlParts$fromClause"
  }

  private def orderBy(ctx: GeneratorContext, sort: ir.Sort): TBA[RemorphContext, String] = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        val dir = direction match {
          case ir.Ascending => ""
          case ir.Descending => " DESC"
        }
        tba"${expr.generate(ctx, child)}$dir ${nulls.sql}"
      }

    tba"${generate(ctx, sort.child)} ORDER BY ${orderStr.mkTba(", ")}"
  }

  private def isLateralView(lp: ir.LogicalPlan): Boolean = {
    lp.find {
      case ir.Lateral(_, _, isView) => isView
      case _ => false
    }.isDefined
  }

  private def generateJoin(ctx: GeneratorContext, join: ir.Join): TBA[RemorphContext, String] = {
    val left = generate(ctx, join.left)
    val right = generate(ctx, join.right)
    if (join.join_condition.isEmpty && join.using_columns.isEmpty && join.join_type == ir.InnerJoin) {
      if (isLateralView(join.right)) {
        tba"$left $right"
      } else {
        tba"$left, $right"
      }
    } else {
      val joinType = generateJoinType(join.join_type)
      val joinClause = if (joinType.isEmpty) { "JOIN" }
      else { joinType + " JOIN" }
      val conditionOpt = join.join_condition.map(expr.generate(ctx, _))
      val condition = join.join_condition match {
        case None => tba""
        case Some(_: ir.And) | Some(_: ir.Or) => tba"ON (${conditionOpt.get})"
        case Some(_) => tba"ON ${conditionOpt.get}"
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

  private def setOperation(ctx: GeneratorContext, setOp: ir.SetOperation): TBA[RemorphContext, String] = {
    if (setOp.allow_missing_columns) {
      return partialResult(setOp)
    }
    if (setOp.by_name) {
      return partialResult(setOp)
    }
    val op = setOp.set_op_type match {
      case ir.UnionSetOp => "UNION"
      case ir.IntersectSetOp => "INTERSECT"
      case ir.ExceptSetOp => "EXCEPT"
      case _ => return partialResult(setOp)
    }
    val duplicates = if (setOp.is_all) " ALL" else if (explicitDistinct) " DISTINCT" else ""
    tba"(${generate(ctx, setOp.left)}) $op$duplicates (${generate(ctx, setOp.right)})"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-insert-into.html
  private def insert(ctx: GeneratorContext, insert: ir.InsertIntoTable): TBA[RemorphContext, String] = {
    val target = generate(ctx, insert.target)
    val columns =
      insert.columns.map(cols => cols.map(expr.generate(ctx, _)).mkTba("(", ", ", ")")).getOrElse(tba"")
    val values = generate(ctx, insert.values)
    val output = insert.outputRelation.map(generate(ctx, _)).getOrElse(tba"")
    val options = insert.options.map(expr.generate(ctx, _)).getOrElse(tba"")
    val overwrite = if (insert.overwrite) "OVERWRITE TABLE" else "INTO"
    tba"INSERT $overwrite $target $columns $values$output$options"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-update.html
  private def update(ctx: GeneratorContext, update: ir.UpdateTable): TBA[RemorphContext, String] = {
    val target = generate(ctx, update.target)
    val set = update.set.map(expr.generate(ctx, _)).mkTba(", ")
    val where = update.where.map(cond => tba" WHERE ${expr.generate(ctx, cond)}").getOrElse("")
    tba"UPDATE $target SET $set$where"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-delete-from.html
  private def delete(
      ctx: GeneratorContext,
      target: ir.LogicalPlan,
      where: Option[ir.Expression]): TBA[RemorphContext, String] = {
    val whereStr = where.map(cond => tba" WHERE ${expr.generate(ctx, cond)}").getOrElse(tba"")
    tba"DELETE FROM ${generate(ctx, target)}$whereStr"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html
  private def merge(ctx: GeneratorContext, mergeIntoTable: ir.MergeIntoTable): TBA[RemorphContext, String] = {
    val target = generate(ctx, mergeIntoTable.targetTable)
    val source = generate(ctx, mergeIntoTable.sourceTable)
    val condition = expr.generate(ctx, mergeIntoTable.mergeCondition)
    val matchedActions =
      mergeIntoTable.matchedActions.map { action =>
        val conditionText = action.condition.map(cond => tba" AND ${expr.generate(ctx, cond)}").getOrElse(tba"")
        tba" WHEN MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkTba

    val notMatchedActions =
      mergeIntoTable.notMatchedActions.map { action =>
        val conditionText = action.condition.map(cond => tba" AND ${expr.generate(ctx, cond)}").getOrElse(tba"")
        tba" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkTba
    val notMatchedBySourceActions =
      mergeIntoTable.notMatchedBySourceActions.map { action =>
        val conditionText = action.condition.map(cond => tba" AND ${expr.generate(ctx, cond)}").getOrElse(tba"")
        tba" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkTba
    tba"""MERGE INTO $target
       |USING $source
       |ON $condition
       |$matchedActions
       |$notMatchedActions
       |$notMatchedBySourceActions
       |""".map(_.stripMargin)
  }

  private def aggregate(ctx: GeneratorContext, aggregate: ir.Aggregate): TBA[RemorphContext, String] = {
    val child = generate(ctx, aggregate.child)
    val expressions = aggregate.grouping_expressions.map(expr.generate(ctx, _)).mkTba(", ")
    aggregate.group_type match {
      case ir.GroupBy =>
        tba"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(ctx, pivot.col)
        val values = pivot.values.map(expr.generate(ctx, _)).mkTba(" IN(", ", ", ")")
        tba"$child PIVOT($expressions FOR $col$values)"
      case a => partialResult(a, ir.UnsupportedGroupType(a.toString))
    }
  }
  private def generateWithOptions(ctx: GeneratorContext, withOptions: ir.WithOptions): TBA[RemorphContext, String] = {
    val optionComments = expr.generate(ctx, withOptions.options)
    val plan = generate(ctx, withOptions.input)
    tba"${optionComments}${plan}"
  }

  private def cte(ctx: GeneratorContext, withCte: ir.WithCTE): TBA[RemorphContext, String] = {
    val ctes = withCte.ctes
      .map {
        case ir.SubqueryAlias(child, alias, cols) =>
          val columns = cols.map(expr.generate(ctx, _)).mkTba("(", ", ", ")")
          val columnsStr = if (cols.isEmpty) tba"" else tba" $columns"
          val id = expr.generate(ctx, alias)
          val sub = generate(ctx, child)
          tba"$id$columnsStr AS ($sub)"
        case x => generate(ctx, x)
      }
    val query = generate(ctx, withCte.query)
    tba"WITH ${ctes.mkTba(", ")} $query"
  }

  private def subQueryAlias(ctx: GeneratorContext, subQAlias: ir.SubqueryAlias): TBA[RemorphContext, String] = {
    val subquery = subQAlias.child match {
      case l: ir.Lateral => lateral(ctx, l)
      case _ => tba"(${generate(ctx, subQAlias.child)})"
    }
    val tableName = expr.generate(ctx, subQAlias.alias)
    val table =
      if (subQAlias.columnNames.isEmpty) {
        tba"AS $tableName"
      } else {
        // Added this to handle the case for POS Explode
        // We have added two columns index and value as an alias for pos explode default columns (pos, col)
        // these column will be added to the databricks query
        subQAlias.columnNames match {
          case Seq(ir.Id("value", _), ir.Id("index", _)) =>
            val columnNamesStr =
              subQAlias.columnNames.sortBy(_.nodeName).reverse.map(expr.generate(ctx, _))
            tba"$tableName AS ${columnNamesStr.mkTba(", ")}"
          case _ =>
            val columnNamesStr = subQAlias.columnNames.map(expr.generate(ctx, _))
            tba"AS $tableName${columnNamesStr.mkTba("(", ", ", ")")}"
        }
      }
    tba"$subquery $table"
  }

  private def tableAlias(ctx: GeneratorContext, alias: ir.TableAlias): TBA[RemorphContext, String] = {
    val target = generate(ctx, alias.child)
    val columns = if (alias.columns.isEmpty) { tba"" }
    else {
      alias.columns.map(expr.generate(ctx, _)).mkTba("(", ", ", ")")
    }
    tba"$target AS ${alias.alias}$columns"
  }

  private def deduplicate(ctx: GeneratorContext, dedup: ir.Deduplicate): TBA[RemorphContext, String] = {
    val table = generate(ctx, dedup.child)
    val columns = if (dedup.all_columns_as_keys) { tba"*" }
    else {
      dedup.column_names.map(expr.generate(ctx, _)).mkTba(", ")
    }
    tba"SELECT DISTINCT $columns FROM $table"
  }
}
