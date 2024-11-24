package com.databricks.labs.remorph.intermediate.procedures

import com.databricks.labs.remorph.intermediate._

case class SetVariable(name: Id, value: Expression, dataType: Option[DataType] = None) extends LeafNode with Command
