package com.databricks.labs.remorph.utils

import com.databricks.labs.remorph.intermediate.TranspileFailure
import com.databricks.labs.remorph.{KoResult, OkResult, Result, WorkflowStage}

import java.io._
import scala.annotation.tailrec
import scala.sys.process.{Process, ProcessIO}
import scala.util.control.NonFatal

class StandardInputPythonSubprocess(passArgs: String) {
  def apply(input: String): Result[String] = {
    val process = Process(s"$getEffectivePythonBin -m $passArgs", None)
    val output = new StringBuilder
    val error = new StringBuilder
    try {
      val result = process.run(createIO(input, output, error)).exitValue()
      if (result != 0) {
        KoResult(WorkflowStage.FORMAT, new TranspileFailure(new IOException(error.toString)))
      } else {
        OkResult(output.toString)
      }
    } catch {
      case e: IOException if e.getMessage.contains("Cannot run") =>
        val failure = new TranspileFailure(new IOException("Invalid $PYTHON_BIN environment variable"))
        KoResult(WorkflowStage.FORMAT, failure)
      case NonFatal(e) =>
        KoResult(WorkflowStage.FORMAT, new TranspileFailure(e))
    }
  }

  private def createIO(input: String, output: StringBuilder, error: StringBuilder) = new ProcessIO(
    stdin => {
      stdin.write(input.getBytes)
      stdin.close()
    },
    stdout => {
      val reader = new BufferedReader(new InputStreamReader(stdout))
      var line: String = reader.readLine()
      while (line != null) {
        output.append(s"$line\n")
        line = reader.readLine()
      }
      reader.close()
    },
    stderr => {
      val reader = new BufferedReader(new InputStreamReader(stderr))
      var line: String = reader.readLine()
      while (line != null) {
        error.append(s"$line\n")
        line = reader.readLine()
      }
      reader.close()
    })

  private def getEffectivePythonBin: String = {
    sys.env.getOrElse(
      "PYTHON_BIN", {
        val projectRoot = findLabsYmlFolderIn(new File(System.getProperty("user.dir")))
        val venvPython = new File(projectRoot, ".venv/bin/python")
        venvPython.getAbsolutePath
      })
  }

  @tailrec private def findLabsYmlFolderIn(path: File): File = {
    if (new File(path, "labs.yml").exists()) {
      path
    } else {
      val parent = path.getParentFile
      if (parent == null) {
        throw new FileNotFoundException(
          "labs.yml not found anywhere in the project hierarchy. " +
            "Please set PYTHON_BIN environment variable to point to the correct Python binary.")
      }
      findLabsYmlFolderIn(parent)
    }
  }
}
