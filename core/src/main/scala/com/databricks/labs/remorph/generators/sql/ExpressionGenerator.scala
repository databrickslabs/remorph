package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.{Generating, OkResult, Phase, Transformation, TransformationConstructors, intermediate => ir}

import java.time._
import java.time.format.DateTimeFormatter
import java.util.Locale

class ExpressionGenerator extends BaseSQLGenerator[ir.Expression] with TransformationConstructors[Phase] {
  private val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC"))

  override def generate(ctx: GeneratorContext, tree: ir.Expression): Transformation[Phase, String] =
    expression(ctx, tree)

  def expression(ctx: GeneratorContext, expr: ir.Expression): Transformation[Phase, String] = {
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
      case _: ir.DeleteAction => code"DELETE"
      case ia: ir.InsertAction => insertAction(ctx, ia)
      case ua: ir.UpdateAction => updateAction(ctx, ua)
      case a: ir.Assign => assign(ctx, a)
      case opts: ir.Options => options(ctx, opts)
      case i: ir.KnownInterval => interval(ctx, i)
      case s: ir.ScalarSubquery => scalarSubquery(ctx, s)
      case c: ir.Case => caseWhen(ctx, c)
      case w: ir.Window => window(ctx, w)
      case o: ir.SortOrder => sortOrder(ctx, o)
      case ir.Exists(subquery) => code"EXISTS (${ctx.logical.generate(ctx, subquery)})"
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
      case fn: ir.Fn => code"${fn.prettyName}(${commas(ctx, fn.children)})"

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

  private def structExpr(ctx: GeneratorContext, s: ir.StructExpr): SQL = {
    s.fields
      .map {
        case a: ir.Alias => generate(ctx, a)
        case s: ir.Star => code"*"
      }
      .mkCode("STRUCT(", ", ", ")")
  }

  private def jsonAccess(ctx: GeneratorContext, j: ir.JsonAccess): SQL = {
    val path = jsonPath(j.path).mkCode
    val anchorPath = path.map(p => if (p.head == '.') ':' +: p.tail else p)
    code"${expression(ctx, j.json)}$anchorPath"
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

  private def isNull(ctx: GeneratorContext, i: ir.IsNull) = code"${expression(ctx, i.left)} IS NULL"
  private def isNotNull(ctx: GeneratorContext, i: ir.IsNotNull) = code"${expression(ctx, i.left)} IS NOT NULL"

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
    code"INTERVAL ${generate(ctx, interval.value)} ${iType}"
  }

  private def options(ctx: GeneratorContext, opts: ir.Options): SQL = {
    // First gather the options that are set by expressions
    val exprOptions = opts.expressionOpts
      .map { case (key, expression) =>
        code"     ${key} = ${generate(ctx, expression)}\n"
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

  private def assign(ctx: GeneratorContext, assign: ir.Assign): SQL = {
    code"${expression(ctx, assign.left)} = ${expression(ctx, assign.right)}"
  }

  private def column(ctx: GeneratorContext, column: ir.Column): SQL = {
    val objectRef = column.tableNameOrAlias.map(or => code"${generateObjectReference(ctx, or)}.").getOrElse("")
    code"$objectRef${id(ctx, column.columnName)}"
  }

  private def insertAction(ctx: GeneratorContext, insertAction: ir.InsertAction): SQL = {
    val (cols, values) = insertAction.assignments.map { assign =>
      (assign.left, assign.right)
    }.unzip
    code"INSERT (${commas(ctx, cols)}) VALUES (${commas(ctx, values)})"
  }

  private def updateAction(ctx: GeneratorContext, updateAction: ir.UpdateAction): SQL = {
    code"UPDATE SET ${commas(ctx, updateAction.assignments)}"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case ir.UMinus(child) => code"-${expression(ctx, child)}"
    case ir.UPlus(child) => code"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => code"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => code"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => code"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => code"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => code"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  private def bitwise(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case ir.BitwiseOr(left, right) => code"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => code"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.BitwiseXor(left, right) => code"${expression(ctx, left)} ^ ${expression(ctx, right)}"
    case ir.BitwiseNot(child) => code"~${expression(ctx, child)}"
  }

  private def likeSingle(
      ctx: GeneratorContext,
      subject: ir.Expression,
      pattern: ir.Expression,
      escapeChar: Option[ir.Expression],
      caseSensitive: Boolean): SQL = {
    val op = if (caseSensitive) { "LIKE" }
    else { "ILIKE" }
    val escape = escapeChar.map(char => code" ESCAPE ${expression(ctx, char)}").getOrElse(code"")
    code"${expression(ctx, subject)} $op ${expression(ctx, pattern)}$escape"
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
    code"${expression(ctx, subject)} $op $allOrAny ${patterns.map(expression(ctx, _)).mkCode("(", ", ", ")")}"
  }

  private def rlike(ctx: GeneratorContext, r: ir.RLike): SQL = {
    code"${expression(ctx, r.left)} RLIKE ${expression(ctx, r.right)}"
  }

  private def predicate(ctx: GeneratorContext, expr: ir.Expression): SQL = expr match {
    case a: ir.And => andPredicate(ctx, a)
    case o: ir.Or => orPredicate(ctx, o)
    case ir.Not(child) => code"NOT (${expression(ctx, child)})"
    case ir.Equals(left, right) => code"${expression(ctx, left)} = ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => code"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => code"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => code"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => code"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => code"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => partialResult(expr)
  }

  private def andPredicate(ctx: GeneratorContext, a: ir.And): SQL = a match {
    case ir.And(ir.Or(ol, or), right) =>
      code"(${expression(ctx, ol)} OR ${expression(ctx, or)}) AND ${expression(ctx, right)}"
    case ir.And(left, ir.Or(ol, or)) =>
      code"${expression(ctx, left)} AND (${expression(ctx, ol)} OR ${expression(ctx, or)})"
    case ir.And(left, right) => code"${expression(ctx, left)} AND ${expression(ctx, right)}"
  }

  private def orPredicate(ctx: GeneratorContext, a: ir.Or): SQL = a match {
    case ir.Or(ir.And(ol, or), right) =>
      code"(${expression(ctx, ol)} AND ${expression(ctx, or)}) OR ${expression(ctx, right)}"
    case ir.Or(left, ir.And(ol, or)) =>
      code"${expression(ctx, left)} OR (${expression(ctx, ol)} AND ${expression(ctx, or)})"
    case ir.Or(left, right) => code"${expression(ctx, left)} OR ${expression(ctx, right)}"
  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): SQL =
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

  private def arrayExpr(ctx: GeneratorContext, a: ir.ArrayExpr): SQL = {
    val elementsStr = commas(ctx, a.children)
    code"ARRAY($elementsStr)"
  }

  private def mapExpr(ctx: GeneratorContext, m: ir.MapExpr): SQL = {
    val entriesStr = m.map
      .map { case (key, value) =>
        code"${expression(ctx, key)}, ${expression(ctx, value)}"
      }
      .toSeq
      .mkCode(", ")
    code"MAP($entriesStr)"
  }

  private def id(ctx: GeneratorContext, id: ir.Id): SQL = id match {
    case ir.Id(name, true) => code"`$name`"
    case ir.Id(name, false) => lift(OkResult(name))
  }

  private def alias(ctx: GeneratorContext, alias: ir.Alias): SQL = {
    code"${expression(ctx, alias.expr)} AS ${expression(ctx, alias.name)}"
  }

  private def distinct(ctx: GeneratorContext, distinct: ir.Distinct): SQL = {
    code"DISTINCT ${expression(ctx, distinct.expression)}"
  }

  private def star(ctx: GeneratorContext, star: ir.Star): SQL = {
    val objectRef = star.objectName.map(or => code"${generateObjectReference(ctx, or)}.").getOrElse(code"")
    code"$objectRef*"
  }

  private def generateObjectReference(ctx: GeneratorContext, reference: ir.ObjectReference): SQL = {
    (reference.head +: reference.tail).map(id(ctx, _)).mkCode(".")
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
    code"$prettyName($e AS $dt)"
  }

  private def dot(ctx: GeneratorContext, dot: ir.Dot): SQL = {
    code"${expression(ctx, dot.left)}.${expression(ctx, dot.right)}"
  }

  private def objectReference(ctx: GeneratorContext, objRef: ir.ObjectReference): SQL = {
    (objRef.head +: objRef.tail).map(id(ctx, _)).mkCode(".")
  }

  private def caseWhen(ctx: GeneratorContext, c: ir.Case): SQL = {
    val expr = c.expression.map(expression(ctx, _)).toSeq
    val branches = c.branches.map { branch =>
      code"WHEN ${expression(ctx, branch.condition)} THEN ${expression(ctx, branch.expression)}"
    }
    val otherwise = c.otherwise.map { o => code"ELSE ${expression(ctx, o)}" }.toSeq
    val chunks = expr ++ branches ++ otherwise
    chunks.mkCode("CASE ", " ", " END")
  }

  private def in(ctx: GeneratorContext, inExpr: ir.In): SQL = {
    val values = commas(ctx, inExpr.other)
    code"${expression(ctx, inExpr.left)} IN ($values)"
  }

  private def scalarSubquery(ctx: GeneratorContext, subquery: ir.ScalarSubquery): SQL = {
    ctx.logical.generate(ctx, subquery.relation)
  }

  private def window(ctx: GeneratorContext, window: ir.Window): SQL = {
    val expr = expression(ctx, window.window_function)
    val partition = if (window.partition_spec.isEmpty) { code"" }
    else { window.partition_spec.map(expression(ctx, _)).mkCode("PARTITION BY ", ", ", "") }
    val orderBy = if (window.sort_order.isEmpty) { code"" }
    else { window.sort_order.map(sortOrder(ctx, _)).mkCode(" ORDER BY ", ", ", "") }
    val windowFrame = window.frame_spec
      .map { frame =>
        val mode = frame.frame_type match {
          case ir.RowsFrame => "ROWS"
          case ir.RangeFrame => "RANGE"
        }
        val boundaries = frameBoundary(ctx, frame.lower) ++ frameBoundary(ctx, frame.upper)
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

  private def frameBoundary(ctx: GeneratorContext, boundary: ir.FrameBoundary): Seq[SQL] = boundary match {
    case ir.NoBoundary => Seq.empty
    case ir.CurrentRow => Seq(code"CURRENT ROW")
    case ir.UnboundedPreceding => Seq(code"UNBOUNDED PRECEDING")
    case ir.UnboundedFollowing => Seq(code"UNBOUNDED FOLLOWING")
    case ir.PrecedingN(n) => Seq(code"${expression(ctx, n)} PRECEDING")
    case ir.FollowingN(n) => Seq(code"${expression(ctx, n)} FOLLOWING")
  }

  private def sortOrder(ctx: GeneratorContext, order: ir.SortOrder): SQL = {
    val orderBy = expression(ctx, order.child)
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

  private def regexpExtract(ctx: GeneratorContext, extract: ir.RegExpExtract): SQL = {
    val c = if (extract.c == ir.Literal(1)) { code"" }
    else { code", ${expression(ctx, extract.c)}" }
    code"${extract.prettyName}(${expression(ctx, extract.left)}, ${expression(ctx, extract.right)}$c)"
  }

  private def arrayAccess(ctx: GeneratorContext, access: ir.ArrayAccess): SQL = {
    code"${expression(ctx, access.array)}[${expression(ctx, access.index)}]"
  }

  private def timestampDiff(ctx: GeneratorContext, diff: ir.TimestampDiff): SQL = {
    code"${diff.prettyName}(${diff.unit}, ${expression(ctx, diff.start)}, ${expression(ctx, diff.end)})"
  }

  private def timestampAdd(ctx: GeneratorContext, tsAdd: ir.TimestampAdd): SQL = {
    code"${tsAdd.prettyName}(${tsAdd.unit}, ${expression(ctx, tsAdd.quantity)}, ${expression(ctx, tsAdd.timestamp)})"
  }

  private def extract(ctx: GeneratorContext, e: ir.Extract): SQL = {
    code"EXTRACT(${expression(ctx, e.left)} FROM ${expression(ctx, e.right)})"
  }

  private def lambdaFunction(ctx: GeneratorContext, l: ir.LambdaFunction): SQL = {
    val parameterList = l.arguments.map(lambdaArgument)
    val parameters = if (parameterList.size > 1) { parameterList.mkCode("(", ", ", ")") }
    else { parameterList.mkCode }
    val body = expression(ctx, l.function)
    code"$parameters -> $body"
  }

  private def lambdaArgument(arg: ir.UnresolvedNamedLambdaVariable): SQL = {
    lift(OkResult(arg.name_parts.mkString(".")))
  }

  private def variable(ctx: GeneratorContext, v: ir.Variable): SQL = code"$${${v.name}}"

  private def concat(ctx: GeneratorContext, c: ir.Concat): SQL = {
    val args = c.children.map(expression(ctx, _))
    if (c.children.size > 2) {
      args.mkCode(" || ")
    } else {
      args.mkCode("CONCAT(", ", ", ")")
    }
  }

  private def schemaReference(ctx: GeneratorContext, s: ir.SchemaReference): SQL = {
    val ref = s.columnName match {
      case d: ir.Dot => expression(ctx, d)
      case i: ir.Id => expression(ctx, i)
      case _ => code"JSON_COLUMN"
    }
    code"{${ref.map(_.toUpperCase(Locale.getDefault()))}_SCHEMA}"
  }
  private def singleQuote(s: String): SQL = code"'$s'"
  private def isValidIdentifier(s: String): Boolean =
    (s.head.isLetter || s.head == '_') && s.forall(x => x.isLetterOrDigit || x == '_')

  private def between(ctx: GeneratorContext, b: ir.Between): SQL = {
    code"${expression(ctx, b.exp)} BETWEEN ${expression(ctx, b.lower)} AND ${expression(ctx, b.upper)}"
  }

}
