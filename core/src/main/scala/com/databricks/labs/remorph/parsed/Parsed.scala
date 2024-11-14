package com.databricks.labs.remorph.parsed

case class ParsedLocation(line: Int, column: Int, tokenIndex: Int)

object ParsedLocation {
  val empty: ParsedLocation = ParsedLocation(-1, -1, -1)
}

case class ParsedRange(start: ParsedLocation, end: ParsedLocation)

object ParsedRange {
  val empty: ParsedRange = ParsedRange(ParsedLocation.empty, ParsedLocation.empty)
}


class ParsedNode[+A](val value: A, val range: ParsedRange) {

  override def equals(other: Any): Boolean = {
    other match {
      case parsed: ParsedNode[A] =>
        value == parsed.value
      case _ => false
    }
  }
  override def hashCode(): Int = value.hashCode()

}

