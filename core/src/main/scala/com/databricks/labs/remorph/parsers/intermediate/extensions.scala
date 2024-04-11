package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

case class Column(name: String) extends Expression with AstExtension {}