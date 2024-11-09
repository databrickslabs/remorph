package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

import java.time.format.DateTimeFormatter
import java.time.{Instant, LocalDate, LocalDateTime, ZoneId, ZonedDateTime}
import java.util.Locale

// F.expr(...)
case class RawExpr(expr: ir.Expression) extends ir.LeafExpression {
  override def dataType: ir.DataType = ir.UnresolvedType
}

class PySparkExpressions extends ir.Rule[ir.Expression] with PyCommon {
  private val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC"))

  override def apply(expr: ir.Expression): ir.Expression = expr transformUp {
    case _: ir.Bitwise => bitwise(expr)
    case ir.Like(col, pattern, escape) => methodOf(col, "like", Seq(pattern) ++ escape)
    case ir.RLike(col, pattern) => methodOf(col, "rlike", Seq(pattern))
    case ir.Between(exp, lower, upper) => methodOf(exp, "between", Seq(lower, upper))
    case ir.Literal(epochDay: Long, ir.DateType) => dateLiteral(epochDay)
    case ir.Literal(epochSecond: Long, ir.TimestampType) => timestampLiteral(epochSecond)
    case ir.ArrayExpr(children, _) => F("array", children)
    case ir.IsNull(col) => methodOf(col, "isNull", Seq())
    case ir.IsNotNull(col) => methodOf(col, "isNotNull", Seq())
    case ir.UnresolvedAttribute(name, _, _, _, _, _, _) => F("col", ir.StringLiteral(name) :: Nil)
    case ir.Id(name, _) => F("col", ir.StringLiteral(name) :: Nil)
    case ir.Alias(child, ir.Id(name, _)) => methodOf(child, "alias", Seq(ir.StringLiteral(name)))
    case o: ir.SortOrder => sortOrder(o)
    case _: ir.Star => F("col", ir.StringLiteral("*") :: Nil)
    case i: ir.KnownInterval => RawExpr(i)
    case ir.Case(None, branches, otherwise) => caseWhenBranches(branches, otherwise)
    case w: ir.Window => window(w)
    // case ir.Exists(subquery) => F("exists", Seq(py.Lambda(py.Arguments(args = Seq(ir.Name("col"))), subquery)))
    // case l: ir.LambdaFunction => py.Lambda(py.Arguments(args = Seq(ir.Name("col"))), apply(l.body))
    case ir.ArrayAccess(array, index) => py.Subscript(apply(array), apply(index))
    case ir.Variable(name) => ir.Name(name)
    case ir.Extract(field, child) => F("extract", Seq(apply(field), apply(child)))
    case ir.Concat(children) => F("concat", children)
    case ir.ConcatWs(children) => F("concat_ws", children)
    case ir.In(value, list) => methodOf(value, "isin", list)
    case fn: ir.Fn => F(fn.prettyName.toLowerCase(Locale.getDefault), fn.children.map(apply))
  }

  private def sortOrder(order: ir.SortOrder): ir.Expression = order match {
    case ir.SortOrder(col, ir.Ascending, ir.NullsFirst) => methodOf(apply(col), "asc_nulls_first", Seq())
    case ir.SortOrder(col, ir.Ascending, ir.NullsLast) => methodOf(apply(col), "asc_nulls_last", Seq())
    case ir.SortOrder(col, ir.Ascending, _) => methodOf(apply(col), "asc", Seq())
    case ir.SortOrder(col, ir.Descending, ir.NullsFirst) => methodOf(apply(col), "desc_nulls_first", Seq())
    case ir.SortOrder(col, ir.Descending, ir.NullsLast) => methodOf(apply(col), "desc_nulls_last", Seq())
    case ir.SortOrder(col, ir.Descending, _) => methodOf(apply(col), "desc", Seq())
    case ir.SortOrder(col, _, _) => apply(col)
  }

  private def window(w: ir.Window): ir.Expression = {
    var windowSpec: ir.Expression = ir.Name("Window")
    windowSpec = w.partition_spec match {
      case Nil => windowSpec
      case _ => methodOf(windowSpec, "partitionBy", w.partition_spec.map(apply))
    }
    windowSpec = w.sort_order match {
      case Nil => windowSpec
      case _ => methodOf(windowSpec, "orderBy", w.sort_order.map(apply))
    }
    windowSpec = w.frame_spec match {
      case None => windowSpec
      case Some(value) => windowFrame(windowSpec, value)
    }
    windowSpec = ImportClassSideEffect(windowSpec, module = "pyspark.sql.window", klass = "Window")
    val fn = apply(w.window_function)
    methodOf(fn, "over", Seq(windowSpec))
  }

  private def windowFrame(windowSpec: ir.Expression, frame: ir.WindowFrame): ir.Expression = frame match {
    case ir.WindowFrame(ir.RangeFrame, left, right) =>
      methodOf(windowSpec, "rangeBetween", Seq(frameBoundary(left), frameBoundary(right)))
    case ir.WindowFrame(ir.RowsFrame, left, right) =>
      methodOf(windowSpec, "rowsBetween", Seq(frameBoundary(left), frameBoundary(right)))
    case _ => windowSpec
  }

  private def frameBoundary(boundary: ir.FrameBoundary): ir.Expression = boundary match {
    case ir.CurrentRow => py.Attribute(ir.Name("Window"), ir.Name("currentRow"))
    case ir.UnboundedPreceding => py.Attribute(ir.Name("Window"), ir.Name("unboundedPreceding"))
    case ir.UnboundedFollowing => py.Attribute(ir.Name("Window"), ir.Name("unboundedFollowing"))
    case ir.PrecedingN(n) => n
    case ir.FollowingN(n) => n
    case ir.NoBoundary => ir.Name("noBoundary")
  }

  private def caseWhenBranches(branches: Seq[ir.WhenBranch], otherwise: Option[ir.Expression]) = {
    val when = F("when", Seq(apply(branches.head.condition), apply(branches.head.expression)))
    val body = branches.foldLeft(when) { case (acc, branch) =>
      methodOf(acc, "when", Seq(apply(branch.condition), apply(branch.expression)))
    }
    otherwise match {
      case Some(value) => methodOf(body, "otherwise", Seq(apply(value)))
      case None => body
    }
  }

  private def dateLiteral(epochDay: Long): ir.Expression = {
    val raw = ir.StringLiteral(LocalDate.ofEpochDay(epochDay).format(dateFormat))
    methodOf(F("lit", Seq(raw)), "cast", Seq(ir.StringLiteral("date")))
  }

  private def timestampLiteral(epochSecond: Long): ir.Expression = {
    val raw = ir.StringLiteral(
      LocalDateTime
        .from(ZonedDateTime.ofInstant(Instant.ofEpochSecond(epochSecond), ZoneId.of("UTC")))
        .format(timeFormat))
    methodOf(F("lit", Seq(raw)), "cast", Seq(ir.StringLiteral("timestamp")))
  }

  private def bitwise(expr: ir.Expression): ir.Expression = expr match {
    case ir.BitwiseOr(left, right) => methodOf(left, "bitwiseOR", Seq(right))
    case ir.BitwiseAnd(left, right) => methodOf(left, "bitwiseAND", Seq(right))
    case ir.BitwiseXor(left, right) => methodOf(left, "bitwiseXOR", Seq(right))
    case ir.BitwiseNot(child) => ir.Not(child)
  }
}
