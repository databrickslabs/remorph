package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.Expression
import com.databricks.labs.remorph.{OkResult, Result, intermediate => ir}

import java.util.Locale

class ExpressionGenerator extends BasePythonGenerator[ir.Expression] {

  override def generate(ctx: GeneratorContext, tree: Expression): Python = expression(ctx, tree)

  def expression(ctx: GeneratorContext, expr: ir.Expression): Python = expr match {
    case ir.Name(name) => py"$name"
    case _: ir.Arithmetic => arithmetic(ctx, expr)
    case _: ir.Predicate => predicate(ctx, expr)
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
