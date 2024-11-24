package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators._
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{intermediate => ir}

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {
  override def generate(tree: Expression): Python = expression(tree)

  private def expression(expr: ir.Expression): Python = expr match {
    case ir.Name(name) => code"$name"
    case _: ir.Arithmetic => arithmetic(expr)
    case _: ir.Predicate => predicate(expr)
    case l: ir.Literal => literal(l)
    case c: Call => call(c)
    case d: Dict => dict(d)
    case s: Slice => slice(s)
    case Comment(child, text) => withGenCtx(ctx => code"# $text\n${ctx.ws}${expression(child)}")
    case Comprehension(target, iter, ifs) => comprehension(target, iter, ifs)
    case GeneratorExp(elt, gens) => code"${expression(elt)} ${spaces(gens)}"
    case ListComp(elt, gens) => code"[${expression(elt)} ${spaces(gens)}]"
    case SetComp(elt, gens) => code"{${expression(elt)} ${spaces(gens)}}"
    case DictComp(key, value, gens) => code"{${generate(key)}: ${generate(value)} ${spaces(gens)}}"
    case IfExp(test, body, orElse) => ifExpr(test, body, orElse)
    case Lambda(args, body) => code"lambda ${arguments(args)}: ${expression(body)}"
    case Tuple(elements, _) => code"(${commas(elements)},)"
    case Attribute(value, attr, _) => code"${expression(value)}.${expression(attr)}"
    case Subscript(value, index, _) => code"${expression(value)}[${expression(index)}]"
    case List(elements, _) => code"[${commas(elements)}]"
    case Set(Nil) => code"set()"
    case Set(elements) => code"{${commas(elements)}}"
    case _ => partialResult(expr)
  }

  private def comprehension(target: Expression, iter: Expression, ifs: Seq[Expression]): Python = {
    val ifsExpr = ifs.map(expression(_)).mkCode(" and ")
    val base = code"for ${expression(target)} in ${expression(iter)}"
    ifsExpr.isEmpty.flatMap { isEmpty =>
      if (isEmpty) {
        base
      } else {
        code"$base if $ifsExpr"
      }
    }
  }

  private def ifExpr(test: Expression, body: Expression, orelse: Expression): Python = {
    code"${expression(body)} if ${expression(test)} else ${expression(orelse)}"
  }

  def arguments(arguments: Arguments): Python = {
    // TODO: add support for defaults
    val positional = arguments.args match {
      case Nil => None
      case some => Some(commas(some))
    }
    val args = arguments.vararg map { case ir.Name(name) => code"*$name" }
    val kwargs = arguments.kwargs map { case ir.Name(name) => code"**$name" }
    val argumentLists = Seq(positional, args, kwargs).filter(_.nonEmpty).map(_.get)
    argumentLists.mkCode(", ")
  }

  private def slice(s: Slice): Python = s match {
    case Slice(None, None, None) => code":"
    case Slice(Some(lower), None, None) => code"${expression(lower)}:"
    case Slice(None, Some(upper), None) => code":${expression(upper)}"
    case Slice(Some(lower), Some(upper), None) => code"${expression(lower)}:${expression(upper)}"
    case Slice(None, None, Some(step)) => code"::${expression(step)}"
    case Slice(Some(lower), None, Some(step)) => code"${expression(lower)}::${expression(step)}"
    case Slice(None, Some(upper), Some(step)) => code":${expression(upper)}:${expression(step)}"
    case Slice(Some(lower), Some(upper), Some(step)) =>
      code"${expression(lower)}:${expression(upper)}:${expression(step)}"
  }

  private def dict(d: Dict): Python = {
    d.keys.zip(d.values).map { case (k, v) =>
      code"${expression(k)}: ${expression(v)}"
    } mkCode ("{", ", ", "}")
  }

  private def call(c: Call): Python = {
    val args = c.args.map(expression(_))
    val kwargs = c.keywords.map { case Keyword(k, v) => code"${expression(k)}=${expression(v)}" }
    code"${expression(c.func)}(${(args ++ kwargs).mkCode(", ")})"
  }

  private def arithmetic(expr: ir.Expression): Python = expr match {
    case ir.UMinus(child) => code"-${expression(child)}"
    case ir.UPlus(child) => code"+${expression(child)}"
    case ir.Multiply(left, right) => code"${expression(left)} * ${expression(right)}"
    case ir.Divide(left, right) => code"${expression(left)} / ${expression(right)}"
    case ir.Mod(left, right) => code"${expression(left)} % ${expression(right)}"
    case ir.Add(left, right) => code"${expression(left)} + ${expression(right)}"
    case ir.Subtract(left, right) => code"${expression(left)} - ${expression(right)}"
  }

  // see com.databricks.labs.remorph.generators.py.rules.AndOrToBitwise
  private def predicate(expr: ir.Expression): Python = expr match {
    case ir.BitwiseOr(left, right) => code"${expression(left)} | ${expression(right)}"
    case ir.BitwiseAnd(left, right) => code"${expression(left)} & ${expression(right)}"
    case ir.And(left, right) => code"${expression(left)} and ${expression(right)}"
    case ir.Or(left, right) => code"${expression(left)} or ${expression(right)}"
    case ir.Not(child) => code"~(${expression(child)})"
    case ir.Equals(left, right) => code"${expression(left)} == ${expression(right)}"
    case ir.NotEquals(left, right) => code"${expression(left)} != ${expression(right)}"
    case ir.LessThan(left, right) => code"${expression(left)} < ${expression(right)}"
    case ir.LessThanOrEqual(left, right) => code"${expression(left)} <= ${expression(right)}"
    case ir.GreaterThan(left, right) => code"${expression(left)} > ${expression(right)}"
    case ir.GreaterThanOrEqual(left, right) => code"${expression(left)} >= ${expression(right)}"
    case _ => partialResult(expr)
  }

  private def literal(l: ir.Literal): Python = l match {
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
