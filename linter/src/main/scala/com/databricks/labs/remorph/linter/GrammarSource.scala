package com.databricks.labs.remorph.linter

import java.io.File
import java.nio.file.{Files, Path}
import scala.collection.JavaConverters._

case class GrammarLint(grammarName: String, inputFile: File)

trait GrammarLintSource {
  def listGrammars: Seq[GrammarLint]
}

class NestedFiles(root: Path) extends GrammarLintSource {
  def listGrammars: Seq[GrammarLint] = {
    val files =
      Files
        .walk(root)
        .iterator()
        .asScala
        .filter(f => Files.isRegularFile(f))
        .toSeq

    val grammarFiles = files.filter(_.getFileName.toString.endsWith(".g4"))
    grammarFiles.map(p => GrammarLint(root.relativize(p).toString, p.toFile))
  }
}
