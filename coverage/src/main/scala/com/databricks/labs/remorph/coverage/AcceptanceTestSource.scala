package com.databricks.labs.remorph.coverage

import java.io.File
import java.nio.file.{Files, Path, Paths}
import scala.annotation.tailrec
import scala.collection.JavaConverters._

case class AcceptanceTest(testName: String, inputFile: File)

trait AcceptanceTestSource {
  def listTests: Seq[AcceptanceTest]
}

object NestedFiles {
  def projectRoot: String = checkProjectRoot(Paths.get(".")) match {
    case p if p == Paths.get("/") => throw new RuntimeException("Could not find project root")
    case p => p.toString
  }

  @tailrec private def checkProjectRoot(current: Path): Path = {
    val a = System.getProperty("user.dir")
    val b = Paths.get(".").toAbsolutePath
    throw new RuntimeException(s"current: $current, a: $a, b: $b")

    // check if labs.yml exists in the current folder
    if (Files.exists(current.resolve("labs.yml"))) {
      current
    } else {
      checkProjectRoot(current.getParent)
    }
  }
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
