package com.databricks.labs.remorph.parsers.intermediate

abstract class Statement extends TreeNode {}

case class CreateVariable(name: String, dataType: DataType, defaultExpr: Option[Expression], replace: Boolean)
    extends Statement {}

case class SetVariable(name: String, dataType: Option[DataType], expr: Option[Expression]) extends Statement {}
