package com.databricks.labs.remorph.discovery

import java.io.File
import java.nio.file.{Files, Path}
import scala.collection.JavaConverters._
import scala.io.Source

class FileQueryHistory(path: Path) extends QueryHistoryProvider {

  private def extractQueriesFromFile(file: File): Seq[ExecutedQuery] = {
    val fileContent = Source.fromFile(file)
    val queries = fileContent.getLines().mkString("\n").split(";").map(_.trim).filter(_.nonEmpty)
    queries.map(ExecutedQuery("10", _, QuerySpec(filename = Some(file.getName))))
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
