package com.databricks.labs.remorph.transpilers

trait Transpiler {

  def transpile(input: String): String
}
