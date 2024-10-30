package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.intermediate.TranspileFailure
import com.databricks.labs.remorph.utils.StandardInputPythonSubprocess
import com.databricks.labs.remorph.{KoResult, OkResult, Result, WorkflowStage}

class RuffFormatter {
  private val ruffFmt = new StandardInputPythonSubprocess("ruff format -")
  def format(input: String): Result[String] = ruffFmt(input)
}