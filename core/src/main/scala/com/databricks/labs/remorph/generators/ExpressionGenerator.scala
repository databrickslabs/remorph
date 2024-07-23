package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.parsers.intermediate.Literal
import com.databricks.labs.remorph.parsers.{intermediate => ir}

class ExpressionGenerator {
  def expression(expr: ir.Expression): String = {
    expr match {
      case l: ir.Literal => literal(l)
      case _ => throw new IllegalArgumentException(s"Unsupported expression: $expr")
    }
  }

  private def literal(l: Literal): String = {
    l.dataType match {
      case ir.NullType => "NULL"
    }
  }
}
