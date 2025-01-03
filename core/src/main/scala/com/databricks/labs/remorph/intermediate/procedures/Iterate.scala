package com.databricks.labs.remorph.intermediate.procedures

// Stops the current iteration of a loop and moves on to the next one.
case class Iterate(label: String) extends LeafStatement
