package com.databricks.labs.remorph.parsers.intermediate

trait IRHelpers {

  protected def namedTable(name: String): LogicalPlan = NamedTable(name, Map.empty, is_streaming = false)
  protected def simplyNamedColumn(name: String): Column = Column(None, Id(name))
  protected def crossJoin(left: LogicalPlan, right: LogicalPlan): LogicalPlan =
    Join(left, right, None, CrossJoin, Seq(), JoinDataType(is_left_struct = false, is_right_struct = false))
}
