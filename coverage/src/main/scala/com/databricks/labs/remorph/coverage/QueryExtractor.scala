package com.databricks.labs.remorph.coverage

import java.io.File
import scala.io.Source

trait QueryExtractor {
  def extractQuery(file: File): Option[(String, String)]
}

class CommentBasedQueryExtractor(startComment: String, endComment: String) extends QueryExtractor {

  override def extractQuery(file: File): Option[(String, String)] = {
    val source = Source.fromFile(file)
    val indexedLines = source.getLines().zipWithIndex.toVector
    source.close()
    val startIndexOpt = indexedLines.find(_._1 == startComment).map(_._2)
    val endIndexOpt = indexedLines.find(_._1 == endComment).map(_._2)
    (startIndexOpt, endIndexOpt) match {
      case (Some(startIndex), Some(endIndex)) =>
        val inputQuery = indexedLines.map(_._1).slice(startIndex + 1, endIndex).mkString("\n")
        val expectedTranslation = indexedLines.map(_._1).drop(endIndex + 1).mkString("\n")
        Some((inputQuery, expectedTranslation))
      case _ => None
    }
  }
}

class DialectNameCommentBasedQueryExtractor(sourceDialect: String, targetDialect: String)
    extends CommentBasedQueryExtractor(s"-- $sourceDialect sql:", s"-- $targetDialect sql:")
