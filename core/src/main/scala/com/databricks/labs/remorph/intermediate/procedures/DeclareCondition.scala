package com.databricks.labs.remorph.intermediate.procedures

case class DeclareCondition(name: String, sqlstate: Option[String] = None) extends LeafStatement
