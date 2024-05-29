package com.databricks.labs.remorph.coverage

import java.io.File
import scala.io.Source

trait QueryExtractor {
  def extractQuery(file: File): String
}

object CommentBasedQueryExtractor extends QueryExtractor {
  override def extractQuery(file: File): String = {
    val source = Source.fromFile(file)
    val indexedLines = source.getLines().zipWithIndex.toSeq
    source.close()
    val startIndex = indexedLines.find(_._1 == "-- snowflake sql:").map(_._2).get
    val endIndex = indexedLines.find(_._1 == "-- databricks sql:").map(_._2).get
    indexedLines.map(_._1).slice(startIndex + 1, endIndex).mkString("\n")
  }
}
