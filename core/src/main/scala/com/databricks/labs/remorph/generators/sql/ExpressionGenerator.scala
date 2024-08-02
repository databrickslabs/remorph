package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.{Generator, GeneratorContext}
import com.databricks.labs.remorph.parsers.intermediate.RLike
import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

import java.time._
import java.time.format.DateTimeFormatter
import java.util.Locale

class ExpressionGenerator(val callMapper: ir.CallMapper = new ir.CallMapper())
    extends Generator[ir.Expression, String] {
  private val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS").withZone(ZoneId.of("UTC"))

  override def generate(ctx: GeneratorContext, tree: ir.Expression): String = expression(ctx, tree)

  def expression(ctx: GeneratorContext, expr: ir.Expression): String = {
    expr match {
      case l: ir.Like => like(ctx, l)
      case r: ir.RLike => rlike(ctx, r)
      case _: ir.Bitwise => bitwise(ctx, expr)
      case _: ir.Arithmetic => arithmetic(ctx, expr)
      case _: ir.Predicate => predicate(ctx, expr)
      case l: ir.Literal => literal(ctx, l)
      case fn: ir.Fn => callFunction(ctx, fn)
      case ir.UnresolvedAttribute(name, _, _) => name
      case d: ir.Dot => dot(ctx, d)
      case i: ir.Id => id(ctx, i)
      case o: ir.ObjectReference => objectReference(ctx, o)
      case a: ir.Alias => alias(ctx, a)
      case d: ir.Distinct => distinct(ctx, d)
      case s: ir.Star => star(ctx, s)
      case c: ir.Cast => cast(ctx, c)
      case col: ir.Column => column(ctx, col)
      case da: ir.DeleteAction => "DELETE"
      case ia: ir.InsertAction => insertAction(ctx, ia)
      case ua: ir.UpdateAction => updateAction(ctx, ua)
      case a: ir.Assign => assign(ctx, a)
      case opts: ir.Options => options(ctx, opts)

      case x => throw TranspileException(s"Unsupported expression: $x")
    }
  }

  private def options(ctx: GeneratorContext, opts: ir.Options): String = {
    // First gather the options that are set by expressions
    val exprOptions = opts.expressionOpts.map { case (key, expression) =>
      s"     ${key} = ${generate(ctx, expression)}\n"
    }.mkString
    val exprStr = if (exprOptions.nonEmpty) {
      s"    Expression options:\n\n${exprOptions}\n"
    } else {
      ""
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
    val optString = s"${exprStr}${stringStr}${boolStr}${autoStr}"
    if (optString.nonEmpty) {
      s"/*\n   The following statement was originally given the following OPTIONS:\n\n${optString}\n */\n"
    } else {
      ""
    }
  }

  private def assign(ctx: GeneratorContext, assign: ir.Assign): String = {
    s"${expression(ctx, assign.left)} = ${expression(ctx, assign.right)}"
  }

  private def column(ctx: GeneratorContext, column: ir.Column): String = {
    val objectRef = column.tableNameOrAlias.map(or => generateObjectReference(ctx, or) + ".").getOrElse("")
    s"$objectRef${id(ctx, column.columnName)}"
  }

  private def insertAction(ctx: GeneratorContext, insertAction: ir.InsertAction): String = {
    val (cols, values) = insertAction.assignments.map { assign =>
      (generate(ctx, assign.left), generate(ctx, assign.right))
    }.unzip
    s"INSERT (${cols.mkString(", ")}) VALUES (${values.mkString(", ")})"
  }

  private def updateAction(ctx: GeneratorContext, updateAction: ir.UpdateAction): String = {
    s"UPDATE SET ${updateAction.assignments.map(assign => generate(ctx, assign)).mkString(", ")}"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): String = expr match {
    case ir.UMinus(child) => s"-${expression(ctx, child)}"
    case ir.UPlus(child) => s"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => s"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => s"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => s"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => s"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => s"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  private def bitwise(ctx: GeneratorContext, expr: ir.Expression): String = expr match {
    case ir.BitwiseOr(left, right) => s"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => s"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.BitwiseXor(left, right) => s"${expression(ctx, left)} ^ ${expression(ctx, right)}"
    case ir.BitwiseNot(child) => s"~${expression(ctx, child)}"
  }

  private def like(ctx: GeneratorContext, like: ir.Like): String = {
    val escape = if (like.escapeChar != '\\') s" ESCAPE '${like.escapeChar}'" else ""
    s"${expression(ctx, like.left)} LIKE ${expression(ctx, like.right)}$escape"
  }

  private def rlike(ctx: GeneratorContext, r: RLike): String = {
    s"${expression(ctx, r.left)} RLIKE ${expression(ctx, r.right)}"
  }

  private def predicate(ctx: GeneratorContext, expr: ir.Expression): String = expr match {
    case ir.And(left, right) => s"(${expression(ctx, left)} AND ${expression(ctx, right)})"
    case ir.Or(left, right) => s"(${expression(ctx, left)} OR ${expression(ctx, right)})"
    case ir.Not(child) => s"NOT (${expression(ctx, child)})"
    case ir.Equals(left, right) => s"${expression(ctx, left)} = ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => s"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => s"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => s"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => s"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => s"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => throw new IllegalArgumentException(s"Unsupported expression: $expr")
  }

  private def callFunction(ctx: GeneratorContext, fn: ir.Fn): String = {
    val call = callMapper.convert(fn)
    call match {
      case r: RLike => rlike(ctx, r)
      case fn: ir.Fn => s"${fn.prettyName}(${fn.children.map(expression(ctx, _)).mkString(", ")})"
      case _ => throw TranspileException("not implemented")
    }

  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): String = {
    l.dataType match {
      case ir.NullType => "NULL"
      case ir.BinaryType => orNull(l.binary.map(_.map("%02X" format _).mkString))
      case ir.BooleanType => orNull(l.boolean.map(_.toString.toUpperCase(Locale.getDefault)))
      case ir.ShortType => orNull(l.short.map(_.toString))
      case ir.IntegerType => orNull(l.integer.map(_.toString))
      case ir.LongType => orNull(l.long.map(_.toString))
      case ir.FloatType => orNull(l.float.map(_.toString))
      case ir.DoubleType => orNull(l.double.map(_.toString))
      case ir.StringType => orNull(l.string.map(singleQuote))
      case ir.DateType => dateLiteral(l)
      case ir.TimestampType => timestampLiteral(l)
      case ir.ArrayType(_) => orNull(l.array.map(arrayExpr(ctx)))
      case ir.MapType(_, _) => orNull(l.map.map(mapExpr(ctx)))
      case _ => throw new IllegalArgumentException(s"Unsupported expression: ${l.dataType}")
    }
  }

  private def timestampLiteral(l: ir.Literal) = {
    l.timestamp match {
      case Some(timestamp) =>
        singleQuote(
          LocalDateTime
            .from(ZonedDateTime.ofInstant(Instant.ofEpochMilli(timestamp), ZoneId.of("UTC")))
            .format(timeFormat))
      case None => "NULL"
    }
  }

  private def dateLiteral(l: ir.Literal) = {
    l.date match {
      case Some(date) =>
        singleQuote(
          LocalDate.from(ZonedDateTime.ofInstant(Instant.ofEpochMilli(date), ZoneId.of("UTC"))).format(dateFormat))
      case None => "NULL"
    }
  }

  private def mapExpr(ctx: GeneratorContext)(map: ir.MapExpr): String = {
    val entries = map.keys.zip(map.values).map { case (key, value) =>
      s"${literal(ctx, key)}, ${expression(ctx, value)}"
    }
    // TODO: line-width formatting
    s"MAP(${entries.mkString(", ")})"
  }

  private def arrayExpr(ctx: GeneratorContext)(array: ir.ArrayExpr): String = {
    val elements = array.elements.map { element =>
      expression(ctx, element)
    }
    // TODO: line-width formatting
    s"ARRAY(${elements.mkString(", ")})"
  }

  private def id(ctx: GeneratorContext, id: ir.Id): String = {
    if (id.caseSensitive) {
      doubleQuote(id.id)
    } else {
      id.id
    }
  }

  private def alias(ctx: GeneratorContext, alias: ir.Alias): String = {
    s"${expression(ctx, alias.expr)} AS ${alias.name.map(expression(ctx, _)).mkString(".")}"
  }

  private def distinct(ctx: GeneratorContext, distinct: ir.Distinct): String = {
    s"DISTINCT ${expression(ctx, distinct.expression)}"
  }

  private def star(ctx: GeneratorContext, star: ir.Star): String = {
    val objectRef = star.objectName.map(or => generateObjectReference(ctx, or) + ".").getOrElse("")
    s"$objectRef*"
  }

  private def generateObjectReference(ctx: GeneratorContext, reference: ir.ObjectReference): String = {
    (reference.head +: reference.tail).map(id(ctx, _)).mkString(".")
  }

  private def cast(ctx: GeneratorContext, cast: ir.Cast): String = {
    val expr = expression(ctx, cast.expr)
    val dataType = DataTypeGenerator.generateDataType(ctx, cast.dataType)
    s"CAST($expr AS $dataType)"
  }

  private def dot(ctx: GeneratorContext, dot: ir.Dot): String = {
    s"${expression(ctx, dot.left)}.${expression(ctx, dot.right)}"
  }

  private def objectReference(ctx: GeneratorContext, objRef: ir.ObjectReference): String = {
    (objRef.head +: objRef.tail).map(id(ctx, _)).mkString(".")
  }

  private def orNull(option: Option[String]): String = option.getOrElse("NULL")

  private def doubleQuote(s: String): String = s""""$s""""

  private def singleQuote(s: String): String = s"'$s'"
}
