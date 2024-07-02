package com.databricks.labs.remorph.generators.pygen

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.intermediate.{Filter, Plan, Project, SubqueryAlias}

import scala.util.matching.Regex

object PythonGenerator {
  private val pattern: Regex = "((?<![\\\\])['])".r

  def fromPlan(ctx: GeneratorContext, plan: Plan): String = plan match {
    case AppendData(table, query, writeOptions, isByName) =>
      s"${fromPlan(ctx, query)}\n.write.saveAsTable(${q(table.name)}, mode='append')"

    case SubqueryAlias(identifier, child) =>
      subqueryPlan(ctx, identifier, child)

    case p: Project =>
      projectPlan(ctx, p)

    case Filter(condition, child) =>
      filterPlan(ctx, condition, child)

    case Limit(expr, child) =>
      limitPlan(ctx, expr, child)

    case Sort(order, global, child) =>
      sortPlan(ctx, order, child)

    case relation: UnresolvedRelation =>
      relationPlan(relation)

    case a: Aggregate =>
      aggregatePlan(ctx, a)

    case Join(left, right, joinType, condition, _) =>
      joinPlan(ctx, left, right, joinType, condition)

    case r: Range =>
      rangePlan(r)

    case Union(children, byName, allowMissingCol) =>
      unionPlan(ctx, children, byName, allowMissingCol)

    case LocalRelation(attrs, data, _) =>
      localRelationPlan(attrs, data)

    case _ =>
      throw new NotImplementedError(plan.toString())
  }

  private def localRelationPlan(attrs: Seq[Attribute], data: Seq[InternalRow]) = {
    val refs = attrs.map(_.asInstanceOf[AttributeReference])
    val cols = refs.map(a => s"${a.name} ${a.dataType.sql}").mkString(", ")
    val rows = data.map(r => internalRow(r, refs)).map(r => s"  ($r)").mkString(",\n")
    s"spark.createDataFrame([\n$rows\n], '$cols')"
  }

  private def unionPlan(ctx: GeneratorContext, children: Seq[Plan], byName: Boolean,
                        allowMissingCol: Boolean) = {
    if (byName) {
      val unionArg = if (allowMissingCol) ", allowMissingColumns=True" else ""
      children.map(fromPlan(ctx, _)).reduce((l, r) => s"$l.unionByName($r$unionArg)")
    }
    else children.map(fromPlan(ctx, _)).reduce((l, r) => s"$l.union($r)")
  }

  private def rangePlan(r: Range) = {
    s"spark.range(${r.start}, ${r.end}, ${r.step})"
  }

  private def joinPlan(ctx: GeneratorContext, left: Plan, right: Plan,
                       joinType: JoinType, condition: Option[Expression]) = {
    // TODO: condition and hints are not yet supported
    val (tp, on) = joinType match {
      case UsingJoin(tp, usingColumns) => (tp, usingColumns)
      case tp => (tp, Seq())
    }
    val how = q(tp.sql.replace(" ", "_").toLowerCase)
    condition match {
      case Some(exp) =>
        s"""${fromPlan(ctx, left)}
           |.join(${fromPlan(ctx, right)},
           |${unfoldJoinCondition(ctx, exp)},
           |$how)""".stripMargin
      case None =>
        s"${fromPlan(ctx, left)}\n.join(${fromPlan(ctx, right)},\n${toPythonList(ctx, on)}, $how)"
    }
  }

  private def aggregatePlan(ctx: GeneratorContext, a: Aggregate) = {
    // matching against class name, as not all Spark implementations have compatible ABI
    val grpExprsRev = a.groupingExpressions.map(_.toString)
    // Removing col used for grouping from the agg expression
    val aggExprRev = a.aggregateExpressions.filter(item => !grpExprsRev.contains(item.toString))
    val aggs = smartDelimiters(ctx, aggExprRev.map(x => expressionCode(ctx, x)))
    val groupBy = exprList(ctx, a.groupingExpressions)
    s"${fromPlan(ctx, a.child)}\n.groupBy($groupBy)\n.agg($aggs)"
  }

  private def relationPlan(relation: UnresolvedRelation) = {
    s"spark.table(${q(relation.name)})"
  }

  private def sortPlan(ctx: GeneratorContext, order: Seq[SortOrder], child: Plan) = {
    val orderBy = order.map(item => {
      val dirStr = if (item.direction == Ascending) {
        "asc()"
      } else "desc()"
      item.child match {
        case Cast(colExpr, dataType, _) =>
          s"F.col(${q(expression(colExpr))}).cast(${q(dataType.simpleString)}).$dirStr"
        case UnresolvedAttribute(nameParts) =>
          s"F.col(${q(nameParts.mkString("."))}).$dirStr"
      }
    })
    s"${fromPlan(ctx, child)}\n.orderBy(${orderBy.mkString(", ")})"
  }

  private def limitPlan(ctx: GeneratorContext, expr: Expression, child: Plan) = {
    s"${fromPlan(ctx, child)}\n.limit($expr)"
  }

  private def filterPlan(ctx: GeneratorContext, condition: Expression, child: Plan) = {
    fromPlan(ctx, child) + "\n" + unfoldWheres(ctx, condition)
  }

  private def subqueryPlan(ctx: GeneratorContext, identifier: AliasIdentifier, child: Plan) = {
    s"${fromPlan(ctx, child)}.alias(${q(identifier.name)})"
  }

  private def projectPlan(ctx: GeneratorContext, p: Project): String = {
    val childCode = fromPlan(ctx, p.child)
    if (p.expressions.length - p.child.expressions.length == 1 || p.projectList.length == 1) {
      p.projectList.last match {
        case _: UnresolvedAttribute =>
          val columnNames = p.projectList.map(_.name).map(q).mkString(", ")
          s"$childCode\n.select($columnNames)"
        case Alias(UnresolvedAttribute(nameParts), name) if nameParts.length == 1 =>
          s"$childCode\n.withColumnRenamed(${q(nameParts.mkString("."))}, ${q(name)})"
        case Alias(child, name) =>
          child match {
            case UnresolvedAttribute(nameParts) =>
              if (nameParts.length > 1) {
                s"$childCode\n.withColumn(${q(name)}, ${expressionCode(ctx, child)})"
              } else {
                s"$childCode\n.withColumnRenamed(${q(nameParts.mkString("."))}, ${q(name)})"
              }
            case _ => s"$childCode\n.withColumn(${q(name)}, ${expressionCode(ctx, child)})"
          }
        case ur: UnresolvedRegex =>
          s"$childCode\n.selectExpr(${q(expression(ur))})"
        case us: UnresolvedStar =>
          us.target match {
            case Some(values) =>
              val starList = values.map(id => {
                val starExpr = s"${id}.*"
                s"F.col(${q(starExpr)})"
              }).mkString(", ")
              s"$childCode\n.select(${starList})"
            case None => ""
          }
        case _ =>
          throw new UnsupportedOperationException(s"cannot generate column: ${p.projectList.last}")
      }
    } else {
      s"$childCode\n.select(${exprCodeList(ctx.nest, p.projectList)})"
    }
  }

  private def internalRow(row: InternalRow, refs: Seq[AttributeReference]) =
    (0 until row.numFields).map(idx => refs(idx).dataType match {
      case StringType => q(row.getString(idx))
      case IntegerType => row.getInt(idx)
      case LongType => row.getLong(idx)
      case BooleanType => if (row.getBoolean(idx)) "True" else "False"
      case MapType(keyType, valueType, _) =>
        val map = row.getMap(idx)
        val ka = map.keyArray()
        val va = map.valueArray()
        (keyType, valueType) match {
          case (StringType, StringType) =>
            val keys = ka.toArray[String](keyType).sorted
            val values = va.toArray[String](valueType).sorted
            val kv = keys.zip(values).map(kv => s"    ${q(kv._1)}: ${q(kv._1)}").mkString(",\n")
            s"{$kv}"
          case _ => throw new NotImplementedError(
            s"Only string-string maps implemented. Field: ${refs(idx).name}")
        }
      case NullType => "None"
      case _ => throw new NotImplementedError(
        s"InternalRow gen: ${refs(idx).dataType.sql} not yet implemented")
    }).mkString(", ")

  private def exprCodeList(ctx: GeneratorContext, exprs: Seq[Expression]) =
    smartDelimiters(ctx, exprs.map(x => expressionCode(ctx, x)))

  private def exprList(ctx: GeneratorContext, exprs: Seq[Expression]) =
    smartDelimiters(ctx, exprs.map(expression).map(q))

  private def toPythonList(ctx: GeneratorContext, elements: Seq[String]): String =
    s"[${smartDelimiters(ctx, elements.map(q))}]"

  private def smartDelimiters(ctx: GeneratorContext, seq: Seq[String]) = {
    val default = seq.mkString(", ")
    if (default.length < ctx.maxLineWidth) default else seq.mkString(s",\n${ctx.ws}")
  }

  private def unfoldJoinCondition(ctx: GeneratorContext, expr: Expression): String = expr match {
    case And(left, right) =>
      s"${unfoldJoinCondition(ctx, left)} && ${unfoldJoinCondition(ctx, right)}"
    case _ => s"${expressionCode(ctx, expr)}"
  }

  private def unfoldWheres(ctx: GeneratorContext, expr: Expression): String = expr match {
    case And(left, right) => s"${unfoldWheres(ctx, left)}\n${unfoldWheres(ctx, right)}"
    case _ => s".where(${expressionCode(ctx, expr)})"
  }

  private def genSortOrderCode(ctx: GeneratorContext, sortOrder: SortOrder) = {
    sortOrder.direction match {
      case Ascending =>
        sortOrder.nullOrdering match {
          case NullsFirst =>
            s"${expressionCode(ctx, sortOrder.child)}.asc()"
          case NullsLast =>
            // default null ordering for `asc()` is NullsFirst
            s"${expressionCode(ctx, sortOrder.child)}.asc_null_last()"
        }
      case Descending =>
        sortOrder.nullOrdering match {
          case NullsFirst =>
            s"${expressionCode(ctx, sortOrder.child)}.desc_null_first()"
          case NullsLast =>
            // default null ordering for `desc()` is NullsLast
            s"${expressionCode(ctx, sortOrder.child)}.desc()"
        }
    }
  }

  private def genWindowSpecCode(ctx: GeneratorContext, ws: WindowSpecDefinition) = {
    val partGenCode = ws.partitionSpec.map(x => expressionCode(ctx, x)).mkString(", ")
    val orderByGenCode = ws.orderSpec.map(x => expressionCode(ctx, x)).mkString(", ")
    val windowGenCode = s"Window.partitionBy($partGenCode).orderBy($orderByGenCode)"
    ws.frameSpecification match {
      case UnspecifiedFrame => windowGenCode
      case SpecifiedWindowFrame(frameType, lower, upper) =>
        frameType match {
          case RangeFrame =>
            s"$windowGenCode.rangeBetween(${expression(lower)}, ${expression(upper)})"
          case RowFrame =>
            s"$windowGenCode.rowsBetween(${expression(lower)}, ${expression(upper)})"
        }
    }
  }

  private val jvmToPythonOverrides = Map(
    "&&" -> "&",
    "=" -> "==",
    "||" -> "|"
  )

  private def withParenthesesIfBinary(ctx: GeneratorContext, expr: Expression): String =
    expr match {
      case b: BinaryOperator =>
        s"(${binaryOperatorCode(ctx, b)})"
      case _ => expressionCode(ctx, expr)
    }

  private def binaryOperatorCode(ctx: GeneratorContext, b: BinaryOperator): String = {
    val symbol = jvmToPythonOverrides.getOrElse(b.symbol, b.symbol)
    val left = withParenthesesIfBinary(ctx, b.left)
    val oneLine = s"$left $symbol ${withParenthesesIfBinary(ctx.withRawLiteral, b.right)}"
    if (oneLine.length < ctx.maxLineWidth) {
      oneLine
    } else {
      val nest = ctx.nest.withRawLiteral // reformat for readability
      val right = withParenthesesIfBinary(nest, b.right)
      s"$left $symbol\n${nest.ws}$right"
    }
  }

  private def wrapLiteral(ctx: GeneratorContext, value: Any): String =
    if (ctx.wrapLiteral) s"F.lit($value)" else value.toString

  private def literalCode(ctx: GeneratorContext, l: Literal): String = l.dataType match {
    case BooleanType => wrapLiteral(ctx, if (l.value.asInstanceOf[Boolean]) "True" else "False")
    case IntegerType => wrapLiteral(ctx, l.value)
    case DoubleType => wrapLiteral(ctx, l.value)
    case StringType => wrapLiteral(ctx, q(l.value.toString))
    case NullType => wrapLiteral(ctx, "None")
  }

  private def expressionCode(ctx: GeneratorContext, expr: Expression): String = expr match {
    case b: BinaryOperator =>
      val op = binaryOperatorCode(ctx, b)
      op
    case Last(child, ignoreNulls) =>
      val pyBool = if (ignoreNulls.asInstanceOf[Boolean]) "True" else "False"
      s"F.last(${expressionCode(ctx, child)}, $pyBool)"
    case First(child, ignoreNulls) =>
      val pyBool = if (ignoreNulls.asInstanceOf[Boolean]) "True" else "False"
      s"F.first(${expressionCode(ctx, child)}, $pyBool)"
    case ArrayFilter(left, LambdaFunction(fn, args, _)) =>
      s"F.filter(${expressionCode(ctx, left)}, " +
        s"lambda ${args.map(expression).mkString(",")}: ${expressionCode(ctx, fn)})"
    case CaseWhen(branches: Seq[(Expression, Expression)], elseValue: Option[Expression]) =>
      caseWhenRep(ctx.nest, branches, elseValue)
    case In(attr, items) =>
      s"${expressionCode(ctx, attr)}.isin(${exprCodeList(ctx, items)})"
    case UnresolvedAlias(child, aliasFunc) =>
      expressionCode(ctx, child)
    case RLike(left, right) =>
      s"${expressionCode(ctx, left)}.rlike(${expressionCode(ctx, right)})"
    case l: Literal =>
      literalCode(ctx, l)
    case Alias(child, name) =>
      s"${expressionCode(ctx, child)}.alias(${q(name)})"
    case Count(children) =>
      s"F.count(${children.map(x => expressionCode(ctx, x)).mkString(", ")})"
    case Round(child, scale) =>
      s"F.round(${expressionCode(ctx, child)}, ${expression(scale)})"
    case Sum(child) =>
      s"F.sum(${expressionCode(ctx, child)})"
    case Length(child) =>
      s"F.length(${expressionCode(ctx, child)})"
    case Size(child, _) =>
      s"F.size(${expressionCode(ctx, child)})"
    case Cast(colExpr, dataType, _) =>
      s"${expressionCode(ctx, colExpr)}.cast(${q(dataType.simpleString)})"
    case Min(expr) =>
      s"F.min(${expressionCode(ctx, expr)})"
    case Max(expr) =>
      s"F.max(${expressionCode(ctx, expr)})"
    case Least(children) =>
      s"F.least(${children.map(x => expressionCode(ctx, x)).mkString(", ")})"
    case Greatest(children) =>
      s"F.greatest(${children.map(x => expressionCode(ctx, x)).mkString(", ")})"
    case MonotonicallyIncreasingID() =>
      s"F.monotonically_increasing_id()"
    case Concat(children) =>
      s"F.concat(${children.map(x => expressionCode(ctx, x)).mkString(", ")})"
    case ArrayJoin(array, delimiter, nullReplacement) =>
      s"F.array_join(${expressionCode(ctx, array)}, ${delimiter.sql})"
    case CollectList(child, x, y) =>
      s"F.collect_list(${expressionCode(ctx, child)})"
    case CollectSet(child, _, _) =>
      s"F.collect_set(${expressionCode(ctx, child)})"
    case RowNumber() =>
      s"F.row_number()"
    case DateFormatClass(left, right, _) =>
      s"F.date_format(${expressionCode(ctx, left)}, ${expression(right)})"
    case AggregateExpression(aggFn, mode, isDistinct, filter, resultId) =>
      expressionCode(ctx, aggFn)
    case CurrentRow =>
      "Window.currentRow"
    case UnboundedFollowing =>
      "Window.unboundedFollowing"
    case UnboundedPreceding =>
      "Window.unboundedPreceding"
    case so: SortOrder =>
      genSortOrderCode(ctx, so)
    case ur: UnresolvedRegex =>
      s"F.col(${q(s"`${ur.regexPattern}`")})"
    case RegExpExtract(subject, regexp, idx) =>
      s"F.regexp_extract(${expressionCode(ctx, subject)}, ${regexp.sql}, ${idx.sql})"
    case RegExpReplace(subject, regexp, rep, _) =>
      s"F.regexp_replace(${expressionCode(ctx, subject)}, ${regexp.sql}, ${rep.sql})"
    case WindowExpression(windowFunction, windowSpec) =>
      s"${expressionCode(ctx, windowFunction)}.over(${expressionCode(ctx, windowSpec)})"
    case ws: WindowSpecDefinition =>
      genWindowSpecCode(ctx, ws)
    case namedStruct: CreateNamedStruct =>
      s"F.struct(${namedStruct.valExprs.map(x => expressionCode(ctx, x)).mkString(", ")})"
    case fs: FormatString =>
      val items = fs.children.toList
      val exprs = items.tail.map(x => expressionCode(ctx, x)).mkString(", ")
      s"F.format_string(${q(items.head.toString())}, $exprs)"
    case attr: AttributeReference =>
      s"F.col(${q(attr.name)})"
    case attr: UnresolvedAttribute =>
      s"F.col(${q(attr.name)})"
    case attr: UnresolvedNamedLambdaVariable =>
      s"${attr.name}"
    case TimeWindow(col, window, slide, _) if window == slide =>
      val interval = IntervalUtils.stringToInterval(
        UTF8String.fromString(s"$window microseconds"))
      s"F.window(${expressionCode(ctx, col)}, '$interval')"
    case Explode(child) =>
      s"F.explode(${expressionCode(ctx, child)})"
    case Substring(str, pos, len) =>
      s"F.substring(${expressionCode(ctx, str)}, ${expression(pos)}, ${expression(len)})"
    case IsNotNull(child) =>
      s"${expressionCode(ctx, child)}.isNotNull()"
    case IsNull(child) =>
      s"${expressionCode(ctx, child)}.isNull()"
    case CurrentTimestamp() =>
      s"F.current_timestamp()"
    case Upper(child) =>
      s"F.upper(${expressionCode(ctx, child)})"
    case Like(col, Literal(value, _ @ StringType), _) =>
      s"${expressionCode(ctx, col)}.like('$value')"
    case GetMapValue(child, key, _) =>
      s"${expressionCode(ctx, child)}.getItem(${expressionCode(ctx, key)})"
    case StringSplit(child, Literal(regex, _ @ StringType), Literal(limit, _ @ IntegerType)) =>
      if (limit == -1) {
        s"F.split(${expressionCode(ctx, child)}, '$regex')"
      } else {
        s"F.split(${expressionCode(ctx, child)}, '$regex', $limit)"
      }
    case GetArrayItem(child, Literal(idx, _ @ IntegerType), _) =>
      s"${expressionCode(ctx, child)}[$idx]"
    case Not(child) =>
      s"!${expressionCode(ctx, child)}"
    case Coalesce(children) =>
      s"F.coalesce(${exprCodeList(ctx, children)})"
    case _ =>
      s"F.expr(${q(expr.sql)})"
  }

  /** Simplified SQL rendering of Spark expressions */
  def expression(expr: Expression): String = expr match {
    case EqualTo(attr: UnresolvedAttribute, value) =>
      s"${attr.name} = ${expression(value)}"
    case In(attr: UnresolvedAttribute, items) =>
      s"${attr.name} IN (${items.map(expression).mkString(", ")})"
    case UnresolvedAlias(child, aliasFunc) => expression(child)
    case Alias(child, name) => s"${expression(child)} AS $name"
    case RLike(left, right) => s"${left.sql} RLIKE ${right.sql}"
    case UnresolvedRegex(regexPattern, table, caseSensitive) => s"`$regexPattern`"
    case CurrentRow => "Window.currentRow"
    case UnboundedFollowing => "Window.unboundedFollowing"
    case UnboundedPreceding => "Window.unboundedPreceding"
    case attr: AttributeReference => attr.name
    case a: UnresolvedAttribute => a.name
    case _: Any => expr.sql
  }

  private def caseWhenRep(ctx: GeneratorContext, branches: Seq[(Expression, Expression)],
                          elseValue: Option[Expression]): String = {
    val nl = if (branches.size > 1) s"\n${ctx.ws}" else ""
    s"\n${ctx.ws}F" + branches.map(t => {
      val left = expressionCode(ctx, t._1)
      val right = expressionCode(ctx.withRawLiteral, t._2)
      val oneline = s".when($left, $right)" + nl
      if (oneline.length < ctx.maxLineWidth) {
        oneline
      } else {
        // do some reformatting because of maximum line width
        val nest = ctx.nest.withRawLiteral
        s".when($left,\n${nest.ws}${expressionCode(nest, t._2)})" + nl
      }
    }).mkString + (if (elseValue.isDefined) {
      s".otherwise(${expressionCode(ctx.withRawLiteral, elseValue.get)})"
    } else "")
  }

  /** Sugar for quoting strings */
  private def q(value: String) =
    if (pattern.findAllIn(value).toList.isEmpty) {
      "'" + value + "'"
    } else "\"" + value + "\""
}
