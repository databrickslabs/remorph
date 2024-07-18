package com.databricks.labs.remorph.parsers.intermediate

trait IRHelpers {

  protected def namedTable(name: String): Relation = NamedTable(name, Map.empty, is_streaming = false)
  protected def simplyNamedColumn(name: String): Column = Column(None, Id(name))
  protected def crossJoin(left: Relation, right: Relation): Relation =
    Join(left, right, None, CrossJoin, Seq(), JoinDataType(is_left_struct = false, is_right_struct = false))
}
