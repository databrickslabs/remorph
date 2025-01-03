package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

trait PyCommon {
  protected def methodOf(value: ir.Expression, name: String, args: Seq[ir.Expression]): ir.Expression = {
    py.Call(py.Attribute(value, ir.Name(name)), args)
  }

  protected def F(name: String, args: Seq[ir.Expression]): ir.Expression = {
    ImportAliasSideEffect(methodOf(ir.Name("F"), name, args), "pyspark.sql.functions", alias = Some("F"))
  }
}
