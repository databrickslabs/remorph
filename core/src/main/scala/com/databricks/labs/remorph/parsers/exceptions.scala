package com.databricks.labs.remorph.parsers

case class NotYetImplemented(msg: String) extends UnsupportedOperationException(msg)

case class UnexpectedParserOutput(msg: String) extends IllegalStateException(msg)