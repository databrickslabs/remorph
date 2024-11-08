package com.databricks.labs.remorph.preprocessor

/**
 * Defines the configuration for the preprocessor, such as Jinga templating delimiters and
 * any DBT parameters that are relevant to us.
 * @param exprStart the char sequence that starts a Ninja expression construct
 * @param exprEnd the char sequence that ends a Ninja expression construct
 * @param statStart the char sequence that starts a Ninja statement construct
 * @param statEnd the char sequence that ends a Ninja statement construct
 * @param commentStart the char sequence that starts a Ninja comment construct
 * @param commentEnd the char sequence that ends a Ninja comment construct
 */
case class Config(
    exprStart: String,
    exprEnd: String,
    statStart: String,
    statEnd: String,
    commentStart: String,
    commentEnd: String) {

  // Standard defaults for Jinga templating
  def this() = this("{{", "}}", "{%", "%}", "{#", "#}")

}
