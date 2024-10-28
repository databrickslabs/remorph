package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

trait PyCommon {
  def methodOf(value: ir.Expression, name: String, args: Seq[ir.Expression]): ir.Expression =
    py.Call(py.Attribute(value, ir.Name(name)), args)
}
