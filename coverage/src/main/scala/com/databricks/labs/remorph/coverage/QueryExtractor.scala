package com.databricks.labs.remorph.coverage

import java.io.File
import scala.io.Source

trait QueryExtractor {
  def extractQuery(file: File): String
}

class CommentBasedQueryExtractor(startComment: String, endComment: String) extends QueryExtractor {
  override def extractQuery(file: File): String = {
    val source = Source.fromFile(file)
    val indexedLines = source.getLines().zipWithIndex.toSeq
    source.close()
    val startIndex = indexedLines.find(_._1 == startComment).map(_._2).get
    val endIndex = indexedLines.find(_._1 == endComment).map(_._2).get
    indexedLines.map(_._1).slice(startIndex + 1, endIndex).mkString("\n")
  }
}
