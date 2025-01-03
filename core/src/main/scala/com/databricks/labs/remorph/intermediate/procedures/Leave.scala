package com.databricks.labs.remorph.intermediate.procedures

// Resumes execution following the specified labeled statement.
case class Leave(label: String) extends LeafStatement
