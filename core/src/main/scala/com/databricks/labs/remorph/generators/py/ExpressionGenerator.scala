package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{intermediate => ir}

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {
  override def generate(ctx: GeneratorContext, tree: Expression): Python = expression(ctx, tree)

  private def expression(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.Name(name) => tba"$name"
    case _: ir.Arithmetic => arithmetic(ctx, expr)
    case _: ir.Predicate => predicate(ctx, expr)
    case l: ir.Literal => literal(ctx, l)
    case c: Call => call(ctx, c)
    case d: Dict => dict(ctx, d)
    case s: Slice => slice(ctx, s)
    case Comprehension(target, iter, ifs) => comprehension(ctx, target, iter, ifs)
    case GeneratorExp(elt, gens) => tba"${expression(ctx, elt)} ${spaces(ctx, gens)}"
    case ListComp(elt, gens) => tba"[${expression(ctx, elt)} ${spaces(ctx, gens)}]"
    case SetComp(elt, gens) => tba"{${expression(ctx, elt)} ${spaces(ctx, gens)}}"
    case DictComp(key, value, gens) => tba"{${generate(ctx, key)}: ${generate(ctx, value)} ${spaces(ctx, gens)}}"
    case IfExp(test, body, orElse) => ifExpr(ctx, test, body, orElse)
    case Lambda(args, body) => tba"lambda ${arguments(ctx, args)}: ${expression(ctx, body)}"
    case Tuple(elements, _) => tba"(${commas(ctx, elements)},)"
    case Attribute(value, attr, _) => tba"${expression(ctx, value)}.${expression(ctx, attr)}"
    case Subscript(value, index, _) => tba"${expression(ctx, value)}[${expression(ctx, index)}]"
    case List(elements, _) => tba"[${commas(ctx, elements)}]"
    case Set(Nil) => tba"set()"
    case Set(elements) => tba"{${commas(ctx, elements)}}"
    case _ => partialResult(expr)
  }

  def spaces(ctx: GeneratorContext, expressions: Seq[ir.Expression]): Python = {
    expressions.map(expression(ctx, _)).mkTba(" ")
  }

  private def comprehension(
      ctx: GeneratorContext,
      target: Expression,
      iter: Expression,
      ifs: Seq[Expression]): Python = {
    val ifsExpr = ifs.map(expression(ctx, _)).mkTba(" and ")
    val base = tba"for ${expression(ctx, target)} in ${expression(ctx, iter)}"
    ifsExpr.isEmpty.flatMap { isEmpty =>
      if (isEmpty) {
        base
      } else {
        tba"$base if $ifsExpr"
      }
    }
  }

  private def ifExpr(ctx: GeneratorContext, test: Expression, body: Expression, orelse: Expression): Python = {
    tba"${expression(ctx, body)} if ${expression(ctx, test)} else ${expression(ctx, orelse)}"
  }

  def arguments(ctx: GeneratorContext, arguments: Arguments): Python = {
    // TODO: add support for defaults
    val positional = arguments.args match {
      case Nil => None
      case some => Some(commas(ctx, some))
    }
    val args = arguments.vararg map { case ir.Name(name) => tba"*$name" }
    val kwargs = arguments.kwargs map { case ir.Name(name) => tba"**$name" }
    val argumentLists = Seq(positional, args, kwargs).filter(_.nonEmpty).map(_.get)
    argumentLists.mkTba(", ")
  }

  private def slice(ctx: GeneratorContext, s: Slice): Python = s match {
    case Slice(None, None, None) => tba":"
    case Slice(Some(lower), None, None) => tba"${expression(ctx, lower)}:"
    case Slice(None, Some(upper), None) => tba":${expression(ctx, upper)}"
    case Slice(Some(lower), Some(upper), None) => tba"${expression(ctx, lower)}:${expression(ctx, upper)}"
    case Slice(None, None, Some(step)) => tba"::${expression(ctx, step)}"
    case Slice(Some(lower), None, Some(step)) => tba"${expression(ctx, lower)}::${expression(ctx, step)}"
    case Slice(None, Some(upper), Some(step)) => tba":${expression(ctx, upper)}:${expression(ctx, step)}"
    case Slice(Some(lower), Some(upper), Some(step)) =>
      tba"${expression(ctx, lower)}:${expression(ctx, upper)}:${expression(ctx, step)}"
  }

  private def dict(ctx: GeneratorContext, d: Dict): Python = {
    d.keys.zip(d.values).map { case (k, v) =>
      tba"${expression(ctx, k)}: ${expression(ctx, v)}"
    } mkTba ("{", ", ", "}")
  }

  private def call(ctx: GeneratorContext, c: Call): Python = {
    val args = c.args.map(expression(ctx, _))
    val kwargs = c.keywords.map { case Keyword(k, v) => tba"${expression(ctx, k)}=${expression(ctx, v)}" }
    tba"${expression(ctx, c.func)}(${(args ++ kwargs).mkTba(", ")})"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.UMinus(child) => tba"-${expression(ctx, child)}"
    case ir.UPlus(child) => tba"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => tba"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => tba"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => tba"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => tba"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => tba"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  // see com.databricks.labs.remorph.generators.py.rules.AndOrToBitwise
  private def predicate(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.BitwiseOr(left, right) => tba"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => tba"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.And(left, right) => tba"${expression(ctx, left)} and ${expression(ctx, right)}"
    case ir.Or(left, right) => tba"${expression(ctx, left)} or ${expression(ctx, right)}"
    case ir.Not(child) => tba"~(${expression(ctx, child)})"
    case ir.Equals(left, right) => tba"${expression(ctx, left)} == ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => tba"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => tba"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => tba"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => tba"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => tba"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => partialResult(expr)
  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): Python = l match {
    case ir.Literal(_, ir.NullType) => tba"None"
    case ir.Literal(bytes: Array[Byte], ir.BinaryType) => ok(bytes.map("%02X" format _).mkString)
    case ir.Literal(true, ir.BooleanType) => tba"True"
    case ir.Literal(false, ir.BooleanType) => tba"False"
    case ir.Literal(value, ir.ShortType) => ok(value.toString)
    case ir.IntLiteral(value) => ok(value.toString)
    case ir.Literal(value, ir.LongType) => ok(value.toString)
    case ir.FloatLiteral(value) => ok(value.toString)
    case ir.DoubleLiteral(value) => ok(value.toString)
    case ir.DecimalLiteral(value) => ok(value.toString)
    case ir.Literal(value: String, ir.StringType) => singleQuote(value)
    case _ => partialResult(l, ir.UnsupportedDataType(l.dataType.toString))
  }

  private def singleQuote(s: String): Python = tba"'$s'"
}
