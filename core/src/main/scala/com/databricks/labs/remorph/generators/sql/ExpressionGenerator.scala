package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, RemorphContext, TBA, TBAS, intermediate => ir}

import java.time._
import java.time.format.DateTimeFormatter
import java.util.Locale

class ExpressionGenerator extends BaseSQLGenerator[ir.Expression] with TBAS[RemorphContext] {
  private val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC"))

  override def generate(ctx: GeneratorContext, tree: ir.Expression): TBA[RemorphContext, String] = expression(ctx, tree)

  def expression(ctx: GeneratorContext, expr: ir.Expression): TBA[RemorphContext, String] = {
    val sql: SQL = expr match {
      case ir.Like(subject, pattern, escape) => likeSingle(ctx, subject, pattern, escape, caseSensitive = true)
      case ir.LikeAny(subject, patterns) => likeMultiple(ctx, subject, patterns, caseSensitive = true, all = false)
      case ir.LikeAll(subject, patterns) => likeMultiple(ctx, subject, patterns, caseSensitive = true, all = true)
      case ir.ILike(subject, pattern, escape) => likeSingle(ctx, subject, pattern, escape, caseSensitive = false)
      case ir.ILikeAny(subject, patterns) => likeMultiple(ctx, subject, patterns, caseSensitive = false, all = false)
      case ir.ILikeAll(subject, patterns) => likeMultiple(ctx, subject, patterns, caseSensitive = false, all = true)
      case r: ir.RLike => rlike(ctx, r)
      case _: ir.Bitwise => bitwise(ctx, expr)
      case _: ir.Arithmetic => arithmetic(ctx, expr)
      case b: ir.Between => between(ctx, b)
      case _: ir.Predicate => predicate(ctx, expr)
      case l: ir.Literal => literal(ctx, l)
      case a: ir.ArrayExpr => arrayExpr(ctx, a)
      case m: ir.MapExpr => mapExpr(ctx, m)
      case s: ir.StructExpr => structExpr(ctx, s)
      case i: ir.IsNull => isNull(ctx, i)
      case i: ir.IsNotNull => isNotNull(ctx, i)
      case ir.UnresolvedAttribute(name, _, _, _, _, _, _) => lift(OkResult(name))
      case d: ir.Dot => dot(ctx, d)
      case i: ir.Id => id(ctx, i)
      case o: ir.ObjectReference => objectReference(ctx, o)
      case a: ir.Alias => alias(ctx, a)
      case d: ir.Distinct => distinct(ctx, d)
      case s: ir.Star => star(ctx, s)
      case c: ir.Cast => cast(ctx, c)
      case t: ir.TryCast => tryCast(ctx, t)
      case col: ir.Column => column(ctx, col)
      case _: ir.DeleteAction => tba"DELETE"
      case ia: ir.InsertAction => insertAction(ctx, ia)
      case ua: ir.UpdateAction => updateAction(ctx, ua)
      case a: ir.Assign => assign(ctx, a)
      case opts: ir.Options => options(ctx, opts)
      case i: ir.KnownInterval => interval(ctx, i)
      case s: ir.ScalarSubquery => scalarSubquery(ctx, s)
      case c: ir.Case => caseWhen(ctx, c)
      case w: ir.Window => window(ctx, w)
      case o: ir.SortOrder => sortOrder(ctx, o)
      case ir.Exists(subquery) => tba"EXISTS (${ctx.logical.generate(ctx, subquery)})"
      case a: ir.ArrayAccess => arrayAccess(ctx, a)
      case j: ir.JsonAccess => jsonAccess(ctx, j)
      case l: ir.LambdaFunction => lambdaFunction(ctx, l)
      case v: ir.Variable => variable(ctx, v)
      case s: ir.SchemaReference => schemaReference(ctx, s)
      case r: ir.RegExpExtract => regexpExtract(ctx, r)
      case t: ir.TimestampDiff => timestampDiff(ctx, t)
      case t: ir.TimestampAdd => timestampAdd(ctx, t)
      case e: ir.Extract => extract(ctx, e)
      case c: ir.Concat => concat(ctx, c)
      case i: ir.In => in(ctx, i)

      // keep this case after every case involving an `Fn`, otherwise it will make said case unreachable
      case fn: ir.Fn => tba"${fn.prettyName}(${fn.children.map(expression(ctx, _)).mkTba(", ")})"

      // We see an unresolved for parsing errors, when we have no visitor for a given rule,
      // when something went wrong with IR generation, or when we have a visitor but it is not
      // yet implemented.
      case u: ir.Unresolved[_] => describeError(u)

      case null => tba"" // don't fail transpilation if the expression is null
      case x => partialResult(x)
    }

    update { case g: Generating =>
      g.copy(currentNode = expr)
    }.flatMap(_ => sql)
  }

  private def structExpr(ctx: GeneratorContext, s: ir.StructExpr): SQL = {
    s.fields
      .map {
        case a: ir.Alias => generate(ctx, a)
        case s: ir.Star => tba"*"
      }
      .mkTba("STRUCT(", ", ", ")")
  }

  private def jsonAccess(ctx: GeneratorContext, j: ir.JsonAccess): SQL = {
    val path = jsonPath(j.path).mkTba
    val anchorPath = path.map(p => if (p.head == '.') ':' +: p.tail else p)
    tba"${expression(ctx, j.json)}$anchorPath"
  }

  private def jsonPath(j: ir.Expression): Seq[SQL] = {
    j match {
      case ir.Id(name, _) if isValidIdentifier(name) => Seq(tba".$name")
      case ir.Id(name, _) => Seq(s"['$name']".replace("'", "\"")).map(OkResult(_)).map(lift)
      case ir.IntLiteral(value) => Seq(tba"[$value]")
      case ir.StringLiteral(value) => Seq(tba"['$value']")
      case ir.Dot(left, right) => jsonPath(left) ++ jsonPath(right)
      case i: ir.Expression => Seq(partialResult(i))
    }
  }

  private def isNull(ctx: GeneratorContext, i: ir.IsNull) = tba"${expression(ctx, i.left)} IS NULL"
  private def isNotNull(ctx: GeneratorContext, i: ir.IsNotNull) = tba"${expression(ctx, i.left)} IS NOT NULL"

  private def interval(ctx: GeneratorContext, interval: ir.KnownInterval): SQL = {
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
    tba"INTERVAL ${generate(ctx, interval.value)} ${iType}"
  }

  private def options(ctx: GeneratorContext, opts: ir.Options): SQL = {
    // First gather the options that are set by expressions
    val exprOptions = opts.expressionOpts
      .map { case (key, expression) =>
        tba"     ${key} = ${generate(ctx, expression)}\n"
      }
      .toSeq
      .mkTba
    val exprStr = exprOptions.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) {
        tba"    Expression options:\n\n${exprOptions}\n"
      } else {
        tba""
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
    val optString = tba"${exprStr}${stringStr}${boolStr}${autoStr}"
    optString.nonEmpty.flatMap { nonEmpty =>
      if (nonEmpty) {
        tba"/*\n   The following statement was originally given the following OPTIONS:\n\n${optString}\n */\n"
      } else {
        tba""
      }
    }
  }

  private def assign(ctx: GeneratorContext, assign: ir.Assign): SQL = {
    tba"${expression(ctx, assign.left)} = ${expression(ctx, assign.right)}"
  }

  private def column(ctx: GeneratorContext, column: ir.Column): SQL = {
    val objectRef = column.tableNameOrAlias.map(or => tba"${generateObjectReference(ctx, or)}.").getOrElse("")
    tba"$objectRef${id(ctx, column.columnName)}"
  }

  private def insertAction(ctx: GeneratorContext, insertAction: ir.InsertAction): SQL = {
    val (cols, values) = insertAction.assignments.map { assign =>
      (generate(ctx, assign.left), generate(ctx, assign.right))
    }.unzip
    tba"INSERT (${cols.mkTba(", ")}) VALUES (${values.mkTba(", ")})"
  }

  private def updateAction(ctx: GeneratorContext, updateAction: ir.UpdateAction): SQL = {
    tba"UPDATE SET ${updateAction.assignments.map(assign => generate(ctx, assign)).mkTba(", ")}"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case ir.UMinus(child) => tba"-${expression(ctx, child)}"
    case ir.UPlus(child) => tba"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => tba"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => tba"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => tba"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => tba"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => tba"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  private def bitwise(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case ir.BitwiseOr(left, right) => tba"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => tba"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.BitwiseXor(left, right) => tba"${expression(ctx, left)} ^ ${expression(ctx, right)}"
    case ir.BitwiseNot(child) => tba"~${expression(ctx, child)}"
  }

  private def likeSingle(
      ctx: GeneratorContext,
      subject: ir.Expression,
      pattern: ir.Expression,
      escapeChar: Option[ir.Expression],
      caseSensitive: Boolean): SQL = {
    val op = if (caseSensitive) { "LIKE" }
    else { "ILIKE" }
    val escape = escapeChar.map(char => tba" ESCAPE ${expression(ctx, char)}").getOrElse(tba"")
    tba"${expression(ctx, subject)} $op ${expression(ctx, pattern)}$escape"
  }

  private def likeMultiple(
      ctx: GeneratorContext,
      subject: ir.Expression,
      patterns: Seq[ir.Expression],
      caseSensitive: Boolean,
      all: Boolean): SQL = {
    val op = if (caseSensitive) { "LIKE" }
    else { "ILIKE" }
    val allOrAny = if (all) { "ALL" }
    else { "ANY" }
    tba"${expression(ctx, subject)} $op $allOrAny ${patterns.map(expression(ctx, _)).mkTba("(", ", ", ")")}"
  }

  private def rlike(ctx: GeneratorContext, r: ir.RLike): SQL = {
    tba"${expression(ctx, r.left)} RLIKE ${expression(ctx, r.right)}"
  }

  private def predicate(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case a: ir.And => andPredicate(ctx, a)
    case o: ir.Or => orPredicate(ctx, o)
    case ir.Not(child) => tba"NOT (${expression(ctx, child)})"
    case ir.Equals(left, right) => tba"${expression(ctx, left)} = ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => tba"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => tba"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => tba"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => tba"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => tba"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => partialResult(expr)
  }

  private def andPredicate(ctx: GeneratorContext, a: ir.And): SQL = a match {
    case ir.And(ir.Or(ol, or), right) =>
      tba"(${expression(ctx, ol)} OR ${expression(ctx, or)}) AND ${expression(ctx, right)}"
    case ir.And(left, ir.Or(ol, or)) =>
      tba"${expression(ctx, left)} AND (${expression(ctx, ol)} OR ${expression(ctx, or)})"
    case ir.And(left, right) => tba"${expression(ctx, left)} AND ${expression(ctx, right)}"
  }

  private def orPredicate(ctx: GeneratorContext, a: ir.Or): SQL = a match {
    case ir.Or(ir.And(ol, or), right) =>
      tba"(${expression(ctx, ol)} AND ${expression(ctx, or)}) OR ${expression(ctx, right)}"
    case ir.Or(left, ir.And(ol, or)) =>
      tba"${expression(ctx, left)} OR (${expression(ctx, ol)} AND ${expression(ctx, or)})"
    case ir.Or(left, right) => tba"${expression(ctx, left)} OR ${expression(ctx, right)}"
  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): SQL =
    l match {
      case ir.Literal(_, ir.NullType) => tba"NULL"
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
        tba"CAST($dateStr AS DATE)"
      case ir.Literal(epochSecond: Long, ir.TimestampType) =>
        val timestampStr = singleQuote(
          LocalDateTime
            .from(ZonedDateTime.ofInstant(Instant.ofEpochSecond(epochSecond), ZoneId.of("UTC")))
            .format(timeFormat))
        tba"CAST($timestampStr AS TIMESTAMP)"
      case _ => partialResult(l, ir.UnsupportedDataType(l.dataType.toString))
    }

  private def arrayExpr(ctx: GeneratorContext, a: ir.ArrayExpr): SQL = {
    val elementsStr = a.children.map(expression(ctx, _)).mkTba(", ")
    tba"ARRAY($elementsStr)"
  }

  private def mapExpr(ctx: GeneratorContext, m: ir.MapExpr): SQL = {
    val entriesStr = m.map
      .map { case (key, value) =>
        tba"${expression(ctx, key)}, ${expression(ctx, value)}"
      }
      .toSeq
      .mkTba(", ")
    tba"MAP($entriesStr)"
  }

  private def id(ctx: GeneratorContext, id: ir.Id): SQL = id match {
    case ir.Id(name, true) => tba"`$name`"
    case ir.Id(name, false) => lift(OkResult(name))
  }

  private def alias(ctx: GeneratorContext, alias: ir.Alias): SQL = {
    tba"${expression(ctx, alias.expr)} AS ${expression(ctx, alias.name)}"
  }

  private def distinct(ctx: GeneratorContext, distinct: ir.Distinct): SQL = {
    tba"DISTINCT ${expression(ctx, distinct.expression)}"
  }

  private def star(ctx: GeneratorContext, star: ir.Star): SQL = {
    val objectRef = star.objectName.map(or => tba"${generateObjectReference(ctx, or)}.").getOrElse(tba"")
    tba"$objectRef*"
  }

  private def generateObjectReference(ctx: GeneratorContext, reference: ir.ObjectReference): SQL = {
    (reference.head +: reference.tail).map(id(ctx, _)).mkTba(".")
  }

  private def cast(ctx: GeneratorContext, cast: ir.Cast): SQL = {
    castLike(ctx, "CAST", cast.expr, cast.dataType)
  }

  private def tryCast(ctx: GeneratorContext, tryCast: ir.TryCast): SQL = {
    castLike(ctx, "TRY_CAST", tryCast.expr, tryCast.dataType)
  }

  private def castLike(ctx: GeneratorContext, prettyName: String, expr: ir.Expression, dataType: ir.DataType): SQL = {
    val e = expression(ctx, expr)
    val dt = DataTypeGenerator.generateDataType(ctx, dataType)
    tba"$prettyName($e AS $dt)"
  }

  private def dot(ctx: GeneratorContext, dot: ir.Dot): SQL = {
    tba"${expression(ctx, dot.left)}.${expression(ctx, dot.right)}"
  }

  private def objectReference(ctx: GeneratorContext, objRef: ir.ObjectReference): SQL = {
    (objRef.head +: objRef.tail).map(id(ctx, _)).mkTba(".")
  }

  private def caseWhen(ctx: GeneratorContext, c: ir.Case): SQL = {
    val expr = c.expression.map(expression(ctx, _)).toSeq
    val branches = c.branches.map { branch =>
      tba"WHEN ${expression(ctx, branch.condition)} THEN ${expression(ctx, branch.expression)}"
    }
    val otherwise = c.otherwise.map { o => tba"ELSE ${expression(ctx, o)}" }.toSeq
    val chunks = expr ++ branches ++ otherwise
    chunks.mkTba("CASE ", " ", " END")
  }

  private def in(ctx: GeneratorContext, inExpr: ir.In): SQL = {
    val values = inExpr.other.map(expression(ctx, _)).mkTba(", ")
    tba"${expression(ctx, inExpr.left)} IN ($values)"
  }

  private def scalarSubquery(ctx: GeneratorContext, subquery: ir.ScalarSubquery): SQL = {
    ctx.logical.generate(ctx, subquery.relation)
  }

  private def window(ctx: GeneratorContext, window: ir.Window): SQL = {
    val expr = expression(ctx, window.window_function)
    val partition = if (window.partition_spec.isEmpty) { tba"" }
    else { window.partition_spec.map(expression(ctx, _)).mkTba("PARTITION BY ", ", ", "") }
    val orderBy = if (window.sort_order.isEmpty) { tba"" }
    else { window.sort_order.map(sortOrder(ctx, _)).mkTba(" ORDER BY ", ", ", "") }
    val windowFrame = window.frame_spec
      .map { frame =>
        val mode = frame.frame_type match {
          case ir.RowsFrame => "ROWS"
          case ir.RangeFrame => "RANGE"
        }
        val boundaries = frameBoundary(ctx, frame.lower) ++ frameBoundary(ctx, frame.upper)
        val frameBoundaries = if (boundaries.size < 2) { boundaries.mkTba }
        else { boundaries.mkTba("BETWEEN ", " AND ", "") }
        tba" $mode $frameBoundaries"
      }
      .getOrElse(tba"")
    if (window.ignore_nulls) {
      return tba"$expr IGNORE NULLS OVER ($partition$orderBy$windowFrame)"
    }

    tba"$expr OVER ($partition$orderBy$windowFrame)"
  }

  private def frameBoundary(ctx: GeneratorContext, boundary: ir.FrameBoundary): Seq[SQL] = boundary match {
    case ir.NoBoundary => Seq.empty
    case ir.CurrentRow => Seq(tba"CURRENT ROW")
    case ir.UnboundedPreceding => Seq(tba"UNBOUNDED PRECEDING")
    case ir.UnboundedFollowing => Seq(tba"UNBOUNDED FOLLOWING")
    case ir.PrecedingN(n) => Seq(tba"${expression(ctx, n)} PRECEDING")
    case ir.FollowingN(n) => Seq(tba"${expression(ctx, n)} FOLLOWING")
  }

  private def sortOrder(ctx: GeneratorContext, order: ir.SortOrder): SQL = {
    val orderBy = expression(ctx, order.child)
    val direction = order.direction match {
      case ir.Ascending => Seq(tba"ASC")
      case ir.Descending => Seq(tba"DESC")
      case ir.UnspecifiedSortDirection => Seq()
    }
    val nulls = order.nullOrdering match {
      case ir.NullsFirst => Seq(tba"NULLS FIRST")
      case ir.NullsLast => Seq(tba"NULLS LAST")
      case ir.SortNullsUnspecified => Seq()
    }
    (Seq(orderBy) ++ direction ++ nulls).mkTba(" ")
  }

  private def regexpExtract(ctx: GeneratorContext, extract: ir.RegExpExtract): SQL = {
    val c = if (extract.c == ir.Literal(1)) { tba"" }
    else { tba", ${expression(ctx, extract.c)}" }
    tba"${extract.prettyName}(${expression(ctx, extract.left)}, ${expression(ctx, extract.right)}$c)"
  }

  private def arrayAccess(ctx: GeneratorContext, access: ir.ArrayAccess): SQL = {
    tba"${expression(ctx, access.array)}[${expression(ctx, access.index)}]"
  }

  private def timestampDiff(ctx: GeneratorContext, diff: ir.TimestampDiff): SQL = {
    tba"${diff.prettyName}(${diff.unit}, ${expression(ctx, diff.start)}, ${expression(ctx, diff.end)})"
  }

  private def timestampAdd(ctx: GeneratorContext, tsAdd: ir.TimestampAdd): SQL = {
    tba"${tsAdd.prettyName}(${tsAdd.unit}, ${expression(ctx, tsAdd.quantity)}, ${expression(ctx, tsAdd.timestamp)})"
  }

  private def extract(ctx: GeneratorContext, e: ir.Extract): SQL = {
    tba"EXTRACT(${expression(ctx, e.left)} FROM ${expression(ctx, e.right)})"
  }

  private def lambdaFunction(ctx: GeneratorContext, l: ir.LambdaFunction): SQL = {
    val parameterList = l.arguments.map(lambdaArgument)
    val parameters = if (parameterList.size > 1) { parameterList.mkTba("(", ", ", ")") }
    else { parameterList.mkTba }
    val body = expression(ctx, l.function)
    tba"$parameters -> $body"
  }

  private def lambdaArgument(arg: ir.UnresolvedNamedLambdaVariable): SQL = {
    lift(OkResult(arg.name_parts.mkString(".")))
  }

  private def variable(ctx: GeneratorContext, v: ir.Variable): SQL = tba"$${${v.name}}"

  private def concat(ctx: GeneratorContext, c: ir.Concat): SQL = {
    val args = c.children.map(expression(ctx, _))
    if (c.children.size > 2) {
      args.mkTba(" || ")
    } else {
      args.mkTba("CONCAT(", ", ", ")")
    }
  }

  private def schemaReference(ctx: GeneratorContext, s: ir.SchemaReference): SQL = {
    val ref = s.columnName match {
      case d: ir.Dot => expression(ctx, d)
      case i: ir.Id => expression(ctx, i)
      case _ => tba"JSON_COLUMN"
    }
    tba"{${ref.map(_.toUpperCase(Locale.getDefault()))}_SCHEMA}"
  }
  private def singleQuote(s: String): SQL = tba"'$s'"
  private def isValidIdentifier(s: String): Boolean =
    (s.head.isLetter || s.head == '_') && s.forall(x => x.isLetterOrDigit || x == '_')

  private def between(ctx: GeneratorContext, b: ir.Between): SQL = {
    tba"${expression(ctx, b.exp)} BETWEEN ${expression(ctx, b.lower)} AND ${expression(ctx, b.upper)}"
  }

}
