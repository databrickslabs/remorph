package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{OkResult, intermediate => ir}

import java.util.Locale

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {

  def many(ctx: GeneratorContext, expressions: Seq[ir.Expression]): Python = {
    expressions.map(generate(ctx, _)).mkPython(", ")
  }

  override def generate(ctx: GeneratorContext, tree: Expression): Python = expression(ctx, tree)

  private def expression(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.Name(name) => py"$name"
    case _: ir.Arithmetic => arithmetic(ctx, expr)
    case _: ir.Predicate => predicate(ctx, expr)
    case l: ir.Literal => literal(ctx, l)
    case c: Call => call(ctx, c)
    case d: Dict => dict(ctx, d)
    case s: Slice => slice(ctx, s)
    case GeneratorExp(elt, generators) => comp(ctx, expression(ctx, elt), generators)
    case ListComp(elt, generators) => py"[${comp(ctx, expression(ctx, elt), generators)}]"
    case SetComp(elt, generators) => py"{${comp(ctx, expression(ctx, elt), generators)}}"
    case DictComp(key, value, generators) =>
      py"{${comp(ctx, py"${generate(ctx, key)} : ${generate(ctx, value)}", generators)}}"
    case IfExp(test, body, orElse) => ifExpr(ctx, test, body, orElse)
    case Lambda(args, body) => py"lambda ${arguments(ctx, args)}: ${expression(ctx, body)}"
    case Tuple(elements, _) => py"(${elements.map(expression(ctx, _)).mkPython(", ")},)"
    case Attribute(value, attr, _) => py"${expression(ctx, value)}.$attr"
    case Subscript(value, index, _) => py"${expression(ctx, value)}[${expression(ctx, index)}]"
    case List(elements, _) => py"[${elements.map(expression(ctx, _)).mkPython(", ")}]"
    case Set(elements) => py"{${elements.map(expression(ctx, _)).mkPython(", ")}}"
    case _ => partialResult(expr)
  }

  private def comp(ctx: GeneratorContext, elt: Python, generators: Seq[Comprehension]): Python = {
    val comps = generators.map { comp =>
      val ifs = comp.ifs.map(expression(ctx, _)).mkPython(" and ")
      py"for ${expression(ctx, comp.target)} in ${expression(ctx, comp.iter)} if $ifs"
    }
    py"$elt for ${comps.mkPython(", ")}"
  }

  private def ifExpr(ctx: GeneratorContext, test: Expression, body: Expression, orelse: Expression) = {
    py"${expression(ctx, body)} if ${expression(ctx, test)} else ${expression(ctx, orelse)}"
  }

  def arguments(ctx: GeneratorContext, arguments: Arguments): Python = {
    OkResult(
      Seq( // TODO: add support for defaults
        Some(arguments.args.map(generate(ctx, _)).mkPython(", ")),
        arguments.vararg map py"*${generate(ctx, _)}",
        arguments.kwargs map py"**${generate(ctx, _)}").filter(_.nonEmpty).mkString(", "))
  }

  private def slice(ctx: GeneratorContext, s: Slice) = s match {
    case Slice(None, None, None) => py":"
    case Slice(Some(lower), None, None) => py"${expression(ctx, lower)}:"
    case Slice(None, Some(upper), None) => py":${expression(ctx, upper)}"
    case Slice(Some(lower), Some(upper), None) => py"${expression(ctx, lower)}:${expression(ctx, upper)}"
    case Slice(None, None, Some(step)) => py"::$step"
    case Slice(Some(lower), None, Some(step)) => py"${expression(ctx, lower)}::$step"
    case Slice(None, Some(upper), Some(step)) => py":${expression(ctx, upper)}:$step"
    case Slice(Some(lower), Some(upper), Some(step)) => py"${expression(ctx, lower)}:${expression(ctx, upper)}:$step"
  }

  private def dict(ctx: GeneratorContext, d: Dict) = {
    val pairs = d.keys.zip(d.values).map { case (k, v) =>
      py"${expression(ctx, k)}: ${expression(ctx, v)}"
    }
    py"{${pairs.mkPython(", ")}}"
  }

  private def call(ctx: GeneratorContext, c: Call) = {
    val args = c.args.map(expression(ctx, _))
    val kwargs = c.keywords.map { case Keyword(k, v) => py"$k=${expression(ctx, v)}" }
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

  // TODO: ir.And && ir.Or should be in PySparkExpressions
  private def predicate(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.And(left, right) => py"${expression(ctx, left)} & ${expression(ctx, right)}"
    case ir.Or(left, right) => py"${expression(ctx, left)} | ${expression(ctx, right)}"
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
    case ir.Literal(value, ir.BooleanType) => OkResult(value.toString.toLowerCase(Locale.getDefault))
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
