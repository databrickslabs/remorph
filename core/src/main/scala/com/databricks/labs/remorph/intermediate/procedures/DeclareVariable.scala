package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.{DataType, Expression}

case class DeclareVariable(name: String, datatype: DataType, default: Option[Expression] = None) extends LeafStatement
