package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.parsers.intermediate.Batch
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

class LogicalPlanGenerator(val expr: ExpressionGenerator, val explicitDistinct: Boolean = false)
    extends Generator[ir.LogicalPlan, String] {

  override def generate(ctx: GeneratorContext, tree: ir.LogicalPlan): String = tree match {
    case b: ir.Batch => batch(ctx, b)
    case w: ir.WithCTE => cte(ctx, w)
    case p: ir.Project => project(ctx, p)
    case ir.NamedTable(id, _, _) => id
    case ir.Filter(input, condition) =>
      s"${generate(ctx, input)} WHERE ${expr.generate(ctx, condition)}"
    case ir.Limit(input, limit) =>
      s"${generate(ctx, input)} LIMIT ${expr.generate(ctx, limit)}"
    case ir.Offset(child, offset) =>
      s"${generate(ctx, child)} OFFSET ${expr.generate(ctx, offset)}"
    case ir.Values(data) =>
      s"VALUES ${data.map(_.map(expr.generate(ctx, _)).mkString("(", ",", ")")).mkString(", ")}"
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
    case ir.NoopNode => ""
    //  TODO We should always generate an unresolved node, our plan should never be null
    case null => "" // don't fail transpilation if the plan is null
    case x => throw unknown(x)
  }

  private def batch(ctx: GeneratorContext, b: Batch): String = {
    val seqSql = b.children
      .map {
        case ir.UnresolvedCommand(text) =>
          s"-- ${text.stripSuffix(";")}"
        case query => s"${generate(ctx, query)}"
      }
      .filter(_.nonEmpty)
    if (seqSql.nonEmpty) {
      seqSql.mkString("", ";\n", ";")
    } else {
      ""
    }
  }

  private def alterTable(ctx: GeneratorContext, a: ir.AlterTableCommand): String = {
    val operation = buildTableAlteration(ctx, a.alterations)
    s"ALTER TABLE  ${a.tableName} $operation"
  }

  private def buildTableAlteration(ctx: GeneratorContext, alterations: Seq[ir.TableAlteration]): String = {
    // docs:https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-alter-table.html#parameters
    // docs:https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-alter-table#syntax
    // ADD COLUMN can be Seq[ir.TableAlteration]
    // DROP COLUMN will be ir.TableAlteration since it stored the list of columns
    // DROP CONSTRAINTS BY NAME is ir.TableAlteration
    // RENAME COLUMN/ RENAME CONSTRAINTS Always be ir.TableAlteration
    // ALTER COLUMN IS A Seq[ir.TableAlternations] Data Type Change, Constraint Changes etc
    alterations map {
      case ir.AddColumn(columns) => s"ADD COLUMN ${buildAddColumn(ctx, columns)}"
      case ir.DropColumns(columns) => s"DROP COLUMN ${columns.mkString(", ")}"
      case ir.DropConstraintByName(constraints) => s"DROP CONSTRAINT ${constraints}"
      case ir.RenameColumn(oldName, newName) => s"RENAME COLUMN ${oldName} to ${newName}"
      case x => throw TranspileException(s"Unsupported table alteration ${x}")
    } mkString ", "
  }

  private def buildAddColumn(ctx: GeneratorContext, columns: Seq[ir.ColumnDeclaration]): String = {
    columns
      .map { c =>
        val dataType = DataTypeGenerator.generateDataType(ctx, c.dataType)
        val constraints = c.constraints.map(constraint(ctx, _)).mkString(" ")
        s"${c.name} $dataType $constraints"
      }
      .mkString(", ")
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-lateral-view.html
  private def lateral(ctx: GeneratorContext, lateral: ir.Lateral): String = lateral match {
    case ir.Lateral(ir.TableFunction(fn), isOuter) =>
      val outer = if (isOuter) " OUTER" else ""
      s"LATERAL VIEW$outer ${expr.generate(ctx, fn)}"
    case _ => throw unknown(lateral)
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-sampling.html
  private def tableSample(ctx: GeneratorContext, t: ir.TableSample): String = {
    val sampling = t.samplingMethod match {
      case ir.RowSamplingProbabilistic(probability) => s"$probability PERCENT"
      case ir.RowSamplingFixedAmount(amount) => s"$amount ROWS"
      case ir.BlockSampling(probability) => s"BUCKET $probability OUT OF 1"
    }
    val seed = t.seed.map(s => s" REPEATABLE ($s)").getOrElse("")
    s"(${generate(ctx, t.child)}) TABLESAMPLE ($sampling)$seed"
  }

  private def createTable(ctx: GeneratorContext, createTable: ir.CreateTableCommand): String = {
    val columns = createTable.columns
      .map { col =>
        val dataType = DataTypeGenerator.generateDataType(ctx, col.dataType)
        val constraints = col.constraints.map(constraint(ctx, _)).mkString(" ")
        s"${col.name} $dataType $constraints"
      }
      .mkString(", ")
    s"CREATE TABLE ${createTable.name} ($columns)"
  }

  private def constraint(ctx: GeneratorContext, c: ir.Constraint): String = c match {
    case ir.Unique => "UNIQUE"
    case ir.Nullability(nullable) => if (nullable) "NULL" else "NOT NULL"
    case ir.PrimaryKey => "PRIMARY KEY"
    case ir.ForeignKey(references) => s"FOREIGN KEY REFERENCES $references"
    case ir.NamedConstraint(name, unnamed) => s"CONSTRAINT $name ${constraint(ctx, unnamed)}"
    case ir.UnresolvedConstraint(inputText) => s"/** $inputText **/"
  }

  private def project(ctx: GeneratorContext, proj: ir.Project): String = {
    val fromClause = if (proj.input != ir.NoTable()) {
      s" FROM ${generate(ctx, proj.input)}"
    } else {
      ""
    }
    s"SELECT ${proj.expressions.map(expr.generate(ctx, _)).mkString(", ")}$fromClause"
  }

  private def orderBy(ctx: GeneratorContext, sort: ir.Sort): String = {
    val orderStr = sort.order
      .map { case ir.SortOrder(child, direction, nulls) =>
        val dir = direction match {
          case ir.Ascending => ""
          case ir.Descending => " DESC"
        }
        s"${expr.generate(ctx, child)}$dir ${nulls.sql}"
      }
      .mkString(", ")
    s"${generate(ctx, sort.child)} ORDER BY $orderStr"
  }

  private def generateJoin(ctx: GeneratorContext, join: ir.Join): String = {
    val left = generate(ctx, join.left)
    val right = generate(ctx, join.right)
    if (join.join_condition.isEmpty && join.using_columns.isEmpty && join.join_type == ir.InnerJoin) {
      if (join.right.find(_.isInstanceOf[ir.Lateral]).isDefined) {
        s"$left $right"
      } else {
        s"$left, $right"
      }
    } else {
      val joinType = generateJoinType(join.join_type)
      val joinClause = if (joinType.isEmpty) { "JOIN" }
      else { joinType + " JOIN" }
      val conditionOpt = join.join_condition.map(expr.generate(ctx, _))
      val condition = join.join_condition match {
        case None => ""
        case Some(_: ir.And) | Some(_: ir.Or) => s"ON (${conditionOpt.get})"
        case Some(_) => s"ON ${conditionOpt.get}"
      }
      val usingColumns = join.using_columns.mkString(", ")
      val using = if (usingColumns.isEmpty) "" else s"USING ($usingColumns)"
      Seq(left, joinClause, right, condition, using).filterNot(_.isEmpty).mkString(" ")
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

  private def setOperation(ctx: GeneratorContext, setOp: ir.SetOperation): String = {
    if (setOp.allow_missing_columns) {
      throw unknown(setOp)
    }
    if (setOp.by_name) {
      throw unknown(setOp)
    }
    val op = setOp.set_op_type match {
      case ir.UnionSetOp => "UNION"
      case ir.IntersectSetOp => "INTERSECT"
      case ir.ExceptSetOp => "EXCEPT"
      case _ => throw unknown(setOp)
    }
    val duplicates = if (setOp.is_all) " ALL" else if (explicitDistinct) " DISTINCT" else ""
    s"(${generate(ctx, setOp.left)}) $op$duplicates (${generate(ctx, setOp.right)})"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-insert-into.html
  private def insert(ctx: GeneratorContext, insert: ir.InsertIntoTable): String = {
    val target = generate(ctx, insert.target)
    val columns = insert.columns.map(_.map(expr.generate(ctx, _)).mkString("(", ", ", ")")).getOrElse("")
    val values = generate(ctx, insert.values)
    val output = insert.outputRelation.map(generate(ctx, _)).getOrElse("")
    val options = insert.options.map(expr.generate(ctx, _)).getOrElse("")
    val overwrite = if (insert.overwrite) "OVERWRITE TABLE" else "INTO"
    s"INSERT $overwrite $target $columns $values$output$options"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-update.html
  private def update(ctx: GeneratorContext, update: ir.UpdateTable): String = {
    val target = generate(ctx, update.target)
    val set = update.set.map(expr.generate(ctx, _)).mkString(", ")
    val where = update.where.map(cond => s" WHERE ${expr.generate(ctx, cond)}").getOrElse("")
    s"UPDATE $target SET $set$where"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-delete-from.html
  private def delete(ctx: GeneratorContext, target: ir.LogicalPlan, where: Option[ir.Expression]): String = {
    val whereStr = where.map(cond => s" WHERE ${expr.generate(ctx, cond)}").getOrElse("")
    s"DELETE FROM ${generate(ctx, target)}$whereStr"
  }

  // @see https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html
  private def merge(ctx: GeneratorContext, mergeIntoTable: ir.MergeIntoTable): String = {
    val target = generate(ctx, mergeIntoTable.targetTable)
    val source = generate(ctx, mergeIntoTable.sourceTable)
    val condition = expr.generate(ctx, mergeIntoTable.mergeCondition)
    val matchedActions = mergeIntoTable.matchedActions.map { action =>
      val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
      s" WHEN MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
    }.mkString
    val notMatchedActions = mergeIntoTable.notMatchedActions.map { action =>
      val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
      s" WHEN NOT MATCHED${conditionText} THEN ${expr.generate(ctx, action)}"
    }.mkString
    val notMatchedBySourceActions = mergeIntoTable.notMatchedBySourceActions.map { action =>
      val conditionText = action.condition.map(cond => s" AND ${expr.generate(ctx, cond)}").getOrElse("")
      s" WHEN NOT MATCHED BY SOURCE${conditionText} THEN ${expr.generate(ctx, action)}"
    }.mkString
    s"""MERGE INTO $target
       |USING $source
       |ON $condition
       |$matchedActions
       |$notMatchedActions
       |$notMatchedBySourceActions
       |""".stripMargin
  }

  private def aggregate(ctx: GeneratorContext, aggregate: ir.Aggregate): String = {
    val child = generate(ctx, aggregate.child)
    val expressions = aggregate.grouping_expressions.map(expr.generate(ctx, _)).mkString(", ")
    aggregate.group_type match {
      case ir.GroupBy =>
        s"$child GROUP BY $expressions"
      case ir.Pivot if aggregate.pivot.isDefined =>
        val pivot = aggregate.pivot.get
        val col = expr.generate(ctx, pivot.col)
        val values = pivot.values.map(expr.generate(ctx, _)).mkString(" IN(", ", ", ")")
        s"$child PIVOT($expressions FOR $col$values)"
      case a => throw TranspileException(s"Unsupported aggregate $a")
    }
  }
  private def generateWithOptions(ctx: GeneratorContext, withOptions: ir.WithOptions): String = {
    val optionComments = expr.generate(ctx, withOptions.options)
    val plan = generate(ctx, withOptions.input)
    s"${optionComments}" +
      s"${plan}"
  }

  private def cte(ctx: GeneratorContext, withCte: ir.WithCTE): String = {
    val ctes = withCte.ctes
      .map {
        case ir.SubqueryAlias(child, alias, cols) =>
          val columns = cols.map(expr.generate(ctx, _)).mkString("(", ", ", ")")
          val columnsStr = if (cols.isEmpty) "" else " " + columns
          val id = expr.generate(ctx, alias)
          val sub = generate(ctx, child)
          s"$id$columnsStr AS ($sub)"
        case x => generate(ctx, x)
      }
      .mkString(", ")
    val query = generate(ctx, withCte.query)
    s"WITH $ctes $query"
  }

  private def subQueryAlias(ctx: GeneratorContext, subQAlias: ir.SubqueryAlias): String = {
    val subquery = subQAlias.child match {
      case l: ir.Lateral => lateral(ctx, l)
      case _ => s"(${generate(ctx, subQAlias.child)})"
    }
    val tableName = expr.generate(ctx, subQAlias.alias)
    val table = if (subQAlias.columnNames.isEmpty) {
      tableName
    } else {
      tableName + subQAlias.columnNames.map(expr.generate(ctx, _)).mkString("(", ", ", ")")
    }
    s"$subquery AS $table"
  }

  private def tableAlias(ctx: GeneratorContext, alias: ir.TableAlias): String = {
    val target = generate(ctx, alias.child)
    val columns = if (alias.columns.isEmpty) { "" }
    else {
      alias.columns.map(expr.generate(ctx, _)).mkString("(", ", ", ")")
    }
    s"$target AS ${alias.alias}$columns"
  }

  private def deduplicate(ctx: GeneratorContext, dedup: ir.Deduplicate): String = {
    val table = generate(ctx, dedup.child)
    val columns = if (dedup.all_columns_as_keys) { "*" }
    else {
      dedup.column_names.map(expr.generate(ctx, _)).mkString(", ")
    }
    s"SELECT DISTINCT $columns FROM $table"
  }
}
