package com.databricks.labs.remorph.generators.orchestration

import java.io.File
import java.nio.file.Files
import scala.collection.mutable

class FileSet {
  private val files = new mutable.HashMap[String, String]()

  def withFile(name: String, content: String): FileSet = {
    files(name) = content
    this
  }

  def getFile(name: String): Option[String] = {
    files.get(name)
  }

  def removeFile(name: String): Unit = {
    files.remove(name)
  }

  def persist(path: File): Unit = {
    files.foreach { case (name, content) =>
      val file = new File(path, name)
      if (!file.getParentFile.exists()) {
        file.getParentFile.mkdirs()
      }
      if (!file.exists()) {
        file.createNewFile()
      }
      Files.write(file.toPath, content.getBytes)
    }
  }
}
