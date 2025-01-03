package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate.Expression

case class Return(value: Expression) extends LeafStatement
