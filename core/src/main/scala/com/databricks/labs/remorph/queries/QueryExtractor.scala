package com.databricks.labs.remorph.queries

import com.databricks.labs.remorph.parsers.PlanParser

import java.io.File
import scala.io.Source

trait QueryExtractor {
  def extractQuery(file: File): Option[ExampleQuery]
}

case class ExampleQuery(query: String, expectedTranslation: Option[String])

class WholeFileQueryExtractor extends QueryExtractor {
  override def extractQuery(file: File): Option[ExampleQuery] = {
    val fileContent = Source.fromFile(file)
    Some(ExampleQuery(fileContent.getLines().mkString("\n"), None))
  }
}

class CommentBasedQueryExtractor(startComment: String, endComment: String) extends QueryExtractor {

  override def extractQuery(file: File): Option[ExampleQuery] = {
    val source = Source.fromFile(file)
    val indexedLines = source.getLines().zipWithIndex.toVector
    source.close()
    val startIndexOpt = indexedLines.find(_._1 == startComment).map(_._2)
    val endIndexOpt = indexedLines.find(_._1 == endComment).map(_._2)
    (startIndexOpt, endIndexOpt) match {
      case (Some(startIndex), Some(endIndex)) =>
        val inputQuery = indexedLines.map(_._1).slice(startIndex + 1, endIndex).mkString("\n")
        val expectedTranslation = indexedLines.map(_._1).drop(endIndex + 1).mkString(" ").replaceAll("\\s+", " ").trim
        Some(ExampleQuery(inputQuery, Some(expectedTranslation)))
      case _ => None
    }
  }
}

class DialectNameCommentBasedQueryExtractor(sourceDialect: String, targetDialect: String)
    extends CommentBasedQueryExtractor(s"-- $sourceDialect sql:", s"-- $targetDialect sql:")

class ExampleDebugger(getParser: String => PlanParser[_], prettyPrinter: Any => Unit) {
  def debugExample(name: String, maybeDialect: Option[String]): Unit = {
    val dialect = maybeDialect.getOrElse("snowflake")
    val parser = getParser(dialect)
    val extractor = new DialectNameCommentBasedQueryExtractor(dialect, "databricks")
    extractor.extractQuery(new File(name)) match {
      case Some(ExampleQuery(query, _)) =>
        val plan = parser.parse(query)
        prettyPrinter(plan)
      case None => throw new IllegalArgumentException(s"Example $name not found")
    }
  }
}