package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.intermediate.{Column, Id, NamedTable, Relation}

trait IRHelpers {

  protected def namedTable(name: String): Relation = NamedTable(name, Map.empty, is_streaming = false)
  protected def simplyNamedColumn(name: String): Column = Column(None, Id(name))
}
