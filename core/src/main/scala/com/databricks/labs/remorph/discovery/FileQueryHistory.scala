package com.databricks.labs.remorph.discovery

import java.io.File
import java.nio.file.{Files, Path}
import scala.collection.JavaConverters._
import scala.io.Source

class FileQueryHistory(path: Path) extends QueryHistoryProvider {

  private def extractQueriesFromFile(file: File): Seq[ExecutedQuery] = {
    val fileContent = Source.fromFile(file)

    val queryMap = fileContent
      .getLines()
      .zipWithIndex
      .foldLeft((Map.empty[Int, String], "", 1)) { case ((acc, query, startLineNumber), (line, lineNumber)) =>
        val newQuery = query + line + "\n"
        if (line.endsWith(";")) {
          (acc + (startLineNumber -> newQuery), "", lineNumber + 2)
        } else {
          (acc, newQuery, startLineNumber)
        }
      }
      ._1

    queryMap.map { case (lineNumber, stmt) =>
      ExecutedQuery(id = s"${file.getName}#${lineNumber}", source = stmt, filename = Some(file.getName))
    }.toSeq
  }

  private def extractQueriesFromFolder(folder: Path): Seq[ExecutedQuery] = {
    val files =
      Files
        .walk(folder)
        .iterator()
        .asScala
        .filter(f => Files.isRegularFile(f))
        .toSeq
        .filter(_.getFileName.toString.endsWith(".sql"))

    files.flatMap(file => extractQueriesFromFile(file.toFile))
  }

  override def history(): QueryHistory = {
    val queries = extractQueriesFromFolder(path)
    QueryHistory(queries)
  }

}
