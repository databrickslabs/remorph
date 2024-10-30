package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{intermediate => ir}

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {
  override def generate(ctx: GeneratorContext, tree: Expression): Python = expression(ctx, tree)

  private def expression(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.Name(name) => code"$name"
    case _: ir.Arithmetic => arithmetic(ctx, expr)
    case _: ir.Predicate => predicate(ctx, expr)
    case l: ir.Literal => literal(ctx, l)
    case c: Call => call(ctx, c)
    case d: Dict => dict(ctx, d)
    case s: Slice => slice(ctx, s)
    case Comprehension(target, iter, ifs) => comprehension(ctx, target, iter, ifs)
    case GeneratorExp(elt, gens) => code"${expression(ctx, elt)} ${spaces(ctx, gens)}"
    case ListComp(elt, gens) => code"[${expression(ctx, elt)} ${spaces(ctx, gens)}]"
    case SetComp(elt, gens) => code"{${expression(ctx, elt)} ${spaces(ctx, gens)}}"
    case DictComp(key, value, gens) => code"{${generate(ctx, key)}: ${generate(ctx, value)} ${spaces(ctx, gens)}}"
    case IfExp(test, body, orElse) => ifExpr(ctx, test, body, orElse)
    case Lambda(args, body) => code"lambda ${arguments(ctx, args)}: ${expression(ctx, body)}"
    case Tuple(elements, _) => code"(${commas(ctx, elements)},)"
    case Attribute(value, attr, _) => code"${expression(ctx, value)}.${expression(ctx, attr)}"
    case Subscript(value, index, _) => code"${expression(ctx, value)}[${expression(ctx, index)}]"
    case List(elements, _) => code"[${commas(ctx, elements)}]"
    case Set(Nil) => code"set()"
    case Set(elements) => code"{${commas(ctx, elements)}}"
    case _ => partialResult(expr)
  }

  private def comprehension(
      ctx: GeneratorContext,
      target: Expression,
      iter: Expression,
      ifs: Seq[Expression]): Python = {
    val ifsExpr = ifs.map(expression(ctx, _)).mkCode(" and ")
    val base = code"for ${expression(ctx, target)} in ${expression(ctx, iter)}"
    ifsExpr.isEmpty.flatMap { isEmpty =>
      if (isEmpty) {
        base
      } else {
        code"$base if $ifsExpr"
      }
    }
  }

  private def ifExpr(ctx: GeneratorContext, test: Expression, body: Expression, orelse: Expression): Python = {
    code"${expression(ctx, body)} if ${expression(ctx, test)} else ${expression(ctx, orelse)}"
  }

  def arguments(ctx: GeneratorContext, arguments: Arguments): Python = {
    // TODO: add support for defaults
    val positional = arguments.args match {
      case Nil => None
      case some => Some(commas(ctx, some))
    }
    val args = arguments.vararg map { case ir.Name(name) => code"*$name" }
    val kwargs = arguments.kwargs map { case ir.Name(name) => code"**$name" }
    val argumentLists = Seq(positional, args, kwargs).filter(_.nonEmpty).map(_.get)
    argumentLists.mkCode(", ")
  }

  private def slice(ctx: GeneratorContext, s: Slice): Python = s match {
    case Slice(None, None, None) => code":"
    case Slice(Some(lower), None, None) => code"${expression(ctx, lower)}:"
    case Slice(None, Some(upper), None) => code":${expression(ctx, upper)}"
    case Slice(Some(lower), Some(upper), None) => code"${expression(ctx, lower)}:${expression(ctx, upper)}"
    case Slice(None, None, Some(step)) => code"::${expression(ctx, step)}"
    case Slice(Some(lower), None, Some(step)) => code"${expression(ctx, lower)}::${expression(ctx, step)}"
    case Slice(None, Some(upper), Some(step)) => code":${expression(ctx, upper)}:${expression(ctx, step)}"
    case Slice(Some(lower), Some(upper), Some(step)) =>
      code"${expression(ctx, lower)}:${expression(ctx, upper)}:${expression(ctx, step)}"
  }

  private def dict(ctx: GeneratorContext, d: Dict): Python = {
    d.keys.zip(d.values).map { case (k, v) =>
      code"${expression(ctx, k)}: ${expression(ctx, v)}"
    } mkCode ("{", ", ", "}")
  }

  private def call(ctx: GeneratorContext, c: Call): Python = {
    val args = c.args.map(expression(ctx, _))
    val kwargs = c.keywords.map { case Keyword(k, v) => code"${expression(ctx, k)}=${expression(ctx, v)}" }
    code"${expression(ctx, c.func)}(${(args ++ kwargs).mkCode(", ")})"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.UMinus(child) => code"-${expression(ctx, child)}"
    case ir.UPlus(child) => code"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => code"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => code"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => code"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => code"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => code"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  // see com.databricks.labs.remorph.generators.py.rules.AndOrToBitwise
  private def predicate(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.BitwiseOr(left, right) => code"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => code"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.And(left, right) => code"${expression(ctx, left)} and ${expression(ctx, right)}"
    case ir.Or(left, right) => code"${expression(ctx, left)} or ${expression(ctx, right)}"
    case ir.Not(child) => code"~(${expression(ctx, child)})"
    case ir.Equals(left, right) => code"${expression(ctx, left)} == ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => code"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => code"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => code"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => code"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => code"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => partialResult(expr)
  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): Python = l match {
    case ir.Literal(_, ir.NullType) => code"None"
    case ir.Literal(bytes: Array[Byte], ir.BinaryType) => ok(bytes.map("%02X" format _).mkString)
    case ir.Literal(true, ir.BooleanType) => code"True"
    case ir.Literal(false, ir.BooleanType) => code"False"
    case ir.Literal(value, ir.ShortType) => ok(value.toString)
    case ir.IntLiteral(value) => ok(value.toString)
    case ir.Literal(value, ir.LongType) => ok(value.toString)
    case ir.FloatLiteral(value) => ok(value.toString)
    case ir.DoubleLiteral(value) => ok(value.toString)
    case ir.DecimalLiteral(value) => ok(value.toString)
    case ir.Literal(value: String, ir.StringType) => singleQuote(value)
    case _ => partialResult(l, ir.UnsupportedDataType(l.dataType.toString))
  }

  private def singleQuote(s: String): Python = code"'$s'"
}
