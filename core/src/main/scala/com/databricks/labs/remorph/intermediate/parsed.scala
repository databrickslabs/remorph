package com.databricks.labs.remorph.intermediate

case class ParsedLocation(line: Int, column: Int, tokenIndex: Int)

object ParsedLocation {
  val empty: ParsedLocation = ParsedLocation(-1, -1, -1)
}

case class ParsedLocationRange(start: ParsedLocation, end: ParsedLocation) {
  def isAfterLine(line: Int): Boolean = start.line > line
}

object ParsedLocationRange {
  val empty: ParsedLocationRange = ParsedLocationRange(ParsedLocation.empty, ParsedLocation.empty)
}

