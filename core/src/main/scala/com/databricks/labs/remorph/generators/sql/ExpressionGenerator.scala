package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, TransformationConstructors, intermediate => ir}

import java.time._
import java.time.format.DateTimeFormatter
import java.util.Locale

class ExpressionGenerator extends BaseSQLGenerator[ir.Expression] with TransformationConstructors {
  private val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC"))

  override def generate(tree: ir.Expression): SQL =
    expression(tree)

  def expression(expr: ir.Expression): SQL = {
    val sql: SQL = expr match {
      case ir.Like(subject, pattern, escape) => likeSingle(subject, pattern, escape, caseSensitive = true)
      case ir.LikeAny(subject, patterns) => likeMultiple(subject, patterns, caseSensitive = true, all = false)
      case ir.LikeAll(subject, patterns) => likeMultiple(subject, patterns, caseSensitive = true, all = true)
      case ir.ILike(subject, pattern, escape) => likeSingle(subject, pattern, escape, caseSensitive = false)
      case ir.ILikeAny(subject, patterns) => likeMultiple(subject, patterns, caseSensitive = false, all = false)
      case ir.ILikeAll(subject, patterns) => likeMultiple(subject, patterns, caseSensitive = false, all = true)
      case r: ir.RLike => rlike(r)
      case _: ir.Bitwise => bitwise(expr)
      case _: ir.Arithmetic => arithmetic(expr)
      case b: ir.Between => between(b)
      case _: ir.Predicate => predicate(expr)
      case l: ir.Literal => literal(l)
      case a: ir.ArrayExpr => arrayExpr(a)
      case m: ir.MapExpr => mapExpr(m)
      case s: ir.StructExpr => structExpr(s)
      case i: ir.IsNull => isNull(i)
      case i: ir.IsNotNull => isNotNull(i)
      case ir.UnresolvedAttribute(name, _, _, _, _, _, _) => lift(OkResult(name))
      case d: ir.Dot => dot(d)
      case i: ir.Id => nameOrPosition(i)
      case o: ir.ObjectReference => objectReference(o)
      case a: ir.Alias => alias(a)
      case d: ir.Distinct => distinct(d)
      case s: ir.Star => star(s)
      case c: ir.Cast => cast(c)
      case t: ir.TryCast => tryCast(t)
      case col: ir.Column => column(col)
      case _: ir.DeleteAction => code"DELETE"
      case ia: ir.InsertAction => insertAction(ia)
      case ua: ir.UpdateAction => updateAction(ua)
      case a: ir.Assign => assign(a)
      case opts: ir.Options => options(opts)
      case i: ir.KnownInterval => interval(i)
      case s: ir.ScalarSubquery => scalarSubquery(s)
      case c: ir.Case => caseWhen(c)
      case w: ir.Window => window(w)
      case o: ir.SortOrder => sortOrder(o)
      case ir.Exists(subquery) =>
        withGenCtx(ctx => code"EXISTS (${ctx.logical.generate(subquery)})")
      case a: ir.ArrayAccess => arrayAccess(a)
      case j: ir.JsonAccess => jsonAccess(j)
      case l: ir.LambdaFunction => lambdaFunction(l)
      case v: ir.Variable => variable(v)
      case s: ir.SchemaReference => schemaReference(s)
      case r: ir.RegExpExtract => regexpExtract(r)
      case t: ir.TimestampDiff => timestampDiff(t)
      case t: ir.TimestampAdd => timestampAdd(t)
      case e: ir.Extract => extract(e)
      case c: ir.Concat => concat(c)
      case i: ir.In => in(i)

      // keep this case after every case involving an `Fn`, otherwise it will make said case unreachable
      case fn: ir.Fn => code"${fn.prettyName}(${commas(fn.children)})"

      // We see an unresolved for parsing errors, when we have no visitor for a given rule,
      // when something went wrong with IR generation, or when we have a visitor but it is not
      // yet implemented.
      case u: ir.Unresolved[_] => describeError(u)

      case null => code"" // don't fail transpilation if the expression is null
      case x => partialResult(x)
    }

    update { case g: Generating =>
      g.copy(currentNode = expr)
    }.flatMap(_ => sql)
  }

  private def structExpr(s: ir.StructExpr): SQL = {
    s.fields
      .map {
        case a: ir.Alias => generate(a)
        case s: ir.Star => code"*"
      }
      .mkCode("STRUCT(", ", ", ")")
  }

  private def jsonAccess(j: ir.JsonAccess): SQL = {
    val path = jsonPath(j.path).mkCode
    val anchorPath = path.map(p => if (p.head == '.') ':' +: p.tail else p)
    code"${expression(j.json)}$anchorPath"
  }

  private def jsonPath(j: ir.Expression): Seq[SQL] = {
    j match {
      case ir.Id(name, _) if isValidIdentifier(name) => Seq(code".$name")
      case ir.Id(name, _) => Seq(s"['$name']".replace("'", "\"")).map(OkResult(_)).map(lift)
      case ir.IntLiteral(value) => Seq(code"[$value]")
      case ir.StringLiteral(value) => Seq(code"['$value']")
      case ir.Dot(left, right) => jsonPath(left) ++ jsonPath(right)
      case i: ir.Expression => Seq(partialResult(i))
    }
  }

  private def isNull(i: ir.IsNull) = code"${expression(i.left)} IS NULL"
  private def isNotNull(i: ir.IsNotNull) = code"${expression(i.left)} IS NOT NULL"

  private def interval(interval: ir.KnownInterval): SQL = {
    val iType = interval.iType match {
      case ir.YEAR_INTERVAL => "YEAR"
      case ir.MONTH_INTERVAL => "MONTH"
      case ir.WEEK_INTERVAL => "WEEK"
      case ir.DAY_INTERVAL => "DAY"
      case ir.HOUR_INTERVAL => "HOUR"
      case ir.MINUTE_INTERVAL => "MINUTE"
      case ir.SECOND_INTERVAL => "SECOND"
      case ir.MILLISECOND_INTERVAL => "MILLISECOND"
      case ir.MICROSECOND_INTERVAL => "MICROSECOND"
      case ir.NANOSECOND_INTERVAL => "NANOSECOND"
    }
    code"INTERVAL ${generate(interval.value)} ${iType}"
  }

  private def options(opts: ir.Options): SQL = {
    // First gather the options that are set by expressions
    val exprOptions = opts.expressionOpts
      .map { case (key, expression) =>
        code"     ${key} = ${generate(expression)}\n"
      }
      .toSeq
      .mkCode
    val exprStr = exprOptions.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) {
        code"    Expression options:\n\n${exprOptions}\n"
      } else {
        code""
      }
    }
    val stringOptions = opts.stringOpts.map { case (key, value) =>
      s"     ${key} = '${value}'\n"
    }.mkString
    val stringStr = if (stringOptions.nonEmpty) {
      s"    String options:\n\n${stringOptions}\n"
    } else {
      ""
    }

    val boolOptions = opts.boolFlags.map { case (key, value) =>
      s"     ${key} ${if (value) { "ON" }
        else { "OFF" }}\n"
    }.mkString
    val boolStr = if (boolOptions.nonEmpty) {
      s"    Boolean options:\n\n${boolOptions}\n"
    } else {
      ""
    }

    val autoOptions = opts.autoFlags.map { key =>
      s"     ${key} AUTO\n"
    }.mkString
    val autoStr = if (autoOptions.nonEmpty) {
      s"    Auto options:\n\n${autoOptions}\n"
    } else {
      ""
    }
    val optString = code"${exprStr}${stringStr}${boolStr}${autoStr}"
    optString.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) {
        code"/*\n   The following statement was originally given the following OPTIONS:\n\n${optString}\n */\n"
      } else {
        code""
      }
    }
  }

  private def assign(assign: ir.Assign): SQL = {
    code"${expression(assign.left)} = ${expression(assign.right)}"
  }

  private def column(column: ir.Column): SQL = {
    val objectRef = column.tableNameOrAlias.map(or => code"${generateObjectReference(or)}.").getOrElse("")
    code"$objectRef${nameOrPosition(column.columnName)}"
  }

  private def insertAction(insertAction: ir.InsertAction): SQL = {
    val (cols, values) = insertAction.assignments.map { assign =>
      (assign.left, assign.right)
    }.unzip
    code"INSERT (${commas(cols)}) VALUES (${commas(values)})"
  }

  private def updateAction(updateAction: ir.UpdateAction): SQL = {
    code"UPDATE SET ${commas(updateAction.assignments)}"
  }

  private def arithmetic(expr: ir.Expression): SQL = expr match {
    case ir.UMinus(child) => code"-${expression(child)}"
    case ir.UPlus(child) => code"+${expression(child)}"
    case ir.Multiply(left, right) => code"${expression(left)} * ${expression(right)}"
    case ir.Divide(left, right) => code"${expression(left)} / ${expression(right)}"
    case ir.Mod(left, right) => code"${expression(left)} % ${expression(right)}"
    case ir.Add(left, right) => code"${expression(left)} + ${expression(right)}"
    case ir.Subtract(left, right) => code"${expression(left)} - ${expression(right)}"
  }

  private def bitwise(expr: ir.Expression): SQL = expr match {
    case ir.BitwiseOr(left, right) => code"${expression(left)} | ${expression(right)}"
    case ir.BitwiseAnd(left, right) => code"${expression(left)} & ${expression(right)}"
    case ir.BitwiseXor(left, right) => code"${expression(left)} ^ ${expression(right)}"
    case ir.BitwiseNot(child) => code"~${expression(child)}"
  }

  private def likeSingle(
      subject: ir.Expression,
      pattern: ir.Expression,
      escapeChar: Option[ir.Expression],
      caseSensitive: Boolean): SQL = {
    val op = if (caseSensitive) { "LIKE" }
    else { "ILIKE" }
    val escape = escapeChar.map(char => code" ESCAPE ${expression(char)}").getOrElse(code"")
    code"${expression(subject)} $op ${expression(pattern)}$escape"
  }

  private def likeMultiple(
      subject: ir.Expression,
      patterns: Seq[ir.Expression],
      caseSensitive: Boolean,
      all: Boolean): SQL = {
    val op = if (caseSensitive) { "LIKE" }
    else { "ILIKE" }
    val allOrAny = if (all) { "ALL" }
    else { "ANY" }
    code"${expression(subject)} $op $allOrAny ${patterns.map(expression(_)).mkCode("(", ", ", ")")}"
  }

  private def rlike(r: ir.RLike): SQL = {
    code"${expression(r.left)} RLIKE ${expression(r.right)}"
  }

  private def predicate(expr: ir.Expression): SQL = expr match {
    case a: ir.And => andPredicate(a)
    case o: ir.Or => orPredicate(o)
    case ir.Not(child) => code"NOT (${expression(child)})"
    case ir.Equals(left, right) => code"${expression(left)} = ${expression(right)}"
    case ir.NotEquals(left, right) => code"${expression(left)} != ${expression(right)}"
    case ir.LessThan(left, right) => code"${expression(left)} < ${expression(right)}"
    case ir.LessThanOrEqual(left, right) => code"${expression(left)} <= ${expression(right)}"
    case ir.GreaterThan(left, right) => code"${expression(left)} > ${expression(right)}"
    case ir.GreaterThanOrEqual(left, right) => code"${expression(left)} >= ${expression(right)}"
    case _ => partialResult(expr)
  }

  private def andPredicate(a: ir.And): SQL = a match {
    case ir.And(ir.Or(ol, or), right) =>
      code"(${expression(ol)} OR ${expression(or)}) AND ${expression(right)}"
    case ir.And(left, ir.Or(ol, or)) =>
      code"${expression(left)} AND (${expression(ol)} OR ${expression(or)})"
    case ir.And(left, right) => code"${expression(left)} AND ${expression(right)}"
  }

  private def orPredicate(a: ir.Or): SQL = a match {
    case ir.Or(ir.And(ol, or), right) =>
      code"(${expression(ol)} AND ${expression(or)}) OR ${expression(right)}"
    case ir.Or(left, ir.And(ol, or)) =>
      code"${expression(left)} OR (${expression(ol)} AND ${expression(or)})"
    case ir.Or(left, right) => code"${expression(left)} OR ${expression(right)}"
  }

  private def literal(l: ir.Literal): SQL =
    l match {
      case ir.Literal(_, ir.NullType) => code"NULL"
      case ir.Literal(bytes: Array[Byte], ir.BinaryType) => lift(OkResult(bytes.map("%02X" format _).mkString))
      case ir.Literal(value, ir.BooleanType) => lift(OkResult(value.toString.toLowerCase(Locale.getDefault)))
      case ir.Literal(value, ir.ShortType) => lift(OkResult(value.toString))
      case ir.IntLiteral(value) => lift(OkResult(value.toString))
      case ir.Literal(value, ir.LongType) => lift(OkResult(value.toString))
      case ir.FloatLiteral(value) => lift(OkResult(value.toString))
      case ir.DoubleLiteral(value) => lift(OkResult(value.toString))
      case ir.DecimalLiteral(value) => lift(OkResult(value.toString))
      case ir.Literal(value: String, ir.StringType) => singleQuote(value)
      case ir.Literal(epochDay: Long, ir.DateType) =>
        val dateStr = singleQuote(LocalDate.ofEpochDay(epochDay).format(dateFormat))
        code"CAST($dateStr AS DATE)"
      case ir.Literal(epochSecond: Long, ir.TimestampType) =>
        val timestampStr = singleQuote(
          LocalDateTime
            .from(ZonedDateTime.ofInstant(Instant.ofEpochSecond(epochSecond), ZoneId.of("UTC")))
            .format(timeFormat))
        code"CAST($timestampStr AS TIMESTAMP)"
      case _ => partialResult(l, ir.UnsupportedDataType(l.dataType.toString))
    }

  private def arrayExpr(a: ir.ArrayExpr): SQL = {
    val elementsStr = commas(a.children)
    code"ARRAY($elementsStr)"
  }

  private def mapExpr(m: ir.MapExpr): SQL = {
    val entriesStr = m.map
      .map { case (key, value) =>
        code"${expression(key)}, ${expression(value)}"
      }
      .toSeq
      .mkCode(", ")
    code"MAP($entriesStr)"
  }

  private def nameOrPosition(id: ir.NameOrPosition): SQL = id match {
    case ir.Id(name, true) => code"`$name`"
    case ir.Id(name, false) => ok(name)
    case ir.Name(name) => ok(name)
    case p @ ir.Position(_) => partialResult(p)
  }

  private def alias(alias: ir.Alias): SQL = {
    code"${expression(alias.expr)} AS ${expression(alias.name)}"
  }

  private def distinct(distinct: ir.Distinct): SQL = {
    code"DISTINCT ${expression(distinct.expression)}"
  }

  private def star(star: ir.Star): SQL = {
    val objectRef = star.objectName.map(or => code"${generateObjectReference(or)}.").getOrElse(code"")
    code"$objectRef*"
  }

  private def generateObjectReference(reference: ir.ObjectReference): SQL = {
    (reference.head +: reference.tail).map(nameOrPosition).mkCode(".")
  }

  private def cast(cast: ir.Cast): SQL = {
    castLike("CAST", cast.expr, cast.dataType)
  }

  private def tryCast(tryCast: ir.TryCast): SQL = {
    castLike("TRY_CAST", tryCast.expr, tryCast.dataType)
  }

  private def castLike(prettyName: String, expr: ir.Expression, dataType: ir.DataType): SQL = {
    val e = expression(expr)
    val dt = DataTypeGenerator.generateDataType(dataType)
    code"$prettyName($e AS $dt)"
  }

  private def dot(dot: ir.Dot): SQL = {
    code"${expression(dot.left)}.${expression(dot.right)}"
  }

  private def objectReference(objRef: ir.ObjectReference): SQL = {
    (objRef.head +: objRef.tail).map(nameOrPosition).mkCode(".")
  }

  private def caseWhen(c: ir.Case): SQL = {
    val expr = c.expression.map(expression).toSeq
    val branches = c.branches.map { branch =>
      code"WHEN ${expression(branch.condition)} THEN ${expression(branch.expression)}"
    }
    val otherwise = c.otherwise.map { o => code"ELSE ${expression(o)}" }.toSeq
    val chunks = expr ++ branches ++ otherwise
    chunks.mkCode("CASE ", " ", " END")
  }

  private def in(inExpr: ir.In): SQL = {
    val values = commas(inExpr.other)
    val enclosed = values.map { sql =>
      if (sql.charAt(0) == '(' && sql.charAt(sql.length - 1) == ')') {
        sql
      } else {
        "(" + sql + ")"
      }
    }
    code"${expression(inExpr.left)} IN ${enclosed}"
  }

  private def scalarSubquery(subquery: ir.ScalarSubquery): SQL = {
    withGenCtx(ctx => {
      val subcode = ctx.logical.generate(subquery.relation)
      code"(${subcode})"
    })
  }

  private def window(window: ir.Window): SQL = {
    val expr = expression(window.window_function)
    val partition = if (window.partition_spec.isEmpty) { code"" }
    else { window.partition_spec.map(expression).mkCode("PARTITION BY ", ", ", "") }
    val orderBy = if (window.sort_order.isEmpty) { code"" }
    else { window.sort_order.map(sortOrder).mkCode(" ORDER BY ", ", ", "") }
    val windowFrame = window.frame_spec
      .map { frame =>
        val mode = frame.frame_type match {
          case ir.RowsFrame => "ROWS"
          case ir.RangeFrame => "RANGE"
        }
        val boundaries = frameBoundary(frame.lower) ++ frameBoundary(frame.upper)
        val frameBoundaries = if (boundaries.size < 2) { boundaries.mkCode }
        else { boundaries.mkCode("BETWEEN ", " AND ", "") }
        code" $mode $frameBoundaries"
      }
      .getOrElse(code"")
    if (window.ignore_nulls) {
      return code"$expr IGNORE NULLS OVER ($partition$orderBy$windowFrame)"
    }

    code"$expr OVER ($partition$orderBy$windowFrame)"
  }

  private def frameBoundary(boundary: ir.FrameBoundary): Seq[SQL] = boundary match {
    case ir.NoBoundary => Seq.empty
    case ir.CurrentRow => Seq(code"CURRENT ROW")
    case ir.UnboundedPreceding => Seq(code"UNBOUNDED PRECEDING")
    case ir.UnboundedFollowing => Seq(code"UNBOUNDED FOLLOWING")
    case ir.PrecedingN(n) => Seq(code"${expression(n)} PRECEDING")
    case ir.FollowingN(n) => Seq(code"${expression(n)} FOLLOWING")
  }

  private def sortOrder(order: ir.SortOrder): SQL = {
    val orderBy = expression(order.child)
    val direction = order.direction match {
      case ir.Ascending => Seq(code"ASC")
      case ir.Descending => Seq(code"DESC")
      case ir.UnspecifiedSortDirection => Seq()
    }
    val nulls = order.nullOrdering match {
      case ir.NullsFirst => Seq(code"NULLS FIRST")
      case ir.NullsLast => Seq(code"NULLS LAST")
      case ir.SortNullsUnspecified => Seq()
    }
    (Seq(orderBy) ++ direction ++ nulls).mkCode(" ")
  }

  private def regexpExtract(extract: ir.RegExpExtract): SQL = {
    val c = if (extract.c == ir.Literal(1)) { code"" }
    else { code", ${expression(extract.c)}" }
    code"${extract.prettyName}(${expression(extract.left)}, ${expression(extract.right)}$c)"
  }

  private def arrayAccess(access: ir.ArrayAccess): SQL = {
    code"${expression(access.array)}[${expression(access.index)}]"
  }

  private def timestampDiff(diff: ir.TimestampDiff): SQL = {
    code"${diff.prettyName}(${diff.unit}, ${expression(diff.start)}, ${expression(diff.end)})"
  }

  private def timestampAdd(tsAdd: ir.TimestampAdd): SQL = {
    code"${tsAdd.prettyName}(${tsAdd.unit}, ${expression(tsAdd.quantity)}, ${expression(tsAdd.timestamp)})"
  }

  private def extract(e: ir.Extract): SQL = {
    code"EXTRACT(${expression(e.left)} FROM ${expression(e.right)})"
  }

  private def lambdaFunction(l: ir.LambdaFunction): SQL = {
    val parameterList = l.arguments.map(lambdaArgument)
    val parameters = if (parameterList.size > 1) { parameterList.mkCode("(", ", ", ")") }
    else { parameterList.mkCode }
    val body = expression(l.function)
    code"$parameters -> $body"
  }

  private def lambdaArgument(arg: ir.UnresolvedNamedLambdaVariable): SQL = {
    lift(OkResult(arg.name_parts.mkString(".")))
  }

  private def variable(v: ir.Variable): SQL = code"$${${v.name}}"

  private def concat(c: ir.Concat): SQL = {
    val args = c.children.map(expression(_))
    if (c.children.size > 2) {
      args.mkCode(" || ")
    } else {
      args.mkCode("CONCAT(", ", ", ")")
    }
  }

  private def schemaReference(s: ir.SchemaReference): SQL = {
    val ref = s.columnName match {
      case d: ir.Dot => expression(d)
      case i: ir.Id => expression(i)
      case _ => code"JSON_COLUMN"
    }
    code"{${ref.map(_.toUpperCase(Locale.getDefault()))}_SCHEMA}"
  }
  private def singleQuote(s: String): SQL = code"'${s.replace("'", "\\'")}'"
  private def isValidIdentifier(s: String): Boolean =
    (s.head.isLetter || s.head == '_') && s.forall(x => x.isLetterOrDigit || x == '_')

  private def between(b: ir.Between): SQL = {
    code"${expression(b.exp)} BETWEEN ${expression(b.lower)} AND ${expression(b.upper)}"
  }

}
