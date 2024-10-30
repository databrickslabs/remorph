package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.utils.StandardInputPythonSubprocess
import com.databricks.labs.remorph.Result

class RuffFormatter {
  private val ruffFmt = new StandardInputPythonSubprocess("ruff format -")
  def format(input: String): Result[String] = ruffFmt(input)
}