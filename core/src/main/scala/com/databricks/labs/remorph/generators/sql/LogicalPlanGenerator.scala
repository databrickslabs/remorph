package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, TransformationConstructors, intermediate => ir}

class LogicalPlanGenerator(
    val expr: ExpressionGenerator,
    val optGen: OptionGenerator,
    val explicitDistinct: Boolean = false)
    extends BaseSQLGenerator[ir.LogicalPlan]
    with TransformationConstructors {

  override def generate(tree: ir.LogicalPlan): SQL = {

    val sql: SQL = tree match {
      case b: ir.Batch => batch(b)
      case w: ir.WithCTE => cte(w)
      case p: ir.Project => project(p)
      case ir.NamedTable(id, _, _) => lift(OkResult(id))
      case ir.Filter(input, condition) => {
        val source = input match {
          // enclose subquery in parenthesis
          case project: ir.Project => code"(${generate(project)})"
          case _ => code"${generate(input)}"
        }
        code"${source} WHERE ${expr.generate(condition)}"
      }
      case ir.Limit(input, limit) =>
        code"${generate(input)} LIMIT ${expr.generate(limit)}"
      case ir.Offset(child, offset) =>
        code"${generate(child)} OFFSET ${expr.generate(offset)}"
      case ir.Values(data) =>
        code"VALUES ${data.map(_.map(expr.generate(_)).mkCode("(", ",", ")")).mkCode(", ")}"
      case ir.PlanComment(child, text) => code"/* $text */\n${generate(child)}"
      case agg: ir.Aggregate => aggregate(agg)
      case sort: ir.Sort => orderBy(sort)
      case join: ir.Join => generateJoin(join)
      case setOp: ir.SetOperation => setOperation(setOp)
      case mergeIntoTable: ir.MergeIntoTable => merge(mergeIntoTable)
      case withOptions: ir.WithOptions => generateWithOptions(withOptions)
      case s: ir.SubqueryAlias => subQueryAlias(s)
      case t: ir.TableAlias => tableAlias(t)
      case d: ir.Deduplicate => deduplicate(d)
      case u: ir.UpdateTable => updateTable(u)
      case i: ir.InsertIntoTable => insert(i)
      case ir.DeleteFromTable(target, None, where, None, None) => delete(target, where)
      case c: ir.CreateTableCommand => createTable(c)
      case rt: ir.ReplaceTableCommand => replaceTable(rt)
      case t: ir.TableSample => tableSample(t)
      case a: ir.AlterTableCommand => alterTable(a)
      case l: ir.Lateral => lateral(l)
      case c: ir.CreateTableParams => createTableParams(c)
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

  private def batch(b: ir.Batch): SQL = {
    val seqSql = b.children.map(generate(_)).sequence
    seqSql.map { seq =>
      seq
        .map { elem =>
          if (!elem.endsWith("*/")) s"$elem;"
          else elem
        }
        .mkString("\n")
    }
  }

  private def createTableParams(crp: ir.CreateTableParams): SQL = {

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
                genColumnDecl(col, constraints, options)
              }
              .mkCode(", ")
        }

        // We now generate any table level constraints
        val tableConstraintStr = crp.constraints.map(constraint).mkCode(", ")
        val tableConstraintStrWithComma =
          tableConstraintStr.nonEmpty.flatMap(nonEmpty => if (nonEmpty) code", $tableConstraintStr" else code"")

        // record any table level options
        val tableOptions = crp.options.map(_.map(optGen.generateOption).mkCode("\n   ")).getOrElse(code"")

        val tableOptionsComment = {
          tableOptions.isEmpty.flatMap { isEmpty =>
            if (isEmpty) code"" else code"   The following options are unsupported:\n\n   $tableOptions\n"
          }
        }
        val indicesStr = crp.indices.map(constraint).mkCode("   \n")
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

      case ctas: ir.CreateTableAsSelect => code"CREATE TABLE ${ctas.table_name} AS ${generate(ctas.query)}"
      case rtas: ir.ReplaceTableAsSelect =>
        code"CREATE OR REPLACE TABLE ${rtas.table_name} AS ${generate(rtas.query)}"
    }
  }

  private def genColumnDecl(
      col: ir.StructField,
      constraints: Seq[ir.Constraint],
      options: Seq[ir.GenericOption]): SQL = {
    val dataType = DataTypeGenerator.generateDataType(col.dataType)
    val dataTypeStr = if (!col.nullable) code"$dataType NOT NULL" else dataType
    val constraintsStr = constraints.map(constraint(_)).mkCode(" ")
    val constraintsGen = constraintsStr.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) code" $constraintsStr" else code""
    }
    val optionsStr = options.map(optGen.generateOption(_)).mkCode(" ")
    val optionsComment = optionsStr.nonEmpty.flatMap { nonEmpty => if (nonEmpty) code" /* $optionsStr */" else code"" }
    code"${col.name} ${dataTypeStr}${constraintsGen}${optionsComment}"
  }

  private def alterTable(a: ir.AlterTableCommand): SQL = {
    val operation = buildTableAlteration(a.alterations)
    code"ALTER TABLE  ${a.tableName} $operation"
  }

  private def buildTableAlteration(alterations: Seq[ir.TableAlteration]): SQL = {
    // docs:https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table.html#parameters
    // docs:https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table#syntax
    // ADD COLUMN can be Seq[ir.TableAlteration]
    // DROP COLUMN will be ir.TableAlteration since it stored the list of columns
    // DROP CONSTRAINTS BY NAME is ir.TableAlteration
    // RENAME COLUMN/ RENAME CONSTRAINTS Always be ir.TableAlteration
    // ALTER COLUMN IS A Seq[ir.TableAlternations] Data Type Change, Constraint Changes etc
    alterations map {
      case ir.AddColumn(columns) => code"ADD COLUMN ${buildAddColumn(columns)}"
      case ir.DropColumns(columns) => code"DROP COLUMN ${columns.mkString(", ")}"
      case ir.DropConstraintByName(constraints) => code"DROP CONSTRAINT ${constraints}"
      case ir.RenameColumn(oldName, newName) => code"RENAME COLUMN ${oldName} to ${newName}"
      case x => partialResult(x, ir.UnexpectedTableAlteration(x.toString))
    } mkCode ", "
  }

  private def buildAddColumn(columns: Seq[ir.ColumnDeclaration]): SQL = {
    columns
      .map { c =>
        val dataType = DataTypeGenerator.generateDataType(c.dataType)
        val constraints = c.constraints.map(constraint(_)).mkCode(" ")
        code"${c.name} $dataType $constraints"
      }
      .mkCode(", ")
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view.html
  private def lateral(lateral: ir.Lateral): SQL =
    lateral match {
      case ir.Lateral(ir.TableFunction(fn), isOuter, isView) =>
        val outer = if (isOuter) " OUTER" else ""
        val view = if (isView) " VIEW" else ""
        code"LATERAL$view$outer ${expr.generate(fn)}"
      case _ => partialResult(lateral)
    }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-sampling.html
  private def tableSample(t: ir.TableSample): SQL = {
    val sampling = t.samplingMethod match {
      case ir.RowSamplingProbabilistic(probability) => s"$probability PERCENT"
      case ir.RowSamplingFixedAmount(amount) => s"$amount ROWS"
      case ir.BlockSampling(probability) => s"BUCKET $probability OUT OF 1"
    }
    val seed = t.seed.map(s => s" REPEATABLE ($s)").getOrElse("")
    code"(${generate(t.child)}) TABLESAMPLE ($sampling)$seed"
  }

  private def createTable(createTable: ir.CreateTableCommand): SQL = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(col.dataType)
        val constraints = col.constraints.map(constraint(_)).mkCode(" ")
        code"${col.name} $dataType $constraints"
      }
    code"CREATE TABLE ${createTable.name} (${columns.mkCode(", ")})"
  }

  private def replaceTable(createTable: ir.ReplaceTableCommand): SQL = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(col.dataType)
        val constraints = col.constraints.map(constraint).mkCode(" ")
        code"${col.name} $dataType $constraints"
      }
    code"CREATE OR REPLACE TABLE ${createTable.name} (${columns.mkCode(", ")})"
  }

  private def constraint(c: ir.Constraint): SQL = c match {
    case unique: ir.Unique => generateUniqueConstraint(unique)
    case ir.Nullability(nullable) => lift(OkResult(if (nullable) "NULL" else "NOT NULL"))
    case pk: ir.PrimaryKey => generatePrimaryKey(pk)
    case fk: ir.ForeignKey => generateForeignKey(fk)
    case ir.NamedConstraint(name, unnamed) => code"CONSTRAINT $name ${constraint(unnamed)}"
    case ir.UnresolvedConstraint(inputText) => code"/** $inputText **/"
    case ir.CheckConstraint(e) => code"CHECK (${expr.generate(e)})"
    case ir.DefaultValueConstraint(value) => code"DEFAULT ${expr.generate(value)}"
    case identity: ir.IdentityConstraint => generateIdentityConstraint(identity)
    case ir.GeneratedAlways(expression) => code"GENERATED ALWAYS AS (${expr.generate(expression)})"
  }

  private def generateIdentityConstraint(c: ir.IdentityConstraint): SQL = c match {
    case ir.IdentityConstraint(None, None, true, false) => code"GENERATED ALWAYS AS IDENTITY"
    case ir.IdentityConstraint(None, None, false, true) => code"GENERATED BY DEFAULT AS IDENTITY"
    case ir.IdentityConstraint(Some(seed), Some(step), false, true) =>
      code"GENERATED BY DEFAULT AS IDENTITY (START WITH $seed INCREMENT BY $step)"
    case ir.IdentityConstraint(Some(seed), None, false, true) =>
      code"GENERATED BY DEFAULT AS IDENTITY (START WITH $seed)"
    case ir.IdentityConstraint(None, Some(step), false, true) =>
      code"GENERATED BY DEFAULT AS IDENTITY (INCREMENT BY $step)"
    // IdentityConstraint(None, None, true, true) This is an incorrect representation parser should not generate this
    // for IdentityConstraint(None, None, false, false) we will generate empty
    case _ => code""

  }

  private def generateForeignKey(fk: ir.ForeignKey): SQL = {
    val colNames = fk.tableCols match {
      case "" => ""
      case cols => s"(${cols}) "
    }
    val commentOptions = optGen.generateOptionList(fk.options) match {
      case "" => ""
      case options => s" /* Unsupported:  $options */"
    }
    code"FOREIGN KEY ${colNames}REFERENCES ${fk.refObject}(${fk.refCols})$commentOptions"
  }

  private def generatePrimaryKey(key: ir.PrimaryKey): SQL = {
    val columns = key.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val commentOptions = optGen.generateOptionList(key.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    val columnsStr = if (columns.isEmpty) "" else s" $columns"
    code"PRIMARY KEY${columnsStr}${commentOptions}"
  }

  private def generateUniqueConstraint(unique: ir.Unique): SQL = {
    val columns = unique.columns.map(_.mkString("(", ", ", ")")).getOrElse("")
    val columnStr = if (columns.isEmpty) "" else s" $columns"
    val commentOptions = optGen.generateOptionList(unique.options) match {
      case "" => ""
      case options => s" /* $options */"
    }
    code"UNIQUE${columnStr}${commentOptions}"
  }

  private def project(proj: ir.Project): SQL = {
    val fromClause = if (proj.input != ir.NoTable) {
      code" FROM ${generate(proj.input)}"
    } else {
      code""
    }

    // Don't put commas after unresolved expressions as they are error comments only
    val sqlParts = proj.expressions
      .map {
        case u: ir.Unresolved[_] => expr.generate(u)
        case exp: ir.Expression => expr.generate(exp).map(_ + ", ")
      }
      .sequence
      .map(_.mkString.stripSuffix(", "))

    code"SELECT $sqlParts$fromClause"
  }

  private def orderBy(sort: ir.Sort): SQL = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        val dir = direction match {
          case ir.Ascending => ""
          case ir.Descending => " DESC"
        }
        code"${expr.generate(child)}$dir ${nulls.sql}"
      }

    code"${generate(sort.child)} ORDER BY ${orderStr.mkCode(", ")}"
  }

  private def isLateralView(lp: ir.LogicalPlan): Boolean = {
    lp.find {
      case ir.Lateral(_, _, isView) => isView
      case _ => false
    }.isDefined
  }

  private def generateJoin(join: ir.Join): SQL = {
    val left = generate(join.left)
    val right = generate(join.right)
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
      val conditionOpt = join.join_condition.map(expr.generate(_))
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

  private def setOperation(setOp: ir.SetOperation): SQL = {
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
    code"(${generate(setOp.left)}) $op$duplicates (${generate(setOp.right)})"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-insert-into.html
  private def insert(insert: ir.InsertIntoTable): SQL = {
    val target = generate(insert.target)
    val columns =
      insert.columns.map(cols => cols.map(expr.generate(_)).mkCode("(", ", ", ")")).getOrElse(code"")
    val values = generate(insert.values)
    val output = insert.outputRelation.map(generate(_)).getOrElse(code"")
    val options = insert.options.map(expr.generate(_)).getOrElse(code"")
    val overwrite = if (insert.overwrite) "OVERWRITE TABLE" else "INTO"
    code"INSERT $overwrite $target $columns $values$output$options"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-update.html
  private def updateTable(update: ir.UpdateTable): SQL = {
    val target = generate(update.target)
    val set = expr.commas(update.set)
    val where = update.where.map(cond => code" WHERE ${expr.generate(cond)}").getOrElse("")
    code"UPDATE $target SET $set$where"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-delete-from.html
  private def delete(target: ir.LogicalPlan, where: Option[ir.Expression]): SQL = {
    val whereStr = where.map(cond => code" WHERE ${expr.generate(cond)}").getOrElse(code"")
    code"DELETE FROM ${generate(target)}$whereStr"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html
  private def merge(mergeIntoTable: ir.MergeIntoTable): SQL = {
    val target = generate(mergeIntoTable.targetTable)
    val source = generate(mergeIntoTable.sourceTable)
    val condition = expr.generate(mergeIntoTable.mergeCondition)
    val matchedActions =
      mergeIntoTable.matchedActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(cond)}").getOrElse(code"")
        code" WHEN MATCHED${conditionText} THEN ${expr.generate(action)}"
      }.mkCode

    val notMatchedActions =
      mergeIntoTable.notMatchedActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(cond)}").getOrElse(code"")
        code" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(action)}"
      }.mkCode
    val notMatchedBySourceActions =
      mergeIntoTable.notMatchedBySourceActions.map { action =>
        val conditionText = action.condition.map(cond => code" AND ${expr.generate(cond)}").getOrElse(code"")
        code" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(action)}"
      }.mkCode
    code"""MERGE INTO $target
       |USING $source
       |ON $condition
       |$matchedActions
       |$notMatchedActions
       |$notMatchedBySourceActions
       |""".map(_.stripMargin)
  }

  private def aggregate(aggregate: ir.Aggregate): SQL = {
    val child = generate(aggregate.child)
    val expressions = expr.commas(aggregate.grouping_expressions)
    aggregate.group_type match {
      case ir.GroupByAll => code"$child GROUP BY ALL"
      case ir.GroupBy =>
        code"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(pivot.col)
        val values = pivot.values.map(expr.generate).mkCode(" IN(", ", ", ")")
        code"$child PIVOT($expressions FOR $col$values)"
      case a => partialResult(a, ir.UnsupportedGroupType(a.toString))
    }
  }
  private def generateWithOptions(withOptions: ir.WithOptions): SQL = {
    val optionComments = expr.generate(withOptions.options)
    val plan = generate(withOptions.input)
    code"${optionComments}${plan}"
  }

  private def cte(withCte: ir.WithCTE): SQL = {
    val ctes = withCte.ctes
      .map {
        case ir.SubqueryAlias(child, alias, cols) =>
          val columns = cols.map(expr.generate(_)).mkCode("(", ", ", ")")
          val columnsStr = if (cols.isEmpty) code"" else code" $columns"
          val id = expr.generate(alias)
          val sub = generate(child)
          code"$id$columnsStr AS ($sub)"
        case x => generate(x)
      }
    val query = generate(withCte.query)
    code"WITH ${ctes.mkCode(", ")} $query"
  }

  private def subQueryAlias(subQAlias: ir.SubqueryAlias): SQL = {
    val subquery = subQAlias.child match {
      case l: ir.Lateral => lateral(l)
      case _ => code"(${generate(subQAlias.child)})"
    }
    val tableName = expr.generate(subQAlias.alias)
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
              subQAlias.columnNames.sortBy(_.nodeName).reverse.map(expr.generate(_))
            code"$tableName AS ${columnNamesStr.mkCode(", ")}"
          case _ =>
            val columnNamesStr = subQAlias.columnNames.map(expr.generate(_))
            code"AS $tableName${columnNamesStr.mkCode("(", ", ", ")")}"
        }
      }
    code"$subquery $table"
  }

  private def tableAlias(alias: ir.TableAlias): SQL = {
    val target = generate(alias.child)
    val columns = if (alias.columns.isEmpty) { code"" }
    else {
      expr.commas(alias.columns).map("(" + _ + ")")
    }
    code"$target AS ${alias.alias}$columns"
  }

  private def deduplicate(dedup: ir.Deduplicate): SQL = {
    val table = generate(dedup.child)
    val columns = if (dedup.all_columns_as_keys) { code"*" }
    else {
      expr.commas(dedup.column_names)
    }
    code"SELECT DISTINCT $columns FROM $table"
  }
}
