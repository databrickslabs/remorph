package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, Phase, Transformation, TransformationConstructors, intermediate => ir}

class LogicalPlanGenerator(
    val expr: ExpressionGenerator,
    val optGen: OptionGenerator,
    val explicitDistinct: Boolean = false)
    extends BaseSQLGenerator[ir.LogicalPlan]
    with TransformationConstructors[Phase] {

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): Transformation[Phase, String] = {

    val sql: Transformation[Phase, String] = tree match {
      case b: ir.Batch => batch(ctx, b)
      case w: ir.WithCTE => cte(ctx, w)
      case p: ir.Project => project(ctx, p)
      case ir.NamedTable(id, _, _) => lift(OkResult(id))
      case ir.Filter(input, condition) =>
        code"${generate(ctx, input)} WHERE ${expr.generate(ctx, condition)}"
      case ir.Limit(input, limit) =>
        code"${generate(ctx, input)} LIMIT ${expr.generate(ctx, limit)}"
      case ir.Offset(child, offset) =>
        code"${generate(ctx, child)} OFFSET ${expr.generate(ctx, offset)}"
      case ir.Values(data) =>
        code"VALUES ${data.map(_.map(expr.generate(ctx, _)).mkCode("(", ",", ")")).mkCode(", ")}"
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
      case ir.NoopNode => code""

      case null => code"" // don't fail transpilation if the plan is null
      case x => partialResult(x)
    }

    update { case g: Generating =>
      g.copy(currentNode = tree)
    }.flatMap(_ => sql)
  }

  private def batch(ctx: GeneratorContext, b: ir.Batch): Transformation[Phase, String] = {
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

  private def createTableParams(ctx: GeneratorContext, crp: ir.CreateTableParams): Transformation[Phase, String] = {

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
              .mkCode(", ")
        }

        // We now generate any table level constraints
        val tableConstraintStr = crp.constraints.map(constraint(ctx, _)).mkCode(", ")
        val tableConstraintStrWithComma =
          tableConstraintStr.nonEmpty.flatMap(nonEmpty => if (nonEmpty) code", $tableConstraintStr" else code"")

        // record any table level options
        val tableOptions = crp.options.map(_.map(optGen.generateOption(ctx, _)).mkCode("\n   ")).getOrElse(code"")

        val tableOptionsComment = {
          tableOptions.isEmpty.flatMap { isEmpty =>
            if (isEmpty) code"" else code"   The following options are unsupported:\n\n   $tableOptions\n"
          }
        }
        val indicesStr = crp.indices.map(constraint(ctx, _)).mkCode("   \n")
        val indicesComment =
          indicesStr.isEmpty.flatMap { isEmpty =>
            if (isEmpty) code""
            else code"   The following index directives are unsupported:\n\n   $indicesStr*/\n"
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

        code"${leadingComment}CREATE TABLE ${ct.table_name} (${columns}${tableConstraintStrWithComma})"

      case ctas: ir.CreateTableAsSelect => code"CREATE TABLE ${ctas.table_name} AS ${generate(ctx, ctas.query)}"
    }
  }

  private def genColumnDecl(
      ctx: GeneratorContext,
      col: ir.StructField,
      constraints: Seq[ir.Constraint],
      options: Seq[ir.GenericOption]): Transformation[Phase, String] = {
    val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
    val dataTypeStr = if (!col.nullable) code"$dataType NOT NULL" else dataType
    val constraintsStr = constraints.map(constraint(ctx, _)).mkCode(" ")
    val constraintsGen = constraintsStr.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) code" $constraintsStr" else code""
    }
    val optionsStr = options.map(optGen.generateOption(ctx, _)).mkCode(" ")
    val optionsComment = optionsStr.nonEmpty.flatMap { nonEmpty => if (nonEmpty) code" /* $optionsStr */" else code"" }
    code"${col.name} ${dataTypeStr}${constraintsGen}${optionsComment}"
  }

  private def alterTable(ctx: GeneratorContext, a: ir.AlterTableCommand): Transformation[Phase, String] = {
    val operation = buildTableAlteration(ctx, a.alterations)
    code"ALTER TABLE  ${a.tableName} $operation"
  }

  private def buildTableAlteration(
      ctx: GeneratorContext,
      alterations: Seq[ir.TableAlteration]): Transformation[Phase, String] = {
    // docs:https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table.html#parameters
    // docs:https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table#syntax
    // ADD COLUMN can be Seq[ir.TableAlteration]
    // DROP COLUMN will be ir.TableAlteration since it stored the list of columns
    // DROP CONSTRAINTS BY NAME is ir.TableAlteration
    // RENAME COLUMN/ RENAME CONSTRAINTS Always be ir.TableAlteration
    // ALTER COLUMN IS A Seq[ir.TableAlternations] Data Type Change, Constraint Changes etc
    alterations map {
      case ir.AddColumn(columns) => code"ADD COLUMN ${buildAddColumn(ctx, columns)}"
      case ir.DropColumns(columns) => code"DROP COLUMN ${columns.mkString(", ")}"
      case ir.DropConstraintByName(constraints) => code"DROP CONSTRAINT ${constraints}"
      case ir.RenameColumn(oldName, newName) => code"RENAME COLUMN ${oldName} to ${newName}"
      case x => partialResult(x, ir.UnexpectedTableAlteration(x.toString))
    } mkCode ", "
  }

  private def buildAddColumn(
      ctx: GeneratorContext,
      columns: Seq[ir.ColumnDeclaration]): Transformation[Phase, String] = {
    columns
      .map { c =>
        val dataType = DataTypeGenerator.generateDataType(ctx, c.dataType)
        val constraints = c.constraints.map(constraint(ctx, _)).mkCode(" ")
        code"${c.name} $dataType $constraints"
      }
      .mkCode(", ")
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view.html
  private def lateral(ctx: GeneratorContext, lateral: ir.Lateral): Transformation[Phase, String] =
    lateral match {
      case ir.Lateral(ir.TableFunction(fn), isOuter, isView) =>
        val outer = if (isOuter) " OUTER" else ""
        val view = if (isView) " VIEW" else ""
        code"LATERAL$view$outer ${expr.generate(ctx, fn)}"
      case _ => partialResult(lateral)
    }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-sampling.html
  private def tableSample(ctx: GeneratorContext, t: ir.TableSample): Transformation[Phase, String] = {
    val sampling = t.samplingMethod match {
      case ir.RowSamplingProbabilistic(probability) => s"$probability PERCENT"
      case ir.RowSamplingFixedAmount(amount) => s"$amount ROWS"
      case ir.BlockSampling(probability) => s"BUCKET $probability OUT OF 1"
    }
    val seed = t.seed.map(s => s" REPEATABLE ($s)").getOrElse("")
    code"(${generate(ctx, t.child)}) TABLESAMPLE ($sampling)$seed"
  }

  private def createTable(ctx: GeneratorContext, createTable: ir.CreateTableCommand): Transformation[Phase, String] = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
        val constraints = col.constraints.map(constraint(ctx, _)).mkCode(" ")
        code"${col.name} $dataType $constraints"
      }
    code"CREATE TABLE ${createTable.name} (${columns.mkCode(", ")})"
  }

  private def constraint(ctx: GeneratorContext, c: ir.Constraint): Transformation[Phase, String] = c match {
    case unique: ir.Unique => generateUniqueConstraint(ctx, unique)
    case ir.Nullability(nullable) => lift(OkResult(if (nullable) "NULL" else "NOT NULL"))
    case pk: ir.PrimaryKey => generatePrimaryKey(ctx, pk)
    case fk: ir.ForeignKey => generateForeignKey(ctx, fk)
    case ir.NamedConstraint(name, unnamed) => code"CONSTRAINT $name ${constraint(ctx, unnamed)}"
    case ir.UnresolvedConstraint(inputText) => code"/** $inputText **/"
    case ir.CheckConstraint(e) => code"CHECK (${expr.generate(ctx, e)})"
    case ir.DefaultValueConstraint(value) => code"DEFAULT ${expr.generate(ctx, value)}"
    case ir.IdentityConstraint(seed, step) => code"IDENTITY ($seed, $step)"
  }

  private def generateForeignKey(ctx: GeneratorContext, fk: ir.ForeignKey): Transformation[Phase, String] = {
    val colNames = fk.tableCols match {
      case "" => ""
      case cols => s"(${cols}) "
    }
    val commentOptions = optGen.generateOptionList(ctx, fk.options) match {
      case "" => ""
      case options => s" /* Unsupported:  $options */"
    }
    code"FOREIGN KEY ${colNames}REFERENCES ${fk.refObject}(${fk.refCols})$commentOptions"
  }

  private def generatePrimaryKey(context: GeneratorContext, key: ir.PrimaryKey): Transformation[Phase, String] = {
    val columns = key.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val commentOptions = optGen.generateOptionList(context, key.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    val columnsStr = if (columns.isEmpty) "" else s" $columns"
    code"PRIMARY KEY${columnsStr}${commentOptions}"
  }

  private def generateUniqueConstraint(ctx: GeneratorContext, unique: ir.Unique): Transformation[Phase, String] = {
    val columns = unique.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val columnStr = if (columns.isEmpty) "" else s" $columns"
    val commentOptions = optGen.generateOptionList(ctx, unique.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    code"UNIQUE${columnStr}${commentOptions}"
  }

  private def project(ctx: GeneratorContext, proj: ir.Project): Transformation[Phase, String] = {
    val fromClause = if (proj.input != ir.NoTable()) {
      code" FROM ${generate(ctx, proj.input)}"
    } else {
      code""
    }

    // Don't put commas after unresolved expressions as they are error comments only
    val sqlParts = proj.expressions
      .map {
        case u: ir.Unresolved[_] => expr.generate(ctx, u)
        case exp: ir.Expression => expr.generate(ctx, exp).map(_ + ", ")
      }
      .sequence
      .map(_.mkString.stripSuffix(", "))

    code"SELECT $sqlParts$fromClause"
  }

  private def orderBy(ctx: GeneratorContext, sort: ir.Sort): Transformation[Phase, String] = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        val dir = direction match {
          case ir.Ascending => ""
          case ir.Descending => " DESC"
        }
        code"${expr.generate(ctx, child)}$dir ${nulls.sql}"
      }

    code"${generate(ctx, sort.child)} ORDER BY ${orderStr.mkCode(", ")}"
  }

  private def isLateralView(lp: ir.LogicalPlan): Boolean = {
    lp.find {
      case ir.Lateral(_, _, isView) => isView
      case _ => false
    }.isDefined
  }

  private def generateJoin(ctx: GeneratorContext, join: ir.Join): Transformation[Phase, String] = {
    val left = generate(ctx, join.left)
    val right = generate(ctx, join.right)
    if (join.join_condition.isEmpty && join.using_columns.isEmpty && join.join_type == ir.InnerJoin) {
      if (isLateralView(join.right)) {
        code"$left $right"
      } else {
        code"$left, $right"
      }
    } else {
      val joinType = generateJoinType(join.join_type)
      val joinClause = if (joinType.isEmpty) { "JOIN" }
      else { joinType + " JOIN" }
      val conditionOpt = join.join_condition.map(expr.generate(ctx, _))
      val condition = join.join_condition match {
        case None => code""
        case Some(_: ir.And) | Some(_: ir.Or) => code"ON (${conditionOpt.get})"
        case Some(_) => code"ON ${conditionOpt.get}"
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

  private def setOperation(ctx: GeneratorContext, setOp: ir.SetOperation): Transformation[Phase, String] = {
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
    code"(${generate(ctx, setOp.left)}) $op$duplicates (${generate(ctx, setOp.right)})"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-insert-into.html
  private def insert(ctx: GeneratorContext, insert: ir.InsertIntoTable): Transformation[Phase, String] = {
    val target = generate(ctx, insert.target)
    val columns =
      insert.columns.map(cols => cols.map(expr.generate(ctx, _)).mkCode("(", ", ", ")")).getOrElse(code"")
    val values = generate(ctx, insert.values)
    val output = insert.outputRelation.map(generate(ctx, _)).getOrElse(code"")
    val options = insert.options.map(expr.generate(ctx, _)).getOrElse(code"")
    val overwrite = if (insert.overwrite) "OVERWRITE TABLE" else "INTO"
    code"INSERT $overwrite $target $columns $values$output$options"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-update.html
  private def update(ctx: GeneratorContext, update: ir.UpdateTable): Transformation[Phase, String] = {
    val target = generate(ctx, update.target)
    val set = expr.commas(ctx, update.set)
    val where = update.where.map(cond => code" WHERE ${expr.generate(ctx, cond)}").getOrElse("")
    code"UPDATE $target SET $set$where"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-delete-from.html
  private def delete(
      ctx: GeneratorContext,
      target: ir.LogicalPlan,
      where: Option[ir.Expression]): Transformation[Phase, String] = {
    val whereStr = where.map(cond => code" WHERE ${expr.generate(ctx, cond)}").getOrElse(code"")
    code"DELETE FROM ${generate(ctx, target)}$whereStr"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html
  private def merge(ctx: GeneratorContext, mergeIntoTable: ir.MergeIntoTable): Transformation[Phase, String] = {
    val target = generate(ctx, mergeIntoTable.targetTable)
    val source = generate(ctx, mergeIntoTable.sourceTable)
    val condition = expr.generate(ctx, mergeIntoTable.mergeCondition)
    val matchedActions =
      mergeIntoTable.matchedActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(ctx, cond)}").getOrElse(code"")
        code" WHEN MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkCode

    val notMatchedActions =
      mergeIntoTable.notMatchedActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(ctx, cond)}").getOrElse(code"")
        code" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkCode
    val notMatchedBySourceActions =
      mergeIntoTable.notMatchedBySourceActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(ctx, cond)}").getOrElse(code"")
        code" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(ctx, action)}"
      }.mkCode
    code"""MERGE INTO $target
       |USING $source
       |ON $condition
       |$matchedActions
       |$notMatchedActions
       |$notMatchedBySourceActions
       |""".map(_.stripMargin)
  }

  private def aggregate(ctx: GeneratorContext, aggregate: ir.Aggregate): Transformation[Phase, String] = {
    val child = generate(ctx, aggregate.child)
    val expressions = expr.commas(ctx, aggregate.grouping_expressions)
    aggregate.group_type match {
      case ir.GroupBy =>
        code"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(ctx, pivot.col)
        val values = pivot.values.map(expr.generate(ctx, _)).mkCode(" IN(", ", ", ")")
        code"$child PIVOT($expressions FOR $col$values)"
      case a => partialResult(a, ir.UnsupportedGroupType(a.toString))
    }
  }
  private def generateWithOptions(ctx: GeneratorContext, withOptions: ir.WithOptions): Transformation[Phase, String] = {
    val optionComments = expr.generate(ctx, withOptions.options)
    val plan = generate(ctx, withOptions.input)
    code"${optionComments}${plan}"
  }

  private def cte(ctx: GeneratorContext, withCte: ir.WithCTE): Transformation[Phase, String] = {
    val ctes = withCte.ctes
      .map {
        case ir.SubqueryAlias(child, alias, cols) =>
          val columns = cols.map(expr.generate(ctx, _)).mkCode("(", ", ", ")")
          val columnsStr = if (cols.isEmpty) code"" else code" $columns"
          val id = expr.generate(ctx, alias)
          val sub = generate(ctx, child)
          code"$id$columnsStr AS ($sub)"
        case x => generate(ctx, x)
      }
    val query = generate(ctx, withCte.query)
    code"WITH ${ctes.mkCode(", ")} $query"
  }

  private def subQueryAlias(ctx: GeneratorContext, subQAlias: ir.SubqueryAlias): Transformation[Phase, String] = {
    val subquery = subQAlias.child match {
      case l: ir.Lateral => lateral(ctx, l)
      case _ => code"(${generate(ctx, subQAlias.child)})"
    }
    val tableName = expr.generate(ctx, subQAlias.alias)
    val table =
      if (subQAlias.columnNames.isEmpty) {
        code"AS $tableName"
      } else {
        // Added this to handle the case for POS Explode
        // We have added two columns index and value as an alias for pos explode default columns (pos, col)
        // these column will be added to the databricks query
        subQAlias.columnNames match {
          case Seq(ir.Id("value", _), ir.Id("index", _)) =>
            val columnNamesStr =
              subQAlias.columnNames.sortBy(_.nodeName).reverse.map(expr.generate(ctx, _))
            code"$tableName AS ${columnNamesStr.mkCode(", ")}"
          case _ =>
            val columnNamesStr = subQAlias.columnNames.map(expr.generate(ctx, _))
            code"AS $tableName${columnNamesStr.mkCode("(", ", ", ")")}"
        }
      }
    code"$subquery $table"
  }

  private def tableAlias(ctx: GeneratorContext, alias: ir.TableAlias): Transformation[Phase, String] = {
    val target = generate(ctx, alias.child)
    val columns = if (alias.columns.isEmpty) { code"" }
    else {
      expr.commas(ctx, alias.columns).map("(" + _ + ")")
    }
    code"$target AS ${alias.alias}$columns"
  }

  private def deduplicate(ctx: GeneratorContext, dedup: ir.Deduplicate): Transformation[Phase, String] = {
    val table = generate(ctx, dedup.child)
    val columns = if (dedup.all_columns_as_keys) { code"*" }
    else {
      expr.commas(ctx, dedup.column_names)
    }
    code"SELECT DISTINCT $columns FROM $table"
  }
}
