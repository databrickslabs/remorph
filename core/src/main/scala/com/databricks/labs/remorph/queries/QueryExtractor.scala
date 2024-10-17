package com.databricks.labs.remorph.queries

import com.databricks.labs.remorph.parsers.PlanParser
import com.databricks.labs.remorph.transpilers.SourceCode

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

class CommentBasedQueryExtractor(inputDialect: String, targetDialect: String) extends QueryExtractor {

  private val markerCommentPattern = "--\\s*(\\S+)\\s+sql:".r

  override def extractQuery(file: File): Option[ExampleQuery] = {
    val source = Source.fromFile(file)

    val linesByDialect = source
      .getLines()
      .foldLeft((Option.empty[String], Map.empty[String, Seq[String]])) {
        case ((currentDialect, dialectToLines), line) =>
          markerCommentPattern.findFirstMatchIn(line) match {
            case Some(m) => (Some(m.group(1)), dialectToLines)
            case None =>
              if (currentDialect.isDefined) {
                (
                  currentDialect,
                  dialectToLines.updated(
                    currentDialect.get,
                    dialectToLines.getOrElse(currentDialect.get, Seq()) :+ line))
              } else {
                (currentDialect, dialectToLines)
              }
          }
      }
      ._2

    linesByDialect.get(inputDialect).map { linesForInputDialect =>
      ExampleQuery(linesForInputDialect.mkString("\n"), linesByDialect.get(targetDialect).map(_.mkString("\n")))
    }
  }
}

class ExampleDebugger(getParser: String => PlanParser[_], prettyPrinter: Any => Unit) {
  def debugExample(name: String, maybeDialect: Option[String]): Unit = {
    val dialect = maybeDialect.getOrElse("snowflake")
    val parser = getParser(dialect)
    val extractor = new CommentBasedQueryExtractor(dialect, "databricks")
    extractor.extractQuery(new File(name)) match {
      case Some(ExampleQuery(query, _)) =>
        parser.parse(new SourceCode(query)).flatMap(parser.visit) match {
          case com.databricks.labs.remorph.Result.Failure(stage, errorJson) =>
            // scalastyle:off println
            System.err.println(s"Failed to parse query: $query $errorJson")
          // scalastyle:on println
          case com.databricks.labs.remorph.Result.Success(plan) =>
            prettyPrinter(plan)
        }
      case None => throw new IllegalArgumentException(s"Example $name not found")
    }
  }
}
