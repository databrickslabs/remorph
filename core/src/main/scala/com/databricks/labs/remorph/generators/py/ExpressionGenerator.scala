package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{OkResult, intermediate => ir}

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {
  override def generate(ctx: GeneratorContext, tree: Expression): Python = expression(ctx, tree)

  private def expression(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.Name(name) => py"$name"
    case _: ir.Arithmetic => arithmetic(ctx, expr)
    case _: ir.Predicate => predicate(ctx, expr)
    case l: ir.Literal => literal(ctx, l)
    case c: Call => call(ctx, c)
    case d: Dict => dict(ctx, d)
    case s: Slice => slice(ctx, s)
    case Comprehension(target, iter, ifs) => comprehension(ctx, target, iter, ifs)
    case GeneratorExp(elt, gens) => py"${expression(ctx, elt)} ${spaces(ctx, gens)}"
    case ListComp(elt, gens) => py"[${expression(ctx, elt)} ${spaces(ctx, gens)}]"
    case SetComp(elt, gens) => py"{${expression(ctx, elt)} ${spaces(ctx, gens)}}"
    case DictComp(key, value, gens) => py"{${generate(ctx, key)}: ${generate(ctx, value)} ${spaces(ctx, gens)}}"
    case IfExp(test, body, orElse) => ifExpr(ctx, test, body, orElse)
    case Lambda(args, body) => py"lambda ${arguments(ctx, args)}: ${expression(ctx, body)}"
    case Tuple(elements, _) => py"(${commas(ctx, elements)},)"
    case Attribute(value, ir.Name(attr), _) => py"${expression(ctx, value)}.$attr"
    case Subscript(value, index, _) => py"${expression(ctx, value)}[${expression(ctx, index)}]"
    case List(elements, _) => py"[${commas(ctx, elements)}]"
    case Set(Nil) => py"set()"
    case Set(elements) => py"{${commas(ctx, elements)}}"
    case _ => partialResult(expr)
  }

  def spaces(ctx: GeneratorContext, expressions: Seq[ir.Expression]): Python = {
    expressions.map(expression(ctx, _)).mkPython(" ")
  }

  private def comprehension(
     ctx: GeneratorContext,
     target: Expression,
     iter: Expression,
     ifs: Seq[Expression]
  ): Python = {
    val ifsExpr = ifs.map(expression(ctx, _)).mkPython(" and ")
    val base = py"for ${expression(ctx, target)} in ${expression(ctx, iter)}"
    if (ifsExpr.isEmpty) {
      base
    } else {
      py"$base if $ifsExpr"
    }
  }

  private def ifExpr(ctx: GeneratorContext, test: Expression, body: Expression, orelse: Expression): Python = {
    py"${expression(ctx, body)} if ${expression(ctx, test)} else ${expression(ctx, orelse)}"
  }

  def arguments(ctx: GeneratorContext, arguments: Arguments): Python = {
    // TODO: add support for defaults
    val positional = arguments.args match {
      case Nil => None
      case some => Some(commas(ctx, some))
    }
    val args = arguments.vararg map { case ir.Name(name) => py"*$name" }
    val kwargs = arguments.kwargs map { case ir.Name(name) => py"**$name" }
    val argumentLists = Seq(positional, args, kwargs).filter(_.nonEmpty).map(_.get)
    argumentLists.mkPython(", ")
  }

  private def slice(ctx: GeneratorContext, s: Slice): Python = s match {
    case Slice(None, None, None) => py":"
    case Slice(Some(lower), None, None) => py"${expression(ctx, lower)}:"
    case Slice(None, Some(upper), None) => py":${expression(ctx, upper)}"
    case Slice(Some(lower), Some(upper), None) => py"${expression(ctx, lower)}:${expression(ctx, upper)}"
    case Slice(None, None, Some(step)) => py"::${expression(ctx, step)}"
    case Slice(Some(lower), None, Some(step)) => py"${expression(ctx, lower)}::${expression(ctx, step)}"
    case Slice(None, Some(upper), Some(step)) => py":${expression(ctx, upper)}:${expression(ctx, step)}"
    case Slice(Some(lower), Some(upper), Some(step)) =>
      py"${expression(ctx, lower)}:${expression(ctx, upper)}:${expression(ctx, step)}"
  }

  private def dict(ctx: GeneratorContext, d: Dict): Python = {
    d.keys.zip(d.values).map { case (k, v) =>
      py"${expression(ctx, k)}: ${expression(ctx, v)}"
    } mkPython("{", ", ", "}")
  }

  private def call(ctx: GeneratorContext, c: Call): Python = {
    val args = c.args.map(expression(ctx, _))
    val kwargs = c.keywords.map { case Keyword(k, v) => py"${expression(ctx, k)}=${expression(ctx, v)}" }
    py"${expression(ctx, c.func)}(${(args ++ kwargs).mkPython(", ")})"
  }

  private def arithmetic(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.UMinus(child) => py"-${expression(ctx, child)}"
    case ir.UPlus(child) => py"+${expression(ctx, child)}"
    case ir.Multiply(left, right) => py"${expression(ctx, left)} * ${expression(ctx, right)}"
    case ir.Divide(left, right) => py"${expression(ctx, left)} / ${expression(ctx, right)}"
    case ir.Mod(left, right) => py"${expression(ctx, left)} % ${expression(ctx, right)}"
    case ir.Add(left, right) => py"${expression(ctx, left)} + ${expression(ctx, right)}"
    case ir.Subtract(left, right) => py"${expression(ctx, left)} - ${expression(ctx, right)}"
  }

  // see com.databricks.labs.remorph.generators.py.rules.AndOrToBitwise
  private def predicate(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.BitwiseOr(left, right) => py"${expression(ctx, left)} | ${expression(ctx, right)}"
    case ir.BitwiseAnd(left, right) => py"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.And(left, right) => py"${expression(ctx, left)} and ${expression(ctx, right)}"
    case ir.Or(left, right) => py"${expression(ctx, left)} or ${expression(ctx, right)}"
    case ir.Not(child) => py"~(${expression(ctx, child)})"
    case ir.Equals(left, right) => py"${expression(ctx, left)} == ${expression(ctx, right)}"
    case ir.NotEquals(left, right) => py"${expression(ctx, left)} != ${expression(ctx, right)}"
    case ir.LessThan(left, right) => py"${expression(ctx, left)} < ${expression(ctx, right)}"
    case ir.LessThanOrEqual(left, right) => py"${expression(ctx, left)} <= ${expression(ctx, right)}"
    case ir.GreaterThan(left, right) => py"${expression(ctx, left)} > ${expression(ctx, right)}"
    case ir.GreaterThanOrEqual(left, right) => py"${expression(ctx, left)} >= ${expression(ctx, right)}"
    case _ => partialResult(expr)
  }

  private def literal(ctx: GeneratorContext, l: ir.Literal): Python = l match {
    case ir.Literal(_, ir.NullType) => py"None"
    case ir.Literal(bytes: Array[Byte], ir.BinaryType) => OkResult(bytes.map("%02X" format _).mkString)
    case ir.Literal(true, ir.BooleanType) => py"True"
    case ir.Literal(false, ir.BooleanType) => py"False"
    case ir.Literal(value, ir.ShortType) => OkResult(value.toString)
    case ir.IntLiteral(value) => OkResult(value.toString)
    case ir.Literal(value, ir.LongType) => OkResult(value.toString)
    case ir.FloatLiteral(value) => OkResult(value.toString)
    case ir.DoubleLiteral(value) => OkResult(value.toString)
    case ir.DecimalLiteral(value) => OkResult(value.toString)
    case ir.Literal(value: String, ir.StringType) => singleQuote(value)
    case _ => partialResult(l, ir.UnsupportedDataType(l.dataType.toString))
  }

  private def singleQuote(s: String): Python = py"'$s'"
}
