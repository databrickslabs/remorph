package com.databricks.labs.remorph.transpilers

import java.nio.file.{Files, Path, Paths}
import scala.io.Source.fromFile
import scala.collection.JavaConverters._

case class SourceCode(source: String, filename: String = "-- test source --")

trait Source extends Iterator[SourceCode]

class DirectorySource(root: String, fileFilter: Option[Path => Boolean] = None) extends Source {
  private val files =
    Files
      .walk(Paths.get(root))
      .iterator()
      .asScala
      .filter(f => Files.isRegularFile(f) && fileFilter.forall(filter => filter(f)))
      .toSeq
      .iterator

  override def hasNext: Boolean = files.hasNext

  override def next(): SourceCode = {
    if (!hasNext) throw new NoSuchElementException("No more source entities")
    val file = files.next()
    val source = fromFile(file.toFile)
    try {
      SourceCode(source.mkString, file.getFileName.toString)
    } finally {
      source.close()
    }
  }
}
