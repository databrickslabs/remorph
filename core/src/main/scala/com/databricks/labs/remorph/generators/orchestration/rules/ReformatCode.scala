package com.databricks.labs.remorph.generators.orchestration.rules

import com.databricks.labs.remorph.{KoResult, OkResult, PartialResult}
import com.databricks.labs.remorph.generators.orchestration.rules.converted.{SuccessPy, SuccessSQL}
import com.databricks.labs.remorph.generators.py.RuffFormatter
import com.databricks.labs.remorph.intermediate.Rule
import com.databricks.labs.remorph.intermediate.workflows.JobNode
import com.github.vertical_blank.sqlformatter.SqlFormatter
import com.github.vertical_blank.sqlformatter.languages.Dialect

class ReformatCode extends Rule[JobNode] {
  private val ruff = new RuffFormatter()
  private val sqlf = SqlFormatter.of(Dialect.SparkSql)

  override def apply(tree: JobNode): JobNode = tree transformUp {
    case SuccessSQL(name, code) => SuccessSQL(name, sqlf.format(code))
    case SuccessPy(name, code) =>
      ruff.format(code) match {
        case OkResult(output) => SuccessPy(name, output)
        case PartialResult(output, _) => SuccessPy(name, output)
        case KoResult(_, _) => SuccessPy(name, code)
      }
  }
}
