package com.databricks.labs.remorph.discovery

import java.io.File
import scala.io.Source

class FileQueryHistory(path: os.Path) extends QueryHistoryProvider {

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

  private def extractQueriesFromFolder(folder: os.Path): Seq[ExecutedQuery] = {
    val files =
      os.walk(folder)
        .filter(_.ext == "sql")

    files.flatMap(file => extractQueriesFromFile(file.toIO))
  }

  override def history(): QueryHistory = {
    val queries = extractQueriesFromFolder(path)
    QueryHistory(queries)
  }
}
