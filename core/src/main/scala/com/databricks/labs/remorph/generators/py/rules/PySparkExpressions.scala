package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{Transformation, TransformationConstructors, intermediate => ir}
import com.databricks.labs.remorph.generators.py

import java.time.format.DateTimeFormatter
import java.time.{Instant, LocalDate, LocalDateTime, ZoneId, ZonedDateTime}
import java.util.Locale

// F.expr(...)
case class RawExpr(expr: ir.Expression) extends ir.LeafExpression {
  override def dataType: ir.DataType = ir.UnresolvedType
}

class PySparkExpressions extends ir.Rule[ir.Expression] with PyCommon with TransformationConstructors {
  private[this] val dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd")
  private[this] val timeFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.of("UTC"))

  override def apply(expr: ir.Expression): Transformation[ir.Expression] = expr transformUp {
    case _: ir.Bitwise => ok(bitwise(expr))
    case ir.Like(col, pattern, escape) => ok(methodOf(col, "like", Seq(pattern) ++ escape))
    case ir.RLike(col, pattern) => ok(methodOf(col, "rlike", Seq(pattern)))
    case ir.Between(exp, lower, upper) => ok(methodOf(exp, "between", Seq(lower, upper)))
    case ir.Literal(epochDay: Long, ir.DateType) => ok(dateLiteral(epochDay))
    case ir.Literal(epochSecond: Long, ir.TimestampType) => ok(timestampLiteral(epochSecond))
    case ir.ArrayExpr(children, _) => ok(F("array", children))
    case ir.IsNull(col) => ok(methodOf(col, "isNull", Seq()))
    case ir.IsNotNull(col) => ok(methodOf(col, "isNotNull", Seq()))
    case ir.UnresolvedAttribute(name, _, _, _, _, _, _) => ok(F("col", ir.StringLiteral(name) :: Nil))
    case ir.Id(name, _) => ok(F("col", ir.StringLiteral(name) :: Nil))
    case ir.Alias(child, ir.Id(name, _)) => ok(methodOf(child, "alias", Seq(ir.StringLiteral(name))))
    case o: ir.SortOrder => sortOrder(o)
    case _: ir.Star => ok(F("col", ir.StringLiteral("*") :: Nil))
    case i: ir.KnownInterval => ok(RawExpr(i))
    case ir.Case(None, branches, otherwise) => caseWhenBranches(branches, otherwise)
    case w: ir.Window => window(w)
    // case ir.Exists(subquery) => F("exists", Seq(py.Lambda(py.Arguments(args = Seq(ir.Name("col"))), subquery)))
    // case l: ir.LambdaFunction => py.Lambda(py.Arguments(args = Seq(ir.Name("col"))), apply(l.body))
    case ir.ArrayAccess(array, index) => apply(array).flatMap { a => apply(index).map(i => py.Subscript(a, i)) }
    case ir.Variable(name) => ok(ir.Name(name))
    case ir.Extract(field, child) => Seq(field, child).map(apply).sequence.map(F("extract", _))
    case ir.Concat(children) => ok(F("concat", children))
    case ir.ConcatWs(children) => ok(F("concat_ws", children))
    case ir.In(value, list) => ok(methodOf(value, "isin", list))
    case fn: ir.Fn => fn.children.map(apply).sequence.map(F(fn.prettyName.toLowerCase(Locale.getDefault), _))
  }

  private def sortOrder(order: ir.SortOrder): Transformation[ir.Expression] = order match {
    case ir.SortOrder(col, ir.Ascending, ir.NullsFirst) => apply(col).map(methodOf(_, "asc_nulls_first", Seq()))
    case ir.SortOrder(col, ir.Ascending, ir.NullsLast) => apply(col).map(methodOf(_, "asc_nulls_last", Seq()))
    case ir.SortOrder(col, ir.Ascending, _) => apply(col).map(methodOf(_, "asc", Seq()))
    case ir.SortOrder(col, ir.Descending, ir.NullsFirst) => apply(col).map(methodOf(_, "desc_nulls_first", Seq()))
    case ir.SortOrder(col, ir.Descending, ir.NullsLast) => apply(col).map(methodOf(_, "desc_nulls_last", Seq()))
    case ir.SortOrder(col, ir.Descending, _) => apply(col).map(methodOf(_, "desc", Seq()))
    case ir.SortOrder(col, _, _) => apply(col)
  }

  private def window(w: ir.Window): Transformation[ir.Expression] = {
    (w.partition_spec match {
      case Nil => ok(ir.Name("Window"))
      case _ => w.partition_spec.map(apply).sequence.map(methodOf(ir.Name("Window"), "partitionBy", _))
    }).flatMap { windowSpec =>
      w.sort_order match {
        case Nil => ok(windowSpec)
        case _ => w.sort_order.map(apply).sequence.map(methodOf(windowSpec, "orderBy", _))
      }
    }.map { withOrder =>
      w.frame_spec match {
        case None => withOrder
        case Some(value) => windowFrame(withOrder, value)
      }
    }.flatMap { window =>
      apply(w.window_function).map { fn =>
        val importClassSideEffect = ImportClassSideEffect(window, module = "pyspark.sql.window", klass = "Window")
        methodOf(fn, "over", Seq(importClassSideEffect))
      }
    }

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

  private def caseWhenBranches(
      branches: Seq[ir.WhenBranch],
      otherwise: Option[ir.Expression]): Transformation[ir.Expression] = {
    val when = Seq(apply(branches.head.condition), apply(branches.head.expression)).sequence.map(F("when", _))
    val body = branches.foldLeft(when) { case (acc, branch) =>
      acc.flatMap { a =>
        Seq(apply(branch.condition), apply(branch.expression)).sequence.map(methodOf(a, "when", _))
      }
    }
    otherwise match {
      case Some(value) => body.flatMap(b => apply(value).map(v => methodOf(b, "otherwise", Seq(v))))
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
