package com.databricks.labs.remorph.parsers

case class ParseException(msg: String) extends RuntimeException(msg)
