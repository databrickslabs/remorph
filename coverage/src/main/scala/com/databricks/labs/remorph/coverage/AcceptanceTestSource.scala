package com.databricks.labs.remorph.coverage

import java.io.File
import java.nio.file.{Files, Path}
import scala.collection.JavaConverters._

case class AcceptanceTest(testName: String, inputFile: File)

trait AcceptanceTestSource {
  def listTests: Seq[AcceptanceTest]
}

class NestedFiles(root: Path) extends AcceptanceTestSource {
  def listTests: Seq[AcceptanceTest] = {
    val files =
      Files
        .walk(root)
        .iterator()
        .asScala
        .filter(f => Files.isRegularFile(f))
        .toSeq

    val sqlFiles = files.filter(_.getFileName.toString.endsWith(".sql"))
    sqlFiles.map(p => AcceptanceTest(root.relativize(p).toString, p.toFile))
  }
}
