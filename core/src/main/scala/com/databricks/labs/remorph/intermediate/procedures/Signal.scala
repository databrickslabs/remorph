package com.databricks.labs.remorph.intermediate.procedures

case class Signal(
    conditionName: String,
    messageParms: Map[String, String] = Map.empty,
    messageText: Option[String],
    sqlState: Option[String] = None)
    extends LeafStatement
