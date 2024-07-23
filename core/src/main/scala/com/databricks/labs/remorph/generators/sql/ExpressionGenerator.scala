package com.databricks.labs.remorph.generators.sql

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.intermediate.Literal
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import java.text.SimpleDateFormat
import java.util.Locale

class ExpressionGenerator {
  private val dateFormat = new SimpleDateFormat("yyyy-MM-dd")
  private val timeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS")

  def expression(ctx: GeneratorContext, expr: ir.Expression): String = {
    expr match {
      case l: ir.Literal => literal(ctx, l)
      case _ => throw new IllegalArgumentException(s"Unsupported expression: $expr")
    }
  }

  private def literal(ctx: GeneratorContext, l: Literal): String = {
    l.dataType match {
      case ir.NullType => "NULL"
      case ir.BinaryType => orNull(l.binary.map(_.map("%02X" format _).mkString))
      case ir.BooleanType => orNull(l.boolean.map(_.toString.toUpperCase(Locale.getDefault)))
      case ir.ShortType => orNull(l.short.map(_.toString))
      case ir.IntegerType => orNull(l.integer.map(_.toString))
      case ir.LongType => orNull(l.long.map(_.toString))
      case ir.FloatType => orNull(l.float.map(_.toString))
      case ir.DoubleType => orNull(l.double.map(_.toString))
      case ir.StringType => orNull(l.string.map(doubleQuote))
      case ir.DateType => l.date match {
        case Some(date) => doubleQuote(dateFormat.format(date))
        case None => "NULL"
      }
      case ir.TimestampType => l.timestamp match {
        case Some(timestamp) => doubleQuote(timeFormat.format(timestamp))
        case None => "NULL"
      }
      case ir.ArrayType(_) => orNull(l.array.map(arrayExpr(ctx)))
      case ir.MapType(_, _) => orNull(l.map.map(mapExpr(ctx)))
      case _ => throw new IllegalArgumentException(s"Unsupported expression: ${l.dataType}")
    }
  }

  private def mapExpr(ctx: GeneratorContext)(map: ir.MapExpr): String = {
    val entries = map.keys.zip(map.values).map {
      case (key, value) => s"${literal(ctx, key)}, ${expression(ctx, value)}"
    }
    // TODO: line-width formatting
    s"MAP(${entries.mkString(", ")})"
  }

  private def arrayExpr(ctx: GeneratorContext)(array: ir.ArrayExpr): String = {
    val elements = array.elements.map {
      element => expression(ctx, element)
    }
    // TODO: line-width formatting
    s"ARRAY(${elements.mkString(", ")})"
  }

  private def orNull(option: Option[String]): String = option.getOrElse("NULL")

  private def doubleQuote(s: String): String = s""""$s""""
}
